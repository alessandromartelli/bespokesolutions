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

## Strategic Positioning (NEW)

**Product**: Fully managed AI employees for executives. Customer never touches tokens, models, or infrastructure.

**Stack**: Hermes Agent + Orgo (cloud computers) + Composio (tool connector) + Agent Mail + Obsidian + GPT 5.5 / Opus 4.7

**Differentiator**: Enterprise quality at SME pricing. White-labelable.

**Target verticals**: Law firms, marketing agencies, insurance, manufacturers, wholesalers, real estate. Avoid healthcare/finance (regulatory).

**Moat**: Vertical-specific skill packs Bespoke builds and improves over time.

---

## Founding Team

- Alessandro Martelli — CFO
- Noel Demko — COO
- Othmane Atif — CEO
- Daniel Demko — CTO
- Amir Czuri — CIO

---

## Active Work

| Area | Status | Next action |
|---|---|---|
| White paper | Drafted v1 at `docs/whitepaper.md` | Review, iterate, export to PDF |
| Sales pipeline | Built, not yet run | Brand assets first, then `/sales prospect` |
| Brand assets | Defined | See `wiki/projects/brand-assets.md` |
| Hermes integration | Researched — open to forking | Decide: fork vs install vs full custom |
| First skill pack | Not started | Build one vertical pack as proof |

---

## Wiki Map

```
wiki/concepts/   ai-native-development, agent-architecture,
                 agent-business-playbook (CORE STRATEGY), sales-playbook
wiki/projects/   bespoke-solutions, sales-agent, brand-assets
wiki/research/   dropshipping-niches, target-verticals
```

---

## Key Decisions

| Decision | Rationale |
|---|---|
| Sell "AI employees" at €4-8K/mo, not project-based | Recurring revenue, customer dependency = stickiness |
| Hermes harness (not OpenClaw) | Higher price point, self-evolving, more reliable |
| Orgo for per-customer compute | Sandboxed, scalable, manageable from one pane |
| Skills > custom agents | Anthropic's emerging standard; compounds; composable |
| Multi-agent sales pipeline with human approval gate | Safety + quality before scale |
| Karpathy LLM Wiki pattern | Knowledge compounds across sessions |
| Obsidian as vault front-end | Markdown-native, graph view, local |

---

## How to Update This File

Run `/save` after any session that changes active work or decisions.
