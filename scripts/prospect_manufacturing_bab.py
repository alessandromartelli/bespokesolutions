#!/usr/bin/env python3
"""
Prospect Manufacturing BAB + South of France
─────────────────────────────────────────────
Sources:
  1. France Travail API    — companies hiring for operational pain ROME codes
  2. Aerospace Valley dir  — pre-qualified manufacturing PMEs, scrapes detail pages

Pipeline:
  FT results + AV results
    → merge by name (AV data wins on overlap)
    → Recherche Entreprises enrichment (SIREN + NAF + size filter)
    → deduplicate by SIREN
    → rank by pain score
    → inbox/prospects-YYYY-MM-DD.md

Usage:
    source .env && python3 scripts/prospect_manufacturing_bab.py
"""

import json
import os
import re
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

# ── Configuration ─────────────────────────────────────────────────────────────

ROME_CODES = {
    "M1502": "Planification",
    "M1801": "ERP / SI",
    "M1802": "Intégration systèmes",
    "N1301": "Logistique / Supply chain",
    "H1402": "Méthodes industrielles",
    "H2503": "Chaudronnerie / fabrication",
}

# Departments: BAB (64,65) + Occitanie (09,11,31,34) + PACA (13,83,84)
DEPARTMENTS = ["64", "65", "09", "11", "31", "34", "13", "83", "84"]

# NAF division codes for manufacturing (section C)
MANUFACTURING_NAF_PREFIXES = {
    "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33"
}

# tranche_effectif for 20–249 employees
TARGET_TRANCHES = {"12", "21", "22", "31"}
TRANCHE_LABELS = {
    "12": "20–49 emp",
    "21": "50–99 emp",
    "22": "100–199 emp",
    "31": "200–249 emp",
}

# Recruitment agency keyword blacklist (lowercased substrings)
AGENCY_KEYWORDS = [
    "interim", "intérim", "recrutement", "recruitment",
    " rh", "solutions rh", "groupe rh",
    "adequat", "adecco", "crit ", "hays ", "manpower", "randstad",
    "synergie", "kelly services", "proman", "start people",
    "gi group", "gi&go", "fab group", "triangle solutions",
    "aquila rh", "potentiel humain", "appel rh", "interaction ",
    "ergos", "mi recrutement", "cluxelite", "btp interim",
    "aftral",
]

AV_BASE = "https://www.aerospace-valley.com"
AV_LIST  = f"{AV_BASE}/annuaire-des-membres"

# ── Helpers ───────────────────────────────────────────────────────────────────

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
}


def fetch(url: str, headers: dict = None) -> str:
    req = urllib.request.Request(url, headers=headers or BROWSER_HEADERS)
    return urllib.request.urlopen(req, timeout=15).read().decode("utf-8", errors="replace")


def strip_tags(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


# ── France Travail ────────────────────────────────────────────────────────────

def get_ft_token() -> str:
    data = urllib.parse.urlencode({
        "grant_type":    "client_credentials",
        "client_id":     os.environ["FRANCE_TRAVAIL_CLIENT_ID"],
        "client_secret": os.environ["FRANCE_TRAVAIL_CLIENT_SECRET"],
        "scope":         "api_offresdemploiv2 o2dsoffre",
    }).encode()
    req = urllib.request.Request(
        "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return json.loads(urllib.request.urlopen(req).read())["access_token"]


def is_agency(name: str) -> bool:
    n = name.lower()
    return any(kw in n for kw in AGENCY_KEYWORDS)


def search_ft(token: str) -> dict:
    """Returns {name: {lieu, dept, signals: set, sources: set}}"""
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    results = {}
    total = len(ROME_CODES) * len(DEPARTMENTS)
    done  = 0

    for rome_code, rome_label in ROME_CODES.items():
        for dept in DEPARTMENTS:
            done += 1
            url = (
                "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
                f"?codeROME={rome_code}&departement={dept}&typeContrat=CDI&range=0-149"
            )
            try:
                req = urllib.request.Request(url, headers=headers)
                data = json.loads(urllib.request.urlopen(req).read())
                for offer in data.get("resultats", []):
                    name = offer.get("entreprise", {}).get("nom", "").strip()
                    if not name or name.lower() == "non renseigné" or is_agency(name):
                        continue
                    lieu = offer.get("lieuTravail", {}).get("libelle", "?")
                    if name not in results:
                        results[name] = {"lieu": lieu, "dept": dept,
                                         "signals": set(), "sources": {"France Travail"}}
                    results[name]["signals"].add(rome_label)
            except Exception:
                pass
            print(f"\r  FT: {done}/{total} queries · {len(results)} raw companies", end="", flush=True)
            time.sleep(0.11)

    print()
    return results


# ── Aerospace Valley ──────────────────────────────────────────────────────────

def _parse_av_list(html: str) -> list:
    """Returns [{name, slug, type}] for all members."""
    card_html = re.split(r'<div class="member-card">', html)[1:]
    members = []
    for card in card_html:
        # Name: may be plain <h3>NAME</h3> or <h3><a ...>NAME</a></h3>
        name_m = re.search(r'<h3>(?:<a[^>]*>)?([^<]+?)(?:</a>)?</h3>', card)
        # Slug: always in the "DÉCOUVRIR" link1 div
        slug_m = re.search(r'class="link1"[^>]*>.*?href="(/annuaire-des-membres/[^"]+)"', card, re.DOTALL)
        type_m = re.search(r'<h6>([^<]+)</h6>', card)
        if name_m and slug_m and type_m:
            members.append({
                "slug": slug_m.group(1),
                "name": name_m.group(1).strip(),
                "type": type_m.group(1).strip(),
            })
    return members


def _parse_av_detail(html: str) -> dict:
    """Extract contact, address, revenue, employees, website from a member detail page."""
    result = {}

    # Postal code → department (first 2 digits)
    postal_m = re.search(r"\b(\d{5})\b", html)
    if postal_m:
        result["dept"] = postal_m.group(1)[:2]
        result["postal"] = postal_m.group(1)

    # Revenue — "Chiffre d'affaire annuel" followed by a number
    rev_m = re.search(r"Chiffre d.affaire annuel\s*[<\|]*\s*([\d\s]+)", html)
    if rev_m:
        result["revenue"] = rev_m.group(1).strip().replace(" ", "")

    # Employees — "Effectif (France)" followed by a number
    emp_m = re.search(r"Effectif\s*\(France\)\s*[<\|]*\s*(\d+)", html)
    if emp_m:
        result["employees"] = int(emp_m.group(1))

    # Website — "VOIR LE SITE" link
    site_m = re.search(r'href="(https?://[^"]+)"[^>]*>\s*VOIR LE SITE', html, re.IGNORECASE)
    if site_m:
        result["website"] = site_m.group(1)

    # Address block — grab city from postal code context
    addr_m = re.search(r"([A-ZÀÂÄÉÈÊËÎÏÔÙÛÜ\s\-]+),?\s*" + (postal_m.group(1) if postal_m else r"\d{5}"), html)
    if addr_m:
        result["commune"] = addr_m.group(0).strip()

    return result


def scrape_aerospace_valley() -> dict:
    """
    Returns {name: {dept, signals: set, sources: set, website, revenue, employees}}
    Filters to PME type + target departments only.
    """
    print("  Fetching AV member list...", end="", flush=True)
    html = fetch(AV_LIST)
    members = _parse_av_list(html)
    pmes = [m for m in members if m["type"] == "PME"]
    print(f" {len(members)} total, {len(pmes)} PMEs")

    results = {}
    for i, m in enumerate(pmes, 1):
        print(f"\r  AV detail pages: {i}/{len(pmes)}", end="", flush=True)
        try:
            detail_html = fetch(f"{AV_BASE}{m['slug']}")
            detail = _parse_av_detail(detail_html)
            dept = detail.get("dept", "")
            if dept not in DEPARTMENTS:
                time.sleep(0.25)
                continue
            results[m["name"]] = {
                "dept":      dept,
                "lieu":      detail.get("commune", "?"),
                "signals":   {"Aerospace Valley member"},
                "sources":   {"Aerospace Valley"},
                "website":   detail.get("website", ""),
                "revenue":   detail.get("revenue", ""),
                "employees": detail.get("employees", ""),
            }
        except Exception:
            pass
        time.sleep(0.25)

    print(f"\n  {len(results)} AV PMEs in target depts")
    return results


# ── Merge ─────────────────────────────────────────────────────────────────────

def merge_sources(ft: dict, av: dict) -> dict:
    """
    Merge FT and AV dicts. AV data wins on key conflicts.
    Signals and sources are unioned.
    """
    merged = {}

    for name, data in ft.items():
        merged[name] = dict(data)

    for name, data in av.items():
        if name in merged:
            merged[name]["signals"]  |= data["signals"]
            merged[name]["sources"]  |= data["sources"]
            # AV enriches with extra fields
            for key in ("website", "revenue", "employees"):
                if data.get(key):
                    merged[name][key] = data[key]
        else:
            merged[name] = dict(data)

    return merged


# ── Recherche Entreprises ─────────────────────────────────────────────────────

def enrich(name: str):
    """
    Look up by name. Returns enrichment dict if manufacturing SME, else None.
    """
    encoded = urllib.parse.quote(name)
    url = f"https://recherche-entreprises.api.gouv.fr/search?q={encoded}&page=1&per_page=5"
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        data = json.loads(urllib.request.urlopen(req).read())
        for result in data.get("results", []):
            naf     = result.get("activite_principale", "") or ""
            prefix  = naf.split(".")[0]
            tranche = result.get("tranche_effectif_salarie", "") or ""
            if prefix in MANUFACTURING_NAF_PREFIXES and tranche in TARGET_TRANCHES:
                siege = result.get("siege", {})
                return {
                    "siren":   result.get("siren", ""),
                    "naf":     naf,
                    "tranche": tranche,
                    "dept":    siege.get("departement", ""),
                    "commune": siege.get("libelle_commune", ""),
                    "address": siege.get("adresse", ""),
                }
    except Exception:
        pass
    finally:
        time.sleep(0.15)
    return None


# ── Output ────────────────────────────────────────────────────────────────────

def write_markdown(prospects: list) -> Path:
    today   = date.today().isoformat()
    out_dir = Path(__file__).parent.parent / "inbox"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"prospects-{today}.md"

    lines = [
        f"# Prospects — Manufacturing BAB + South of France — {today}",
        "",
        "**Sources**: France Travail (hiring signal) + Aerospace Valley (cluster directory)",
        "**Enriched via**: Recherche Entreprises (SIREN + NAF + size filter)",
        f"**Geography**: depts {', '.join(DEPARTMENTS)}",
        "**Filter**: NAF manufacturing (C22–C33) + 20–249 employees",
        f"**Total qualified**: {len(prospects)}",
        "",
        "---",
        "",
    ]

    for p in prospects:
        score  = len(p["signals"])
        stars  = "★" * score
        src    = ", ".join(sorted(p.get("sources", set())))
        extras = []
        if p.get("website"):
            extras.append(f"- **Website**: {p['website']}")
        if p.get("revenue"):
            extras.append(f"- **Revenue**: €{int(p['revenue']):,}".replace(",", " "))
        if p.get("employees"):
            extras.append(f"- **Employees (FR)**: {p['employees']}")

        lines += [
            f"## {p['name']}",
            f"- **Score**: {stars} ({score} signal{'s' if score > 1 else ''})",
            f"- **Sources**: {src}",
            f"- **Location**: {p['commune']} (dept {p['dept']})",
            f"- **Size**: {TRANCHE_LABELS.get(p.get('tranche',''), '?')}",
            f"- **NAF**: {p.get('naf', '?')}",
            f"- **SIREN**: {p.get('siren', '?')}",
            f"- **Address**: {p.get('address', '?')}",
            f"- **Pain signals**: {', '.join(sorted(p['signals']))}",
            *extras,
            f"- **Outreach**: [ ] pending",
            "",
        ]

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    for key in ("FRANCE_TRAVAIL_CLIENT_ID", "FRANCE_TRAVAIL_CLIENT_SECRET"):
        if not os.environ.get(key):
            raise SystemExit(f"Missing env var: {key}. Run: source .env")

    print("Step 1/5  France Travail — getting token...")
    token = get_ft_token()
    print("          OK")

    print(f"Step 2/5  France Travail — {len(ROME_CODES)} ROME codes × {len(DEPARTMENTS)} depts (CDI)...")
    ft_raw = search_ft(token)
    print(f"          {len(ft_raw)} named non-agency employers")

    print("Step 3/5  Aerospace Valley — scraping PME directory...")
    av_raw = scrape_aerospace_valley()

    print("Step 4/5  Merging sources...")
    merged = merge_sources(ft_raw, av_raw)
    print(f"          {len(merged)} unique companies ({len(ft_raw)} FT + {len(av_raw)} AV, deduped by name)")

    print("Step 5/5  Recherche Entreprises — SIREN + NAF + size filter...")
    seen_sirens = set()
    prospects   = []
    for i, (name, data) in enumerate(merged.items(), 1):
        print(f"\r          {i}/{len(merged)} checked · {len(prospects)} qualified", end="", flush=True)
        e = enrich(name)
        if not e:
            continue
        if e["siren"] and e["siren"] in seen_sirens:
            continue
        seen_sirens.add(e["siren"])
        prospects.append({
            "name":      name,
            "signals":   data["signals"],
            "sources":   data.get("sources", set()),
            "website":   data.get("website", ""),
            "revenue":   data.get("revenue", ""),
            "employees": data.get("employees", ""),
            **e,
        })
    print()

    prospects.sort(key=lambda x: len(x["signals"]), reverse=True)
    out_path = write_markdown(prospects)

    print(f"\nDone. {len(prospects)} qualified prospects → {out_path}")
    if prospects:
        print("\nTop 5 by score:")
        for p in prospects[:5]:
            src_tag = "+AV" if "Aerospace Valley" in p.get("sources", set()) else "FT "
            print(f"  [{'★' * len(p['signals'])}] [{src_tag}] {p['name']} — {p['commune']} — {TRANCHE_LABELS.get(p.get('tranche',''), '?')}")


if __name__ == "__main__":
    main()
