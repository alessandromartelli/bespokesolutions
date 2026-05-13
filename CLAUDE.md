# Bespoke Solutions — Claude Code Guidelines

> AI-native company. 80%+ of code is written by agentic AI.
> This file is law. Every rule here overrides default behavior.

---

## SESSION START — YOU MUST DO THIS FIRST

**At the start of EVERY session, before responding to anything:**

1. Read `HOME.md` — understand the current state of the project
2. Read `wiki/index.md` — know what knowledge already exists
3. Read any wiki pages relevant to the user's request before acting on it
4. If `CONTEXT.md` exists, read it — it contains the latest active work summary

**Do not skip this.** A response given without reading the wiki first is a guess. The wiki is the source of truth.

---

## WIKI-FIRST RULE — ALWAYS

This repo is an Obsidian vault following Karpathy's LLM Wiki pattern. The wiki is the memory. It compounds across sessions. Every session contributes to it.

**Before any task:**
- Check `wiki/` for existing knowledge on the topic
- If a relevant page exists, read it fully before proceeding
- If no page exists, that is a signal to create one after the task

**The wiki beats your training.** If `wiki/concepts/sales-playbook.md` says something different from what you'd default to, follow the wiki. It reflects what we've actually learned, not general knowledge.

**Agents read the wiki.** Every agent that makes decisions must read the relevant wiki page first. Logic lives in the wiki, not hardcoded in agent files. Agent files are executors; the wiki is the brain.

---

## TASK COMPLETION RITUAL — NEVER SKIP

**After completing any task that produces knowledge:**

1. Ask: "Did this session produce anything worth keeping?" 
2. If yes: run `/save` — save the key insight, decision, or finding to the wiki
3. If a new concept was discovered: create a wiki page for it
4. If an existing page needs updating: update it
5. Update `CONTEXT.md` with what changed

**What counts as worth keeping:**
- A decision and its rationale
- A pattern that worked or didn't
- Research findings
- New understanding of a concept
- Anything you'd want to know at the start of the next session

---

## BUILD GATE — NO EXCEPTIONS

**Before building, creating, or significantly modifying anything:**

1. Invoke the `brainstorming` skill — this is mandatory, not optional
2. Check the wiki for prior decisions on this topic
3. Get explicit approval on the approach before writing files
4. Only skip brainstorming if the task is purely mechanical (a single file edit, a rename, a typo fix)

**The moment you write a new file or design a system, brainstorming was required first.**

---

## Karpathy's 4 Behavioral Rules

### 1. Think Before Coding
State your assumptions explicitly before writing a single line.
If multiple interpretations exist, **present them and ask** — never silently pick one.
If a simpler approach exists, say so and push back.
If you are confused, name what is unclear and stop.

### 2. Simplicity First
Write the minimum code that solves the problem. Nothing speculative.
No unrequested abstractions, no premature generalization, no future-proofing.
Test: would a senior engineer call this overcomplicated? If yes, simplify.

### 3. Surgical Changes
Touch ONLY what the task requires.
- Do not reformat adjacent code
- Do not refactor unrelated functions
- Do not remove comments or code your change didn't render unnecessary
- Do not change whitespace, imports, or style outside your diff

### 4. Goal-Driven Execution
Transform every task into explicit, verifiable success criteria.
Loop until those criteria are met. Do not report done until verified.

---

## Development Workflow

Follow these phases in order. Do not skip ahead.

1. **Read wiki** — check for existing knowledge (SESSION START RULE)
2. **Explore** — read relevant files, understand the system
3. **Plan** — write a concrete implementation plan (brainstorming skill)
4. **Build** — implement against the plan, one logical unit at a time
5. **Verify** — run tests, linter, type checker
6. **Save** — run `/save`, update wiki (TASK COMPLETION RITUAL)
7. **Ship** — commit with a descriptive message, open PR

Use `/spec`, `/plan`, `/fix-issue`, `/review`, `/code-simplify`, `/ship` for structured workflows.
Use `/wiki`, `/save`, `/ingest` to maintain the knowledge base.
Use `/sales` for the full sales pipeline.

---

## Repository Conventions

**Branches**: `feat/<slug>`, `fix/<slug>`, `chore/<slug>`, `claude/<task-slug>`
**Commits**: imperative mood, ≤72 chars subject, explain WHY not WHAT
**PRs**: must include Summary, Test Plan, and link to issue/spec
**Never** commit `.env`, secrets, or credentials

---

## Build, Test, Lint

```bash
npm install
npm test
npm run lint
npm run typecheck
npm run build
```

Always run lint + typecheck after making changes. Fix all errors before reporting done.

---

## Code Style

- Prefer explicit over implicit
- No magic numbers — name constants
- Functions do one thing
- Error handling only at system boundaries (user input, external APIs)
- No comments explaining WHAT — only WHY
- Tests live next to the code they test

---

## Environment

Copy `.env.example` to `.env` and fill in values. Never commit `.env`.

---

## Wiki Schema

### Structure

```
wiki/
  index.md          ← table of contents, auto-updated
  concepts/         ← evergreen knowledge (how things work)
  projects/         ← ongoing work and decisions
  research/         ← research findings and agent output
inbox/              ← raw notes waiting to be processed
```

### Page conventions

- **Filename**: lowercase, hyphen-separated (`ai-native-development.md`)
- **Title**: H1 at the top, matches the filename concept
- **Links**: Obsidian wiki links `[[page-name|Display Name]]`
- **Related section**: every page ends with `## Related`
- **No timestamps** in page content — git history tracks changes

### When to create vs update

- **Create** when a concept is distinct enough to stand alone
- **Update** when new info refines what's already there
- **Never delete** — move outdated info to `## History` at the bottom

### After every wiki write

Update `wiki/index.md`. Update `HOME.md` Recent Entries. Update `CONTEXT.md`.

---

## Context Management

- `/clear` between unrelated tasks
- Use subagents for deep codebase exploration
- `/compact` when context gets heavy mid-task
- If you correct Claude twice on the same mistake: `/clear` and re-prompt
