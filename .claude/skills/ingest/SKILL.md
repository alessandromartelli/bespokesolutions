---
name: ingest
description: Feed a URL or file to the agent and integrate the extracted knowledge into the wiki. Used to grow the knowledge base from external sources (articles, papers, docs).
version: 1.0.0
author: Bespoke Solutions
license: proprietary
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: ingest, wiki, knowledge-base, research, karpathy
---

# /ingest

Feed Claude a URL or file and integrate it into the wiki.

## Usage

```
/ingest <url>
/ingest <file-path>
```

## Behavior

1. Fetch and read the content at the URL or file path
2. Extract the durable knowledge — key concepts, findings, decisions, data points
3. Discard: navigation, ads, boilerplate, repetition
4. Determine which wiki page(s) this content belongs to:
   - Does a page already exist on this topic? → integrate into it
   - Is this a distinct new concept? → create `wiki/concepts/<slug>.md`
   - Is this research data? → create or update `wiki/research/<slug>.md`
5. Write with wiki page conventions (see CLAUDE.md Wiki Schema section)
6. Cross-link to related pages
7. Update `wiki/index.md` if a new page was created
8. Update `HOME.md` Recent Entries for new pages

## Synthesis rules

- One paragraph max per key point — if it needs more, break it into subheadings
- Quote sparingly — paraphrase and synthesize instead
- Always answer: "why does this matter for Bespoke Solutions?"
- Link the source at the bottom under `## Sources`
