---
name: sales
description: Master orchestrator for the Bespoke Solutions sales pipeline. Use for prospecting, research, strategy, copywriting, pipeline review, and outcome capture.
version: 1.0.0
author: Bespoke Solutions
license: proprietary
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [sales, outreach, prospecting, sme, b2b, pipeline]
    related_skills: [wiki, save, ingest]
---

# Sales

Master orchestrator for the Bespoke Solutions sales pipeline. Runs the full prospecting-to-outreach workflow.

## Hermes Invocation

Load this skill when the user asks for sales prospecting, prospect research, outreach strategy, outreach copy, pipeline review, or outcome capture.

If the user writes Claude-style syntax such as `/sales prospect ...`, treat it as a normal instruction, not as a native Hermes slash command.

Supported intents:
- `sales prospect <criteria>`
- `sales research <business-name-or-url>`
- `sales strategize <business-slug>`
- `sales draft <business-slug>`
- `sales review`
- `sales pipeline`
- `sales close <business-slug> <outcome>`

## Commands

### Prospect: `sales prospect <criteria>`

Find new leads matching the criteria.

Examples:
```
sales prospect "restaurants in Milan"
sales prospect "law firms in London under 20 people"
sales prospect "e-commerce stores in Spain with outdated websites"
```

Perform the sales-prospector role directly or via Hermes `delegate_task`: find qualified leads, capture evidence, and save output to `inbox/prospects-<date>.md`.

After running: open the file in Obsidian, review the leads, delete any that are not right, then run `sales research` on the ones worth pursuing.

### Research: `sales research <business-name-or-url>`

Deep-dive one prospect and build their full profile.

Examples:
```
sales research "Trattoria da Mario, Milan"
sales research https://example-restaurant.com
```

Perform the sales-researcher role directly or via Hermes `delegate_task`. Save output to `inbox/research-<slug>.md`.

After running: review the research file. If the pain score is below 5/15, skip this prospect. If above 5, run `sales strategize`.

### Strategize: `sales strategize <business-slug>`

Build the outreach strategy for a researched prospect.

Read `inbox/research-<slug>.md` and perform the sales-strategist role directly or via Hermes `delegate_task`. Save output to `inbox/strategy-<slug>.md`.

After running: review the strategy. Check the channel, angle, and hook. Edit if needed. Then run `sales draft`.

### Draft: `sales draft <business-slug>`

Write the full 4-touch outreach sequence for a prospect.

Read `inbox/research-<slug>.md` and `inbox/strategy-<slug>.md`; perform the sales-copywriter role directly or via Hermes `delegate_task`. Save output to `inbox/outreach-<slug>.md`.

After running: this is the approval gate. Open the outreach file in Obsidian. Read every message. Edit anything that does not sound right. Check the box `**Approved**: [x]` only when ready to send manually.

### Review: `sales review`

Show all outreach files in `inbox/` that have not been approved yet.

List every `outreach-*.md` where `**Approved**: [ ]` is unchecked. Remind the user to review before sending.

### Pipeline: `sales pipeline`

Show the full pipeline status: what stage every prospect is at.

Read all `inbox/` files and produce a status table:

| Business | Research | Strategy | Outreach | Approved | Sent |
|---|---|---|---|---|---|
| Example Co | ✓ | ✓ | ✓ | ✓ | Touch 2 |
| Another Co | ✓ | ✓ | — | — | — |

### Close: `sales close <business-slug> <outcome>`

Record the outcome of a prospect and feed it back into the wiki.

Outcomes: `won`, `lost`, `ghosted`, `not-now`.

Examples:
```
sales close trattoria-mario won
sales close law-firm-smith ghosted
```

This command:
1. Reads `inbox/outreach-<slug>.md` and `inbox/strategy-<slug>.md`.
2. Extracts vertical, channel used, angle used, touches sent, and outcome.
3. Appends a row to the "What We're Learning" table in `wiki/concepts/sales-playbook.md`.
4. Updates `CONTEXT.md` with the latest pipeline status.
5. Archives the inbox files to `wiki/research/prospects/<slug>.md` after confirming the archive content is complete.
6. Uses the `save` skill procedure to preserve durable learning.

This is mandatory after every prospect is resolved. The wiki only gets smarter if outcomes go back in.

## Full Workflow

```
1. sales prospect "criteria"
   → Review inbox/prospects-*.md in Obsidian
   → Delete leads you do not want

2. sales research "business name"
   → Review inbox/research-*.md
   → Skip if pain score < 5

3. sales strategize "slug"
   → Review inbox/strategy-*.md
   → Edit hook and angle if needed

4. sales draft "slug"
   → Review inbox/outreach-*.md in Obsidian
   → Edit messages, check the Approved box

5. Send manually via email/LinkedIn/WhatsApp
   → Mark sent date in the outreach file
   → Follow up on schedule

6. sales close "slug" "outcome"
   → Archive learning into the wiki
```

## Rules

- Nothing sends automatically. Every outreach file requires human approval before use.
- One prospect at a time through research → strategy → draft. Do not batch research 20 prospects and then lose provenance.
- Always close prospects when a deal is won, lost, or goes cold. The wiki learns from every outcome.
- The wiki is the brain. The strategist reads `wiki/concepts/sales-playbook.md`. Keep it current after every 5 prospects.
- Before deleting or archiving inbox files, confirm the useful information has been preserved.
