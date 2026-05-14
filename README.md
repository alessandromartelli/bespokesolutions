# Bespoke Solutions

AI Employees as a Service for SMEs and executives. €4–8K/month per customer.

We build and manage fully managed AI employees so executives can reclaim their time — without touching tokens, models, or infrastructure.

---

## What's In This Repo

This repo is simultaneously the codebase, the knowledge base, and the sales system.

| Folder | Purpose |
|---|---|
| `wiki/` | Company knowledge base (Karpathy LLM Wiki pattern) |
| `.claude/skills/` | Skills for Claude Code (dev workflow + sales + knowledge) |
| `agents/` | Production agents; `agents/examples/` for reference scripts |
| `scripts/` | Setup and automation |
| `docs/` | White paper, specs, workflow docs |

---

## Getting Started (New Team Member)

```bash
git clone git@github.com:alessandromartelli/bespokesolutions.git
cd bespokesolutions
bash scripts/setup.sh
```

The setup script will:
1. Create `.env` from `.env.example` — **fill in your keys**
2. Create `CLAUDE.local.md` for personal Claude overrides
3. Install the MCP stack (Hermes, Composio, Memory, GitHub) into Claude Code

Then open Claude Code:
```bash
claude
```

---

## The Stack

| Layer | Tool |
|---|---|
| AI harness | Hermes Agent (VPS) |
| Tool connector | Composio (Gmail, Calendar, LinkedIn, Slack, Notion, 1000+ apps) |
| Agent identity | Agent Mail (one email per AI Employee) |
| Customer compute | Orgo (one sandboxed VM per customer) |
| Default model | GPT 5.5 (inside Hermes) |
| Builder | Claude Code + Opus 4.7 |

---

## Target Verticals

Law firms · Marketing agencies · Insurance agencies · Manufacturers · Wholesalers · Real estate

---

## Founding Team

Othmane Atif (CEO) · Noel Demko (COO) · Daniel Demko (CTO) · Amir Czuri (CIO) · Alessandro Martelli (CFO)

---

## Key Docs

- [`wiki/concepts/agent-business-playbook.md`](wiki/concepts/agent-business-playbook.md) — full operating model
- [`wiki/concepts/sales-playbook.md`](wiki/concepts/sales-playbook.md) — how we sell
- [`docs/whitepaper.md`](docs/whitepaper.md) — client-facing white paper
- [`docs/ai-workflow.md`](docs/ai-workflow.md) — how the team uses Claude Code
