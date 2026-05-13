# /wiki

Research a topic and add it to the wiki, or maintain the wiki's health.

## Usage

```
/wiki <topic>
/wiki process-inbox
/wiki update-index
/wiki lint
```

---

## Commands

### /wiki \<topic\>

1. Search for existing wiki pages on the topic (`wiki/` folder)
2. If a page exists — read it, then research what's new or missing and update it
3. If no page exists — determine the right subfolder (`concepts/`, `projects/`, `research/`) and create it
4. Use web search if the topic requires current information
5. Write following the wiki page conventions in CLAUDE.md:
   - Lowercase hyphenated filename
   - H1 title
   - Obsidian wiki links for cross-references
   - `## Related` section at the bottom
6. Update `wiki/index.md` to include the new/updated page
7. Update `HOME.md` Recent Entries if it's a new page
8. Update `CONTEXT.md` wiki map section

---

### /wiki process-inbox

1. Read every file in `inbox/` (skip `README.md` and `prospects-*`, `research-*`, `strategy-*`, `outreach-*` — those belong to the sales pipeline)
2. For each file, determine: is this a concept, project update, or research finding?
3. Integrate the content into the appropriate wiki page (create if needed)
4. Delete the processed inbox file
5. Update `wiki/index.md` and `CONTEXT.md`

---

### /wiki update-index

Regenerate `wiki/index.md` by scanning all `.md` files under `wiki/` and rebuilding the table of contents grouped by subfolder.

---

### /wiki lint

Health check on the wiki. Find and report:

1. **Broken links** — `[[page-name]]` references where the target file doesn't exist
2. **Orphan pages** — wiki pages that nothing links to
3. **Empty sections** — headings with no content below them
4. **Stale placeholders** — pages with "TBD", "TODO", "—" in tables that should have data
5. **Missing Related section** — pages that don't have a `## Related` block
6. **CONTEXT.md drift** — items in CONTEXT.md that no longer match actual file state

Output a report grouped by issue type. For each issue: file path, line number if applicable, and suggested fix.

After reporting, ask: "Fix automatically?" For safe fixes (adding missing Related sections, updating index), fix inline. For destructive fixes (removing pages), ask first.

---

## Rules

- Never summarize — synthesize. Extract the durable insight, not the raw content.
- Cross-link aggressively. Every new page should link to at least one existing page.
- If unsure which subfolder, use `concepts/`.
- Do not add timestamps to page content. Git tracks when.
- After any wiki write, always update `CONTEXT.md` and `wiki/index.md`.
