#!/usr/bin/env python3
"""
Scrape HelloWork for job signal intelligence on manufacturing SMEs.

Two modes:
  --keywords   Run all keyword × region combinations
  --companies  Run all Aerospace Valley company name searches
  --all        Both (default)

Output: data/job_signals.json  (flat list of postings)
        data/job_summary.json  (counts per company + signal score)

Usage:
  python enrich_job_boards.py --all
  python enrich_job_boards.py --companies
"""

import json
import re
import time
import argparse
from pathlib import Path
from urllib.parse import urlencode, quote_plus

import requests
from bs4 import BeautifulSoup

# ─────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────

BASE_URL = "https://www.hellowork.com/fr-fr/emploi/recherche.html"
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "fr-FR,fr;q=0.9",
}

DELAY_SECONDS = 1.5  # polite crawl delay

# ─────────────────────────────────────────────────
# Keywords — process pain signals
# ─────────────────────────────────────────────────

SIGNAL_KEYWORDS = [
    # Supply chain / procurement
    "approvisionnement",
    "approvisionneur",
    "gestionnaire approvisionnement",
    "acheteur industriel",
    "gestionnaire achats",
    "pilote flux",
    "coordinateur logistique",
    # Planning / scheduling
    "planification industrielle",
    "planificateur production",
    "ordonnancement",
    "ordonnanceur",
    "master planner",
    "demand planner",
    # Stock / inventory
    "gestionnaire stocks",
    "responsable stocks",
    "magasinier gestionnaire",
    # ERP / systems signals
    "ERP production",
    "SAP production",
    "GPAO",
    "APS planification",
    # Operations management
    "responsable supply chain",
    "directeur supply chain",
    "responsable opérations industrielles",
    "amélioration continue lean",
    "technicien méthodes",
    # Finance / reporting pain
    "contrôleur gestion industriel",
    "analyste performance industrielle",
]

REGIONS = [
    "Nouvelle-Aquitaine",
    "Occitanie",
    "Provence-Alpes-Côte d'Azur",
]

# ─────────────────────────────────────────────────
# Aerospace Valley companies (80+ members, South of France)
# From cluster directory scrape, pages 0–8
# ─────────────────────────────────────────────────

AEROSPACE_VALLEY_COMPANIES = [
    # Dept 64 / BAB area
    "NEXTEAM",
    "LAUAK GROUPE",
    "DAHER",
    "SOCATA",
    "TURBOMECA",
    "MESSIER BUGATTI DOWTY",
    "SNECMA",
    "RATIER FIGEAC",
    "LATECOE",
    "FIGEAC AERO",
    "MECAFORM",
    "MECAFI",
    "ATELIERS BIGATA",
    "CAZENAVE",
    "AMCP",
    "ECHEVERRIA",
    "COMPOSITES AQUITAINE",
    "EURO ENGINEERING",
    "EXCENT",
    "PROTEOR",
    # Dept 31 / Toulouse
    "AIRBUS",
    "STELIA AEROSPACE",
    "AEROLIA",
    "THALES ALENIA SPACE",
    "MADES",
    "MECACHROME",
    "MAPAERO",
    "LISI AEROSPACE",
    "ROXEL",
    "DUQUEINE GROUP",
    "GECI INTERNATIONAL",
    "SET WAY",
    "AKKA TECHNOLOGIES",
    "SOGECLAIR",
    "SABENA TECHNICS",
    "SATYS",
    "RECAERO",
    "PYRESCOM",
    # Dept 65 / Tarbes
    "SAFRAN",
    "LIEBHERR AEROSPACE",
    "TURBOMECA BORDES",
    "HEXCEL",
    "PROTUBEXPAND",
    "MBDA",
    "MBDA MISSILE SYSTEMS",
    # Dept 33 / Gironde
    "THALES",
    "DASSAULT AVIATION",
    "ZODIAC AEROSPACE",
    "HUTCHINSON",
    "LABINAL",
    "SAFT",
    "SNECMA SERVICES",
    "SOGERMA",
    # Occitanie / PACA others
    "AIRBUS HELICOPTERS",
    "EUROCOPTER",
    "EUROJET",
    "AERAZUR",
    "HEICO",
    "LISI FASTENERS",
    "CPI AEROSTRUCTURES",
    "COMPOSITES EN MIDI PYRENEES",
    "FIGEAC AERO GROUPE",
    "FONDASOL",
    "ALTRAN",
    "EXPLEO",
    "ALTEN",
    "ASSYSTEM",
    "SEGULA TECHNOLOGIES",
    "AKKA",
    "BERTIN TECHNOLOGIES",
    "CS GROUP",
    "INTESPACE",
    "MICROTURBO",
    "TURBOMECA AFRICA",
    "RATIER INDUSTRIES",
    # SME cluster members (smaller, higher value targets)
    "MÉCAFORM",
    "MECAFORM INDUSTRIE",
    "PYROTECHNICS",
    "AEROFONCTIONS",
    "AEROTEC",
    "AERTEC SOLUTIONS",
    "PRECISIUM GROUP",
    "MÉCAPOLE",
    "MECAPOLE INDUSTRIE",
    "PLASTIVALOIRE",
    "RADIALL",
    "SOURIAU",
    "ESTERLINE",
    "CROUZET",
    "SAFT BATTERIES",
    "SERMA TECHNOLOGIES",
    "CEVA LOGISTICS",
    "GEODIS",
    "KUEHNE NAGEL",
]

# ─────────────────────────────────────────────────
# Scraping helpers
# ─────────────────────────────────────────────────

def fetch_hellowork(keyword: str, region: str = None, page: int = 1) -> list[dict]:
    """Fetch one page of HelloWork results. Returns list of job dicts."""
    params = {"k": keyword}
    if region:
        params["l"] = region
    params["ray"] = "100"
    if page > 1:
        params["p"] = str(page)

    url = BASE_URL + "?" + urlencode(params, quote_via=quote_plus)

    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"  ⚠ Request failed: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = []

    # Extract result count
    count_el = soup.find(string=re.compile(r"\d+ offre"))
    total = 0
    if count_el:
        match = re.search(r"(\d[\d\s]*)", count_el)
        if match:
            total = int(match.group(1).replace(" ", ""))

    # Parse job cards — HelloWork renders these server-side
    for card in soup.select("article, [data-testid='job-card'], .JobCard"):
        title_el = card.find(["h2", "h3"])
        company_el = card.find(class_=re.compile(r"company|entreprise", re.I))
        location_el = card.find(class_=re.compile(r"location|localisation|ville", re.I))
        contract_el = card.find(class_=re.compile(r"contract|contrat", re.I))
        salary_el = card.find(class_=re.compile(r"salary|salaire", re.I))
        date_el = card.find(class_=re.compile(r"date|publication", re.I))
        link_el = card.find("a", href=True)

        job = {
            "title": title_el.get_text(strip=True) if title_el else None,
            "company": company_el.get_text(strip=True) if company_el else None,
            "location": location_el.get_text(strip=True) if location_el else None,
            "contract": contract_el.get_text(strip=True) if contract_el else None,
            "salary": salary_el.get_text(strip=True) if salary_el else None,
            "date": date_el.get_text(strip=True) if date_el else None,
            "url": "https://www.hellowork.com" + link_el["href"] if link_el and link_el["href"].startswith("/") else (link_el["href"] if link_el else None),
            "source_keyword": keyword,
            "source_region": region,
        }
        if job["title"]:
            jobs.append(job)

    # Fallback: parse visible text blocks when structured selectors miss
    if not jobs and total > 0:
        jobs = _parse_text_fallback(soup, keyword, region)

    return jobs, total


def _parse_text_fallback(soup: BeautifulSoup, keyword: str, region: str) -> list[dict]:
    """
    HelloWork's JS-rendered cards may not be in static HTML.
    Extract what we can from visible text: title + company + location combos.
    """
    jobs = []
    main = soup.find("main") or soup
    # Look for patterns: role name followed by company name followed by city - dept
    text_blocks = [el.get_text(" ", strip=True) for el in main.find_all(["li", "article", "div"], limit=200)]
    for block in text_blocks:
        # Heuristic: contains "H/F" or "F/H" → likely a job title line
        if "H/F" in block or "F/H" in block:
            jobs.append({
                "title": block[:120],
                "company": None,
                "location": None,
                "contract": None,
                "salary": None,
                "date": None,
                "url": None,
                "source_keyword": keyword,
                "source_region": region,
            })
    return jobs[:50]


def signal_score(jobs: list[dict]) -> int:
    """
    Score 1–5 based on job titles found.
    5 = direct process pain signal (ordonnancement, GPAO, ERP, approvisionnement)
    4 = indirect signal (supply chain manager, planificateur)
    3 = operations hire (responsable production)
    1-2 = operational roles (opérateur, cariste)
    """
    HIGH_SIGNAL = {"ordonnancement", "ordonnanceur", "approvisionneur", "approvisionnement",
                   "planificateur", "planification", "gpao", "erp", "sap", "demand planner",
                   "master planner", "aps", "gestionnaire stocks", "pilote flux"}
    MED_SIGNAL = {"supply chain", "logistique", "responsable production", "methodes",
                  "lean", "amélioration continue", "acheteur"}

    score = 0
    for job in jobs:
        title = (job.get("title") or "").lower()
        if any(kw in title for kw in HIGH_SIGNAL):
            score += 3
        elif any(kw in title for kw in MED_SIGNAL):
            score += 2
        else:
            score += 1

    return min(5, max(1, round(score / max(len(jobs), 1))))


# ─────────────────────────────────────────────────
# Main runners
# ─────────────────────────────────────────────────

def run_keyword_searches() -> list[dict]:
    """Run all keyword × region combinations."""
    all_jobs = []
    total_combos = len(SIGNAL_KEYWORDS) * len(REGIONS)
    done = 0

    print(f"\n📋 Keyword searches: {len(SIGNAL_KEYWORDS)} keywords × {len(REGIONS)} regions = {total_combos} queries\n")

    for keyword in SIGNAL_KEYWORDS:
        for region in REGIONS:
            done += 1
            print(f"  [{done}/{total_combos}] '{keyword}' in {region}...", end=" ", flush=True)
            jobs, total = fetch_hellowork(keyword, region)
            print(f"{total} results, {len(jobs)} parsed")
            all_jobs.extend(jobs)
            time.sleep(DELAY_SECONDS)

    return all_jobs


def run_company_searches() -> list[dict]:
    """Run company name searches — confirms which cluster members actively recruit."""
    all_jobs = []
    print(f"\n🏭 Company searches: {len(AEROSPACE_VALLEY_COMPANIES)} companies\n")

    for i, company in enumerate(AEROSPACE_VALLEY_COMPANIES, 1):
        print(f"  [{i}/{len(AEROSPACE_VALLEY_COMPANIES)}] {company}...", end=" ", flush=True)
        jobs, total = fetch_hellowork(company)
        print(f"{total} results")
        for job in jobs:
            job["target_company"] = company
        all_jobs.extend(jobs)
        time.sleep(DELAY_SECONDS)

    return all_jobs


def build_summary(all_jobs: list[dict]) -> dict:
    """Group by company/target and compute signal scores."""
    from collections import defaultdict

    by_company = defaultdict(list)
    for job in all_jobs:
        company = job.get("target_company") or job.get("company") or "unknown"
        by_company[company].append(job)

    summary = {}
    for company, jobs in by_company.items():
        summary[company] = {
            "total_postings": len(jobs),
            "signal_score": signal_score(jobs),
            "roles": sorted({j["title"] for j in jobs if j.get("title")}),
            "locations": sorted({j["location"] for j in jobs if j.get("location")}),
        }

    # Sort by signal score desc, then total postings
    return dict(sorted(summary.items(), key=lambda x: (-x[1]["signal_score"], -x[1]["total_postings"])))


# ─────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Enrich prospects from HelloWork job signals")
    parser.add_argument("--keywords", action="store_true")
    parser.add_argument("--companies", action="store_true")
    parser.add_argument("--all", dest="run_all", action="store_true", default=True)
    args = parser.parse_args()

    run_kw = args.keywords or args.run_all
    run_co = args.companies or args.run_all

    all_jobs = []

    if run_kw:
        all_jobs += run_keyword_searches()

    if run_co:
        all_jobs += run_company_searches()

    # Deduplicate by URL
    seen = set()
    deduped = []
    for job in all_jobs:
        key = job.get("url") or job.get("title", "") + str(job.get("company", ""))
        if key not in seen:
            seen.add(key)
            deduped.append(job)

    summary = build_summary(deduped)

    signals_path = DATA_DIR / "job_signals.json"
    summary_path = DATA_DIR / "job_summary.json"

    signals_path.write_text(json.dumps(deduped, ensure_ascii=False, indent=2))
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2))

    print(f"\n✅ Done.")
    print(f"   {len(deduped)} unique postings → {signals_path}")
    print(f"   {len(summary)} companies summarised → {summary_path}")
    print(f"\n🎯 Top 10 by signal score:")
    for company, data in list(summary.items())[:10]:
        print(f"   [{data['signal_score']}/5] {company} — {data['total_postings']} postings — {', '.join(data['roles'][:3])}")


if __name__ == "__main__":
    main()
