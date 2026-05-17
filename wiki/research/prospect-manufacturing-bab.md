# Prospect Research — Manufacturing BAB + South of France

---

## Target Profile

**Geography**: Biarritz-Bayonne-Anglet (dept 64) + Occitanie + PACA
**Vertical**: Manufacturing SMEs, 20–250 employees
**Pain**: Heavy manual processes in planning, procurement, inventory, reporting
**NAF codes to filter**: 25 (fabrication produits métalliques), 28 (machines/équipements), 29 (véhicules), 30 (autres matériels transport)

---

## Verified Source Stack

Three sources confirmed working. All others tested and dropped (see below).

### 1. Recherche Entreprises API
- **URL**: `recherche-entreprises.api.gouv.fr`
- **Auth**: None — fully open, no registration
- **Rate limit**: 7 req/s
- **Data per company**: SIREN, SIRET, denomination, NAF code, address, department, phone, email, activity start date, employee bracket (`tranche_effectif`), active status, headquarters flag
- **Filters available**: NAF code, department, employee size bracket
- **Known caveat**: ~50% of establishments under 3 years old have no `tranche_effectif` data — size filter will miss young companies. Cross-reference with Aerospace Valley for those.
- **Nomenclature**: Uses NAF2025 as of 2025
- **Role in pipeline**: Primary discovery — pull list by NAF + dept + size

### 2. Aerospace Valley Member Directory
- **URL**: `aerospace-valley.com/annuaire-des-membres`
- **Auth**: None — publicly accessible, no login required
- **Scrapability**: Standard HTML, scrapable (check robots.txt before running)
- **Member count**: 835+ members total, 580+ are SMEs (PME category)
- **Filters on site**: Region (Nouvelle-Aquitaine, Occitanie, Île-de-France + 9 others), organization type (Grande Entreprise, PME, Centre de formation, Laboratoire, etc.)
- **Data per member (list view)**: Name, member type, logo
- **Data per member (profile page)**: Contact name + title, phone, full address, website, company type, annual revenue (€), employee count (France-based), business description (bilingual)
- **Why it matters**: Pre-qualified manufacturing SMEs with revenue + headcount already included — removes a full enrichment step. BAB geography covered via Nouvelle-Aquitaine filter.
- **Role in pipeline**: Pre-qualified list, merge with Recherche Entreprises output, deduplicate by SIREN

### 3. France Travail API (ex Pôle Emploi)
- **URL**: `api.francetravail.io/partenaire/offresdemploi/v2/offres`
- **Auth**: OAuth2 — Client ID + Client Secret (free, registered at francetravail.io)
- **Token endpoint**: `https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire`
- **Scope needed**: `api_offresdemploiv2 o2dsoffre`
- **Filters available**: ROME code, department/commune, `taille_entreprise` (PME / ETI / GE), contract type, activity sector
- **Known caveat**: Company name is not always included — masked when the offer was placed via a recruitment agency
- **APIs activated** (with rate limits):
  - Offres d'emploi v2 — **10 calls/sec** ← main prospecting API
  - ROME 4.0 Métiers v1 — 1 call/sec
  - ROME 4.0 Compétences v1 — 1 call/sec
  - ROME 4.0 Contextes de travail v1 — 1 call/sec
  - ROME 4.0 Fiches métiers v1 — 1 call/sec
  - ROMEo v2 (AI text→ROME matcher) — 3 calls/sec
- **ROME codes for operational pain signals**:
  - M1502 — planification (planning)
  - M1801 — ERP / systèmes d'information
  - M1802 — systèmes d'information / intégration
  - N1301 — logistique / supply chain
- **ROMEo note**: Can be used to fuzzy-match free-text job titles to ROME codes — useful for catching non-standard titles like "Chef de projet GPAO" or "Responsable ADV"
- **Role in pipeline**: Signal layer — flag companies in hiring mode for operations roles, score higher in enrichment

---

## Dropped Sources

Tested and eliminated. Do not re-add without a concrete workaround.

| Source | Why dropped |
|---|---|
| **BODACC** | Requires bearer token (not open). No NAF filter — can only query by SIREN/name. Useful only for event monitoring (restructurings, liquidations), not discovery. Re-evaluate if we need M&A signals later. |
| **INSEE Sirene** | OAuth2 registration required. 30 req/min rate limit. Fields largely duplicate Recherche Entreprises. Adds historical data but not worth the auth friction at this stage. |
| **HelloWork** | No API. Anti-scraping protections (IP blocking) — requires residential proxies. Company names visible but no size filter. Low SME signal density. |
| **APEC** | No API. Targets cadres/executive roles only — wrong audience for operational pain signals. Not worth the scraping cost. |
| **UIMM** | 42,000 member companies but zero public directory. Only the 60 regional office contacts are accessible. Individual member data not available. |
| **French Fab** | Directory returns HTTP 403 on all listing and profile pages. Login required. 853+ companies listed but completely inaccessible programmatically. |

---

## Pipeline Flow

```
Recherche Entreprises API
  └── filter: NAF 25/28/29/30 + dept 64/65/09/11/31/34 + tranche_effectif ≥ 11
      ↓
Aerospace Valley directory
  └── filter: Nouvelle-Aquitaine + Occitanie, type = PME
      ↓
Merge + deduplicate by SIREN
      ↓
France Travail API
  └── flag companies hiring ROME M1502, M1801, N1301 → pain score +1 per match
      ↓
Researcher agent
  └── LinkedIn company page + website enrichment
      ↓
Strategist → Copywriter → [Human approval] → Send
```

---

## ENV Keys Required

| Key | Source | Status |
|---|---|---|
| `FRANCE_TRAVAIL_CLIENT_ID` | francetravail.io dashboard | Access granted, fill in |
| `FRANCE_TRAVAIL_CLIENT_SECRET` | francetravail.io dashboard | Access granted, fill in |
| `FIRECRAWL_API_KEY` | firecrawl.dev | Needed for Aerospace Valley scrape + website enrichment |
| `ANTHROPIC_API_KEY` | console.anthropic.com | Needed for researcher/strategist agents |
| `COMPOSIO_API_KEY` + `COMPOSIO_LINKEDIN_URL` | composio.dev | LinkedIn enrichment (step 4, can defer) |

---

## Related

- [[../projects/sales-agent|Sales Agent]]
- [[target-verticals|Target Verticals]]
- [[../concepts/sales-playbook|Sales Playbook]]
