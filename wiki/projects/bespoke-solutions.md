# Bespoke Solutions

AI-native agency selling **fully-managed AI Employees** to SMEs and executives under one umbrella: **Intelligent Business Systems**.

---

## What We Sell

Not project work. Not deliverables. **AI Employees.**

Each customer gets one or more named digital employees with:
- Persistent memory (Obsidian vault per customer)
- Their own email (Agent Mail)
- Access to 1000+ tools (Composio)
- A sandboxed cloud computer (Orgo)
- A skill pack tailored to their vertical

**Pricing**: €4-8K/month per customer. Unlimited everything. 48-hour onboarding.

The customer never touches tokens, models, or infrastructure.

---

## The Founding Team

| Role | Name |
|---|---|
| CEO | Othmane Atif |
| COO | Noel Demko |
| CTO | Daniel Demko |
| CIO | Amir Czuri |
| CFO | Alessandro Martelli |

Remote-first, global from day one.

---

## Stack

| Layer | Tool | Why |
|---|---|---|
| Agent harness | **Hermes Agent** (NousResearch) | Self-evolving, reliable, supports €10K/mo tier |
| Compute | **Orgo** | One cloud computer per customer, isolated, manageable from one pane |
| Tool connector | **Composio** | One MCP → Gmail, Slack, Notion, Calendar, LinkedIn, etc. |
| Agent identity | **Agent Mail** | Each employee gets their own email — sends, receives, self-alerts |
| Memory layer | **Obsidian vault** (per customer) | Markdown second brain, persistent context |
| Build environment | **Claude Code** / **Codex** | Use agents to build customer agents |
| Default model | **GPT 5.5** | Tool-efficient, generous usage |
| Heavy reasoning | **Claude Opus 4.7** | Long coding tasks via Claude Code |
| Knowledge base (this repo) | **Karpathy LLM Wiki** in Obsidian | Compounds across sessions |

---

## How We Work

Internal workflow lives in [[../../docs/ai-workflow|AI Workflow]]. Short version:

1. **`/spec`** — define what we're building
2. **`/plan`** — architect before coding
3. **Build with agents** — 80%+ of code written by AI under human direction
4. **Verify** — lint, typecheck, test
5. **`/save`** — capture knowledge to the wiki

We use the same agentic stack internally that we sell to customers. Bespoke is its own first customer.

---

## Key Decisions

| Decision | Rationale |
|---|---|
| Sell "AI Employees" not project work | Recurring revenue, customer dependency = retention |
| €4-8K/mo subscription model | Unlimited iteration, customer never thinks about cost |
| Hermes as harness (not OpenClaw) | More reliable, allows higher price point |
| Karpathy LLM Wiki pattern | Knowledge compounds across sessions, beats RAG |
| Obsidian as vault front-end | Markdown-native, local-first, graph view |
| Skills > custom agents (per Anthropic) | Composable, progressive disclosure, future-proof |
| Skip healthcare/finance verticals | Regulatory burden too high for early stage |
| Target Tier 1 verticals first | Legacy + wants-to-be-AI-native + decision maker has budget |
| Multi-agent sales pipeline with human gate | Quality + safety before scaling outreach |

See [[../concepts/agent-business-playbook|Agent Business Playbook]] for the full operational framework.

---

## Active Products / Initiatives

- **Sales Pipeline** — multi-agent prospecting and outreach ([[sales-agent|Sales Agent]])
- **White Paper** — company positioning document (`docs/whitepaper.md`)
- **Brand Assets** — pre-outreach essentials ([[brand-assets|Brand Assets]])
- **First Vertical Skill Pack** — TBD, will be one of: law firms, marketing agencies, real estate

---

## Related

- [[../concepts/agent-business-playbook|Agent Business Playbook]]
- [[../concepts/ai-native-development|AI-Native Development]]
- [[../concepts/agent-architecture|Agent Architecture]]
- [[../concepts/sales-playbook|Sales Playbook]]
- [[sales-agent|Sales Agent]]
- [[brand-assets|Brand Assets]]
- [[../research/target-verticals|Target Verticals]]
