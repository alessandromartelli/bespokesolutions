# AI-Native Development

> Software 3.0: humans direct agents toward verifiable goals; agents write the code.

---

## Core Idea

Traditional development: human writes code, AI assists.
AI-native: AI writes code, human reviews diffs and sets goals.

The human role shifts to:
1. Define clear success criteria
2. Review diffs, not prose
3. Catch surgical violations and over-engineering
4. Maintain CLAUDE.md as the team's shared memory

---

## Karpathy's 4 Rules

The four failure modes agents hit most often, and their fixes:

| Failure | Rule |
|---|---|
| Agent guesses instead of asking | Think before coding — state assumptions, ask when ambiguous |
| Agent over-engineers | Simplicity first — minimum code that solves the problem |
| Agent touches too much | Surgical changes — only what the task requires |
| Agent reports done prematurely | Goal-driven — loop until verifiable criteria are met |

---

## The Stack

```
System prompt + CLAUDE.md + Skills + Tools + LLM
```

- **LLM** — reasoning and language (Claude Opus 4.7)
- **System prompt** — persona and constraints
- **CLAUDE.md** — project-specific context loaded at session start
- **Skills** — reusable procedural knowledge (`/spec`, `/plan`, `/wiki`)
- **Tools** — actions the agent can take (bash, file read/write, web search)

---

## Related

- [[agent-architecture|Agent Architecture]]
- [[../projects/bespoke-solutions|Bespoke Solutions]]
