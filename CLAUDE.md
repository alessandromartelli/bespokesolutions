# Bespoke Solutions — Claude Code Guidelines

> AI-native company. 80%+ of code is written by agentic AI.
> These rules encode hard-won lessons about where agents fail.

---

## Behavioral Principles (Karpathy's 4 Rules)

### 1. Think Before Coding
State your assumptions explicitly before writing a single line.
If multiple interpretations exist, **present them and ask** — never silently pick one.
If a simpler approach exists, say so and push back.
If you are confused, name what is unclear and stop.

### 2. Simplicity First
Write the minimum code that solves the problem. Nothing speculative.
No unrequested abstractions, no premature generalization, no future-proofing.
Test: would a senior engineer call this overcomplicated? If yes, simplify.

### 3. Surgical Changes — IMPORTANT
Touch ONLY what the task requires.
- Do not reformat adjacent code
- Do not refactor unrelated functions
- Do not remove comments or code your change didn't render unnecessary
- Do not change whitespace, imports, or style outside your diff

### 4. Goal-Driven Execution — YOU MUST follow this
Transform every task into explicit, verifiable success criteria.
Loop until those criteria are met. Do not report done until verified.
Example: "tests pass", "linter shows 0 errors", "screenshot matches design".

---

## Development Workflow

Follow these phases in order. Do not skip ahead.

1. **Explore** — read relevant files, understand the system, form hypotheses (plan mode)
2. **Plan** — write a concrete implementation plan before touching code (plan mode)
3. **Build** — implement against the plan, one logical unit at a time
4. **Verify** — run tests, linter, type checker; check all success criteria
5. **Review** — check your own diff for surgical violations and over-engineering
6. **Ship** — commit with a descriptive message, open PR

Use `/spec`, `/plan`, `/fix-issue`, `/review`, `/code-simplify`, `/ship` for structured workflows.

---

## Repository Conventions

**Branches**: `feat/<slug>`, `fix/<slug>`, `chore/<slug>`, `claude/<task-slug>`
**Commits**: imperative mood, ≤72 chars subject, explain WHY not WHAT
**PRs**: must include Summary, Test Plan, and link to issue/spec
**Never** commit `.env`, secrets, or credentials

---

## Build, Test, Lint

> Update these commands when the stack is decided.

```bash
# Install
npm install            # or: pip install -r requirements.txt / poetry install

# Test
npm test               # run unit tests
npm run test:e2e       # run end-to-end tests

# Lint & type-check
npm run lint           # ESLint / Ruff / etc.
npm run typecheck      # tsc --noEmit / mypy

# Build
npm run build
```

IMPORTANT: Always run lint + typecheck after making changes. Fix all errors before reporting done.

---

## Code Style

- Prefer explicit over implicit
- No magic numbers — name constants
- Functions do one thing
- Error handling only at system boundaries (user input, external APIs)
- No comments explaining WHAT — only WHY (hidden constraints, non-obvious invariants)
- Tests live next to the code they test

---

## Environment

Copy `.env.example` to `.env` and fill in values. Never commit `.env`.
See `docs/ai-workflow.md` for how we use Claude Code as a team.

---

## Context Management

- `/clear` between unrelated tasks
- Use subagents for deep codebase exploration (keeps main context clean)
- Use `/compact` when context gets heavy mid-task
- If you correct Claude twice on the same mistake: `/clear` and re-prompt with what you learned
