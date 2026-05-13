---
name: sales
description: Master orchestrator for the Bespoke Solutions sales pipeline. Run prospecting, deep research, strategy, copywriting, and outcome capture for the multi-agent outreach workflow.
version: 1.0.0
author: Bespoke Solutions
license: proprietary
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: sales, outreach, prospecting, SME, B2B, pipeline
---

# /sales

Master orchestrator for the Bespoke Solutions sales pipeline. Runs the full prospecting-to-outreach workflow.

## Usage

```
/sales prospect <criteria>
/sales research <business-name-or-url>
/sales strategize <business-slug>
/sales draft <business-slug>
/sales review
/sales pipeline
```

---

## Commands

### /sales prospect \<criteria\>

Find new leads matching the criteria.

**Examples:**
```
/sales prospect "restaurants in Milan"
/sales prospect "law firms in London under 20 people"
/sales prospect "e-commerce stores in Spain with outdated websites"
```

Runs the `sales-prospector` agent. Output saved to `inbox/prospects-<date>.md`.

After running: open the file in Obsidian, review the leads, delete any that aren't right, then run `/sales research` on the ones you want to pursue.

---

### /sales research \<business-name-or-url\>

Deep-dive one prospect and build their full profile.

**Examples:**
```
/sales research "Trattoria da Mario, Milan"
/sales research https://example-restaurant.com
```

Runs the `sales-researcher` agent. Output saved to `inbox/research-<slug>.md`.

After running: review the research file. If the pain score is below 5/15, skip this prospect. If above 5, run `/sales strategize`.

---

### /sales strategize \<business-slug\>

Build the outreach strategy for a researched prospect.

Reads `inbox/research-<slug>.md` and runs the `sales-strategist` agent.
Output saved to `inbox/strategy-<slug>.md`.

After running: review the strategy. Check the channel, angle, and hook. Edit if needed. Then run `/sales draft`.

---

### /sales draft \<business-slug\>

Write the full 4-touch outreach sequence for a prospect.

Reads `inbox/research-<slug>.md` and `inbox/strategy-<slug>.md` and runs the `sales-copywriter` agent.
Output saved to `inbox/outreach-<slug>.md`.

After running: **this is your approval gate.** Open the outreach file in Obsidian. Read every message. Edit anything that doesn't sound right. Check the box `**Approved**: [x]` when ready to send.

---

### /sales review

Show all outreach files in `inbox/` that have not been approved yet.

Lists every `outreach-*.md` where `**Approved**: [ ]` (unchecked). Reminds you to review before sending.

---

### /sales pipeline

Show the full pipeline status — what stage every prospect is at.

Reads all `inbox/` files and produces a status table:

| Business | Research | Strategy | Outreach | Approved | Sent |
|---|---|---|---|---|---|
| Example Co | ✓ | ✓ | ✓ | ✓ | Touch 2 |
| Another Co | ✓ | ✓ | — | — | — |

---

## Full workflow

```
1. /sales prospect "criteria"
   → Review inbox/prospects-*.md in Obsidian
   → Delete leads you don't want

2. /sales research "business name"
   → Review inbox/research-*.md
   → Skip if pain score < 5

3. /sales strategize "slug"
   → Review inbox/strategy-*.md
   → Edit hook and angle if needed

4. /sales draft "slug"
   → Review inbox/outreach-*.md in Obsidian
   → Edit messages, check the Approved box

5. Send manually via email/LinkedIn/WhatsApp
   → Mark sent date in the outreach file
   → Follow up on schedule
```

---

---

### /sales close \<business-slug\> \<outcome\>

Record the outcome of a prospect and feed it back into the wiki.

**Outcomes:** `won`, `lost`, `ghosted`, `not-now`

```
/sales close trattoria-mario won
/sales close law-firm-smith ghosted
```

This command:
1. Reads `inbox/outreach-<slug>.md` and `inbox/strategy-<slug>.md`
2. Extracts: vertical, channel used, angle used, touches sent, outcome
3. Appends a row to the "What We're Learning" table in `wiki/concepts/sales-playbook.md`
4. Updates `CONTEXT.md` with the latest pipeline status
5. Archives the inbox files to `wiki/research/prospects/<slug>.md`
6. Runs `/save` to commit the knowledge

**This is mandatory after every prospect is resolved.** The wiki only gets smarter if outcomes go back in.

---

## Rules

- **Nothing sends automatically.** Every outreach file requires human approval before use.
- **One prospect at a time** through research → strategy → draft. Don't batch research 20 prospects and then wonder which strategy was for whom.
- **Always close prospects.** Run `/sales close` when a deal is won, lost, or goes cold. The wiki learns from every outcome.
- **The wiki is the brain.** The strategist reads `wiki/concepts/sales-playbook.md`. Keep it current — update it after every 5 prospects with what you're learning.
