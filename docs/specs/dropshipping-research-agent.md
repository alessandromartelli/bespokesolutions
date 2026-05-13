# Dropshipping Product Research Agent

## Goal
An agent that autonomously discovers trending niches, researches products within them, scores each product on trend velocity and competitor ad spend, and outputs a validated shortlist as a JSON file — run manually on demand.

## Background
Manually finding winning dropshipping products is slow and inconsistent. This agent replaces the weekly manual research loop: finding niches, checking TikTok/Google trends, monitoring competitor ad libraries, and scanning marketplace best-sellers. The output is a structured JSON file ready to be fed into a downstream decision or publishing workflow.

## Success Criteria
- [ ] Agent discovers at least 3 niches per run without any manual input
- [ ] For each niche, agent produces a list of products that cleared the score threshold
- [ ] Each product record includes: name, niche, trend_score, ad_spend_score, composite_score, source_urls, summary
- [ ] Output written to `output/research_<YYYY-MM-DD>.json`
- [ ] Run completes in under 10 minutes on a standard laptop
- [ ] Agent gracefully handles rate limits and missing data (no crashes, logs warnings)
- [ ] All data sourced from free/public sources in v1 (Google Trends, TikTok public search, Meta Ad Library)

## Scope

### In Scope
- Auto-discovery of trending niches (via Google Trends, TikTok trending)
- Product research per niche: trend velocity scoring (Google Trends + TikTok views)
- Competitor validation: Meta Ad Library scrape for active ads on discovered products
- Scoring engine: weighted composite score (trend velocity + ad spend signals)
- Score threshold filter — only products above threshold make the output
- Structured JSON output: one file per run, timestamped
- CLI entry point: `python run.py` (no arguments required for a standard run)
- Logging to stdout with run summary at the end

### Out of Scope
- Automated scheduling / cron (manual trigger only in v1)
- Publishing output to Notion, Sheets, Slack, or any external service
- Paid data sources (Apify, Jungle Scout, SimilarWeb) — pluggable in v2
- Supplier lookup, margin calculation, or fulfilment data
- UI of any kind
- Multi-user or API server mode

## Behaviour

### Standard run
```
python run.py
```
1. **Niche discovery** — agent queries Google Trends and TikTok public search to identify 3–5 niches with accelerating search/view velocity in the past 7 days. Logs discovered niches.
2. **Product research** — for each niche, agent finds candidate products by scraping TikTok search results and Google Shopping trending items. Collects product name, estimated views/search volume, and source URLs.
3. **Competitor validation** — for each candidate product, checks Meta Ad Library for active ads. Records number of active ads and estimated advertiser count as a proxy for competitor ad spend.
4. **Scoring** — each product receives:
   - `trend_score` (0–100): based on search/view growth velocity
   - `ad_spend_score` (0–100): based on active ad count and unique advertiser count in Meta Ad Library
   - `composite_score`: weighted average (trend 60%, ad spend 40%)
5. **Threshold filter** — products with `composite_score` below the configured threshold (default: 60) are dropped.
6. **Output** — surviving products written to `output/research_<YYYY-MM-DD>.json`. Run summary printed to stdout.

### Output format
```json
{
  "run_date": "2026-05-13",
  "niches_discovered": ["pet accessories", "kitchen gadgets", "home lighting"],
  "products": [
    {
      "name": "Automatic Pet Feeder",
      "niche": "pet accessories",
      "trend_score": 82,
      "ad_spend_score": 74,
      "composite_score": 79,
      "active_ads": 43,
      "unique_advertisers": 12,
      "source_urls": ["https://...", "https://..."],
      "summary": "High TikTok view growth (+340% WoW), 43 active Meta ads across 12 advertisers."
    }
  ],
  "products_evaluated": 38,
  "products_above_threshold": 7
}
```

### Edge cases
- **No products clear threshold**: output file still written with empty `products` array and a log warning
- **Rate limited by a source**: agent logs the warning, skips that source for the current niche, continues with remaining sources
- **TikTok/Meta structure changes (scrape breaks)**: agent logs an error for that source, continues with remaining signals, notes degraded scoring in output
- **Duplicate products across niches**: deduped by product name, highest composite_score record kept

## Technical Notes

- **Language**: Python 3.11+
- **LLM**: Anthropic Claude API (claude-sonnet-4-6) for niche discovery reasoning and product summary generation
- **Scraping**: `playwright` (headless) for TikTok and Meta Ad Library; `pytrends` for Google Trends
- **HTTP**: `httpx` for any direct API calls
- **Config**: `config.py` with `SCORE_THRESHOLD`, `MAX_NICHES`, `MAX_PRODUCTS_PER_NICHE`, `ANTHROPIC_API_KEY` (from env)
- **Output directory**: `output/` (gitignored)
- **Structure**:
  ```
  agents/
    dropshipping_researcher/
      __init__.py
      run.py              ← entry point
      discoverer.py       ← niche discovery
      researcher.py       ← product research per niche
      scorer.py           ← scoring engine
      sources/
        google_trends.py
        tiktok.py
        meta_ads.py
      config.py
      output/             ← gitignored
  requirements.txt
  ```
- **Prompt caching**: use Anthropic prompt caching on the system prompt for the summary generation step (reduces cost on repeated runs)
- **Tests**: unit tests for `scorer.py` (pure functions, easy to test); integration tests mocked

## Open Questions
- Should the Meta Ad Library scraper use Playwright or is there a public API endpoint we can hit directly? (Playwright is the safe fallback but slower)
- What threshold makes sense for v1 — 60 is a guess. Should be tunable after first run.
- Should `run.py` accept an optional `--niche` flag to override auto-discovery for manual targeted runs?
