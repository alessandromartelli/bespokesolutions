# Bespoke Solutions

AI-native software company. 80%+ of code written by agentic AI.

---

## What We're Building

- AI agents for business workflows
- Dropshipping product research tooling (see [[../research/dropshipping-niches]])
- AI-native development infrastructure (this repo)

---

## Stack

| Layer | Choice |
|---|---|
| AI | Claude Opus 4.7 (Anthropic) |
| Agent framework | Claude Code + custom skills |
| Knowledge base | Obsidian + this wiki |
| Version control | GitHub |
| Backend | TBD |
| Frontend | TBD |

---

## How We Work

1. Every task starts with `/spec`
2. Every spec gets a `/plan`
3. Every plan gets built surgically
4. Every build gets verified (`lint + typecheck + test`)
5. Every ship goes through `/review` then `/ship`

Full workflow: [[../../docs/ai-workflow|AI Workflow]]

---

## Key Decisions

| Decision | Rationale | Date |
|---|---|---|
| Claude Opus 4.7 as default model | Best reasoning, adaptive thinking | 2026-05 |
| Obsidian as wiki/second brain | Markdown-native, graph view, Claude writes .md directly | 2026-05 |
| Karpathy LLM Wiki pattern | Knowledge compounds across sessions instead of RAG | 2026-05 |

---

## Related

- [[../concepts/ai-native-development|AI-Native Development]]
- [[../concepts/agent-architecture|Agent Architecture]]
