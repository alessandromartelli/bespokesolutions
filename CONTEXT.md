# Current Context — Bespoke Solutions

> Injected at session start. Keep under 60 lines. Update via `/save`.

---

## What This Repo Is

Bespoke Solutions — AI-native agency selling **"AI Employees as a Service"** to SMEs and executives. €4-8K/month per customer.

This repo is simultaneously:
- The **codebase** (agents, skills, scripts)
- The **knowledge base** (Obsidian wiki, Karpathy LLM Wiki pattern)
- The **sales system** (prospecting pipeline, outreach sequences)

---

## Strategic Positioning

**Product**: Fully managed AI employees for executives. Customer never touches tokens, models, or infrastructure.

**Stack**: Hermes Agent + Orgo (per-customer compute) + Composio (tool connector) + Agent Mail + Obsidian + GPT 5.5 / Opus 4.7

**Differentiator**: Enterprise quality at SME prices. White-labelable.

**Target verticals (Tier 1)**: Law firms, marketing agencies, insurance, manufacturers, wholesalers, real estate. **Avoid**: healthcare, finance (regulatory).

**Moat**: Vertical-specific skill packs Bespoke builds and improves over time.

---

## Founding Team

- Othmane Atif — CEO
- Noel Demko — COO
- Daniel Demko — CTO
- Amir Czuri — CIO
- Alessandro Martelli — CFO

---

## Active Work

| Area | Status | Next action |
|---|---|---|
| White paper | v1 at `docs/whitepaper.md` | Fill contact placeholders, export to PDF |
| Sales pipeline | Built + cleaned | Phase 2 stack signups, then `/sales prospect` |
| Brand assets | Defined per wiki | Polish LinkedIn profiles + one-liner test |
| Stack signups | Hermes ✓, OpenAI ✓, Agent Mail ✓, Composio ✓. Orgo deferred. | Run `scripts/setup-mcps.sh` to wire MCPs |
| MCP wiring | Scaffolding ready in `.claude/settings.local.json.example` | Populate `.env`, then run setup script |
| First skill pack | Not started | Pick first vertical, build pack |
| GitHub PR #1 | Pushed for review | Merge via GitHub app |

---

## Wiki Map

```
wiki/concepts/   ai-native-development, agent-architecture,
                 agent-business-playbook (CORE), sales-playbook
wiki/projects/   bespoke-solutions, sales-agent, brand-assets
wiki/research/   target-verticals, dropshipping-niches (demo only)
```

---

## Skills (Hermes/agentskills.io compatible)

`.claude/skills/`: spec, plan, review, ship, code-simplify, fix-issue (dev workflow)
+ wiki, save, ingest (knowledge maintenance)
+ sales (outreach pipeline)

All have YAML frontmatter with Hermes metadata.

---

## Key Decisions

| Decision | Rationale |
|---|---|
| Sell "AI Employees" at €4-8K/mo | Recurring revenue, customer stickiness |
| Hermes harness (not OpenClaw) | Reliable, supports higher price tier |
| Orgo per-customer compute | Sandboxed, scalable, one workspace per client |
| Skills > custom agents | Anthropic's emerging standard; composable |
| Karpathy LLM Wiki | Knowledge compounds across sessions |
| Skip healthcare/finance | Regulatory burden too high for early stage |

---

## How to Update This File

Run `/save` after any session that changes active work or decisions.
