---
name: ingest
description: Feed a URL or file to the agent and integrate the extracted knowledge into the wiki. Used to grow the knowledge base from external sources.
version: 1.0.0
author: Bespoke Solutions
license: proprietary
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ingest, wiki, knowledge-base, research, karpathy]
    related_skills: [wiki, save]
---

# Ingest

Feed a URL or file to the agent and integrate the extracted durable knowledge into the wiki.

## Hermes Invocation

Load this skill when the user asks to ingest, import, process, summarize into the wiki, or add knowledge from a URL/file.

Input is a URL or file path supplied by the user. If the user writes Claude-style syntax such as `/ingest <url>`, treat it as a normal instruction.

## Behavior

1. Fetch and read the content at the URL or file path.
2. Extract durable knowledge: key concepts, findings, decisions, examples, and data points.
3. Discard navigation, ads, boilerplate, repetition, and non-durable detail.
4. Determine which wiki page(s) this content belongs to:
   - Existing topic page → integrate into it.
   - Distinct new concept → create `wiki/concepts/<slug>.md`.
   - Research data → create or update `wiki/research/<slug>.md`.
5. Write with wiki page conventions from `CLAUDE.md`/project docs:
   - lowercase hyphenated filename
   - H1 title
   - Obsidian wiki links for cross-references
   - `## Related` section
6. Cross-link to related pages.
7. Update `wiki/index.md` if a new page was created.
8. Update `HOME.md` Recent Entries if a new page was created.
9. Update `CONTEXT.md` if the wiki map or active understanding changed.

## Synthesis Rules

- Synthesize rather than summarize; extract durable insight.
- One paragraph max per key point; if it needs more, break it into subheadings.
- Quote sparingly; paraphrase and synthesize instead.
- Always answer: "why does this matter for Bespoke Solutions?"
- Link the source at the bottom under `## Sources`.

## Safety

Do not overwrite existing wiki pages wholesale. Integrate new knowledge into the appropriate section and preserve existing useful context.
