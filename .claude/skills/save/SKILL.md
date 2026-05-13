---
name: save
description: Save durable knowledge from the current conversation to the wiki and update CONTEXT.md after decisions, findings, or new understanding.
version: 1.0.0
author: Bespoke Solutions
license: proprietary
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [save, memory, wiki, knowledge-capture, karpathy]
    related_skills: [wiki, ingest]
---

# Save

Save durable knowledge from the current conversation to the wiki and update `CONTEXT.md`.

## Hermes Invocation

Load this skill when the user asks to save, preserve, remember in the wiki, update context, capture decisions, or end a session that produced durable knowledge.

Input is an optional title supplied by the user. If no title is provided, infer the best title from the conversation. If the user writes Claude-style syntax such as `/save <title>`, treat it as a normal instruction.

## Behavior

1. Review the current conversation and identify durable knowledge:
   - decisions made
   - concepts explained or clarified
   - research found
   - problems solved
   - patterns that worked or did not work
2. If a title is provided, use it. Otherwise infer the best title from the conversation.
3. Determine the right wiki subfolder:
   - New concept or explanation → `wiki/concepts/`
   - Project decision or update → `wiki/projects/`
   - Research findings → `wiki/research/`
4. Check whether a relevant page already exists. If yes, integrate into it. If no, create a new page.
5. Write only what would be useful to a future reader: conclusions, decisions, rationale, and reusable context, not the back-and-forth.
6. Add a `## Related` section linking to connected pages.
7. Update `wiki/index.md` if a new page was created.
8. Update `HOME.md` Recent Entries if a new page was created.
9. Update `CONTEXT.md`:
   - Active Work table
   - Key Decisions Made
   - outdated status entries
   - wiki map if relevant

## What to Save vs Skip

Save:
- Decisions and rationale
- Concepts that were explained or clarified
- Research findings
- Patterns that worked or did not work
- Anything useful at the start of the next session

Skip:
- Debugging back-and-forth that led nowhere
- Temporary context that will not matter next session
- Things already well-documented in the wiki with no new information
- Secrets, credentials, or private tokens

## Safety

Before changing multiple wiki/context files, keep the edits scoped and preserve existing useful content. Do not delete inbox or wiki files as part of save unless the user explicitly requested that cleanup.

## After Saving

Confirm:
- Which wiki page was created or updated
- What was added to `CONTEXT.md`
- Whether `wiki/index.md` was updated
