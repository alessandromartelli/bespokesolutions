---
name: prospect-manufacturing-bab
description: Use when running or maintaining the manufacturing prospect pipeline for BAB + South of France. Covers data sources, script execution, ENV requirements, output format, known caveats, and feed into sales pipeline.
version: 1.0.0
author: Bespoke Solutions
license: proprietary
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [prospecting, manufacturing, france-travail, aerospace-valley, pipeline, bab]
    related_skills: [sales, wiki, save]
---

# Prospect Manufacturing BAB

Automated pipeline that finds qualified manufacturing SMEs in BAB + South of France, ranks them by operational pain signals, and outputs a ready-to-use prospect list.

---

## When to Use

- Starting a new prospecting run for manufacturing in the target geography
- Debugging or extending the pipeline script
- Adding a new data source
- Troubleshooting low yield or geography drift in results

---

## Script

```
scripts/prospect_manufacturing_bab.py
```

**Run:**
```bash
source .env && python3 scripts/prospect_manufacturing_bab.py
```

**Output:** `inbox/prospects-YYYY-MM-DD.md`

**Runtime:** ~8–10 minutes total. AV detail pages are the bottleneck (616 PMEs × 0.25s).

---

## ENV Requirements

| Variable | Required | Notes |
|---|---|---|
| `FRANCE_TRAVAIL_CLIENT_ID` | Yes | Confirmed working. Format: `PAR_<appname>_<hash>` |
| `FRANCE_TRAVAIL_CLIENT_SECRET` | Yes | Confirmed working |

Recherche Entreprises and Aerospace Valley require no credentials — both are public.

---

## Pipeline Steps

```
Step 1  France Travail OAuth2 token
Step 2  FT search: 6 ROME codes × 9 departments (CDI only) → strip agencies
Step 3  Aerospace Valley: fetch list (1 req) → filter PMEs → fetch 616 detail pages
Step 4  Merge FT + AV by name, union signals and sources
Step 5  Recherche Entreprises: look up each company by name → filter manufacturing NAF + 20–249 emp → deduplicate by SIREN
Step 6  Write inbox/prospects-YYYY-MM-DD.md ranked by pain score
```

---

## Data Sources

### 1. France Travail API (job hiring signals)

- **Endpoint:** `https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search`
- **Token endpoint:** `https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire`
- **Scope:** `api_offresdemploiv2 o2dsoffre`
- **Rate limit:** 10 calls/sec (Offres d'emploi v2)
- **Safe delay:** 0.11s between requests

**Activated APIs on the account:**

| API | Rate limit |
|---|---|
| Offres d'emploi v2 | 10 calls/sec |
| ROME 4.0 Métiers v1 | 1 call/sec |
| ROME 4.0 Compétences v1 | 1 call/sec |
| ROME 4.0 Contextes de travail v1 | 1 call/sec |
| ROME 4.0 Fiches métiers v1 | 1 call/sec |
| ROMEo v2 (AI text→ROME) | 3 calls/sec |

**ROME codes queried:**

| Code | Label |
|---|---|
| M1502 | Planification |
| M1801 | ERP / SI |
| M1802 | Intégration systèmes |
| N1301 | Logistique / Supply chain |
| H1402 | Méthodes industrielles |
| H2503 | Chaudronnerie / fabrication |

**Known caveat:** Company name is masked when the offer was placed via a recruitment agency. These appear as `"non renseigné"` and are dropped.

**ROMEo note:** The ROMEo v2 API can fuzzy-match free-text job titles to ROME codes — useful for catching non-standard titles like "Chef de projet GPAO" that wouldn't match a hardcoded ROME code.

---

### 2. Aerospace Valley Member Directory (pre-qualified PMEs)

- **URL:** `https://www.aerospace-valley.com/annuaire-des-membres`
- **Auth:** None — publicly accessible, no login
- **Rate limit:** None published. Use 0.25s/request to be safe.

**Critical scraping note:** The server returns only ~16 members to Python's default `urllib` without a browser User-Agent. Must send:

```python
BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
}
```

**HTML parsing note:** Member cards have two formats for the name:
- Most: `<h3>COMPANY NAME</h3>` — plain text, no anchor
- Some: `<h3><a href="...">COMPANY NAME</a></h3>`

Always extract the name from the `<h3>` tag separately from the slug. The slug (detail page link) is always in the `class="link1"` div.

**Data per detail page:**
- Contact name + title
- Phone
- Full address (postal code → extract dept as `str(postal)[:2]`)
- Revenue (`Chiffre d'affaire annuel`)
- Employees (`Effectif (France)`)
- Website (`VOIR LE SITE` link)

**Filtering:** Only keep PMEs (`<h6>PME</h6>`) in target departments. Geography determined from postal code on detail page.

---

### 3. Recherche Entreprises API (firmographic enrichment + SIREN)

- **URL:** `https://recherche-entreprises.api.gouv.fr/search?q={name}&page=1&per_page=5`
- **Auth:** None — fully open
- **Rate limit:** 7 req/s. Use 0.15s delay.
- **Nomenclature:** NAF2025 as of 2025

**Manufacturing NAF prefixes (section C):** `22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33`

**Target `tranche_effectif_salarie` codes (20–249 employees):**

| Code | Label |
|---|---|
| 12 | 20–49 emp |
| 21 | 50–99 emp |
| 22 | 100–199 emp |
| 31 | 200–249 emp |

**Known caveat:** ~50% of establishments under 3 years old have no `tranche_effectif` data — they pass through unfiltered. The AV source partially compensates because AV publishes headcount directly on detail pages.

**Geography drift:** Name-based lookup finds the national HQ, not the local establishment that posted the job. Some results will show a department outside the target list (e.g., dept 78, 85). These are real companies with a local presence but HQ elsewhere. Review manually.

---

## Target Geography

Departments: `64, 65, 09, 11, 31, 34, 13, 83, 84`

| Zone | Depts |
|---|---|
| BAB (Biarritz-Anglet-Bayonne) | 64, 65 |
| Occitanie | 09, 11, 31, 34 |
| PACA | 13, 83, 84 |

---

## Agency Keyword Blacklist

Applied to France Travail company names before enrichment. Any name containing these substrings (lowercased) is dropped:

```
interim, intérim, recrutement, recruitment,
 rh, solutions rh, groupe rh,
adequat, adecco, crit , hays , manpower, randstad,
synergie, kelly services, proman, start people,
gi group, gi&go, fab group, triangle solutions,
aquila rh, potentiel humain, appel rh, interaction ,
ergos, mi recrutement, cluxelite, btp interim, aftral
```

Note the trailing space on `crit ` and `hays ` — prevents false positives on company names containing those strings as prefixes.

---

## Scoring

| Signal | Points |
|---|---|
| Each FT ROME code match | +1 |
| Aerospace Valley member | +1 |

Companies appearing in both sources score ≥ 2 (★★) and are highest priority.

---

## Dropped Sources

Do not re-add without a concrete workaround:

| Source | Reason |
|---|---|
| BODACC | Requires bearer token; no NAF filter; event monitoring only |
| INSEE Sirene | OAuth2 required; duplicates Recherche Entreprises; 30 req/min |
| HelloWork | No API; anti-scraping (residential proxies needed); no SME filter |
| APEC | No API; targets cadres only — wrong audience for operations pain |
| UIMM | 42,000 members but zero public company directory; only 60 regional office contacts |
| French Fab | HTTP 403 on all directory + company profile pages; login required |

---

## Output Format

File: `inbox/prospects-YYYY-MM-DD.md`

Each entry includes:
- Score (stars) and count
- Sources (France Travail / Aerospace Valley)
- Location + department
- Size (tranche label)
- NAF code
- SIREN
- Full address
- Pain signals
- Website (if from AV)
- Revenue (if from AV)
- Employees (if from AV)
- Outreach checkbox: `[ ] pending`

---

## After Running

1. Open `inbox/prospects-YYYY-MM-DD.md` in Obsidian
2. Delete any entries with obvious geography drift (dept outside 64/65/09/11/31/34/13/83/84) unless the company has a confirmed local site
3. Delete any entries that are clearly not manufacturing (check NAF if unsure)
4. For ★★ companies: run `sales research "<company name>"` first
5. For ★ AV-only companies: check their website, verify they match the target profile, then run research

**Feed into sales pipeline:**
```
sales research "ADHETEC"
sales strategize "adhetec"
sales draft "adhetec"
```

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Running without `source .env` | Script exits with `KeyError: FRANCE_TRAVAIL_CLIENT_ID` |
| Forgetting browser User-Agent on AV fetch | Returns only ~16 members instead of 900+ |
| Removing `time.sleep()` between requests | France Travail token expires mid-run or gets rate-limited |
| Matching only `<h3><a href>` pattern for AV names | Misses 885/901 cards — most use plain `<h3>NAME</h3>` |
| Assuming RE enrichment geography = hiring location | It's HQ location. Verify locally-present companies manually. |
| Re-running on same day | Overwrites `inbox/prospects-YYYY-MM-DD.md` — copy first if needed |

---

## Related

- `wiki/research/prospect-manufacturing-bab.md` — data source research and pipeline architecture
- `wiki/projects/sales-agent.md` — overall sales agent architecture
- `wiki/concepts/sales-playbook.md` — scoring, channel, outreach strategy
- `scripts/prospect_manufacturing_bab.py` — the script itself
