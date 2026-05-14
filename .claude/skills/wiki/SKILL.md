---
name: wiki
description: Research a topic and add it to the wiki, process the inbox into wiki pages, regenerate the index, or run a wiki health lint.
version: 1.0.0
author: Bespoke Solutions
license: proprietary
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [wiki, knowledge-base, obsidian, research, karpathy]
    related_skills: [save, ingest]
---

# Wiki

Research a topic and add it to the wiki, process the inbox into wiki pages, regenerate the index, or run a wiki health lint.

## Hermes Invocation

Load this skill when the user asks to update the wiki, research a topic into the knowledge base, process the inbox, update the wiki index, or lint wiki health.

If the user writes Claude-style syntax such as `/wiki <topic>`, `/wiki process-inbox`, `/wiki update-index`, or `/wiki lint`, treat it as a normal instruction.

## Commands

### Research or Update a Topic

1. Search for existing wiki pages on the topic under `wiki/`.
2. If a page exists, read it, then research what is new or missing and update it.
3. If no page exists, determine the right subfolder:
   - `concepts/`
   - `projects/`
   - `research/`
4. Use web search if the topic requires current information.
5. Write following the wiki page conventions in `CLAUDE.md`/project docs:
   - Lowercase hyphenated filename
   - H1 title
   - Obsidian wiki links for cross-references
   - `## Related` section at the bottom
6. Update `wiki/index.md` to include the new/updated page.
7. Update `HOME.md` Recent Entries if it is a new page.
8. Update `CONTEXT.md` wiki map section.

### Process Inbox

1. Read every file in `inbox/`.
2. Skip `README.md` and sales pipeline files: `prospects-*`, `research-*`, `strategy-*`, `outreach-*`.
3. For each file, determine whether it is a concept, project update, or research finding.
4. Integrate the content into the appropriate wiki page, creating one if needed.
5. Before deleting processed inbox files, confirm that the content has been integrated correctly.
6. Update `wiki/index.md` and `CONTEXT.md`.

### Update Index

Regenerate `wiki/index.md` by scanning all `.md` files under `wiki/` and rebuilding the table of contents grouped by subfolder.

### Lint

Health check on the wiki. Find and report:

1. Broken links: `[[page-name]]` references where the target file does not exist.
2. Orphan pages: wiki pages that nothing links to.
3. Empty sections: headings with no content below them.
4. Stale placeholders: pages with `TBD`, `TODO`, or `—` in tables that should have data.
5. Missing Related section: pages that do not have a `## Related` block.
6. `CONTEXT.md` drift: items in `CONTEXT.md` that no longer match actual file state.

Output a report grouped by issue type. For each issue include file path, line number if applicable, and suggested fix.

After reporting, ask whether to fix automatically. Safe fixes, such as adding missing Related sections or updating the index, may be fixed inline after approval. Destructive fixes, such as removing pages or deleting inbox files, require explicit approval.

## Rules

- Never summarize; synthesize. Extract durable insight, not raw content.
- Cross-link aggressively. Every new page should link to at least one existing page.
- If unsure which subfolder to use, use `concepts/`.
- Do not add timestamps to page content. Git tracks when.
- After any wiki write, always update `CONTEXT.md` and `wiki/index.md`.
- Preserve existing useful page content; integrate rather than overwrite.
