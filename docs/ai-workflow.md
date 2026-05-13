# AI Workflow at Bespoke Solutions

> 80%+ of our code is written by agentic AI. This document explains how we work.

---

## Philosophy

We are a Software 3.0 company. We don't write most code by hand — we direct AI agents toward verifiable goals and review the results. The human role is to:

1. Define clear success criteria
2. Review diffs, not prose descriptions
3. Catch surgical violations and over-engineering
4. Maintain a sharp CLAUDE.md as the team's shared memory

Karpathy's 4 rules are embedded in our CLAUDE.md because they target the specific failure modes we see most: agents that guess instead of asking, agents that over-engineer, agents that touch more than they should, and agents that report done before verifying.

---

## Daily Workflow

### Starting a new feature
```
/spec <feature description>
```
This interviews you, then writes a spec to `docs/specs/`. Review and commit the spec before implementation starts.

### Planning implementation
```
/plan docs/specs/<slug>.md
```
Claude explores the codebase in plan mode and produces a file-level implementation plan. Approve the plan before any code is written.

### Building
Work through the plan one logical unit at a time. Each unit should be a clean, passing commit.

### Verifying
After each unit:
```bash
npm run lint && npm run typecheck && npm test
```
Do not move to the next unit until all checks pass.

### Reviewing your own diff
```
/review
```
Check for surgical violations before shipping. Run this before every PR.

### Shipping
```
/ship
```
Runs final checks, commits, pushes, and opens the PR.

---

## Fixing bugs

```
/fix-issue <issue-number>
```

Runs the full cycle: explore → reproduce → fix → test → ship.

---

## Context hygiene

- `/clear` between unrelated tasks — stale context degrades output
- Use subagents for deep exploration: `"Use a subagent to investigate how X works"`
- Keep CLAUDE.md under 300 lines — bloated files get ignored
- `/compact` when context gets heavy mid-task
- If you correct Claude twice on the same mistake, `/clear` and re-prompt

---

## Parallel sessions

For large features, run parallel Claude sessions using worktrees:
```bash
git worktree add ../bespokesolutions-feat-X feat/X
# Open a second Claude Code session in that directory
```

Writer/Reviewer pattern: one session builds, a second session reviews from a clean context.

---

## What humans review

**Always review:**
- The full diff before merging any PR
- Surgical violations (changes outside task scope)
- Security-sensitive code (auth, input handling, data access)
- Architecture decisions

**Delegate to agents:**
- `/security-review` for security audits
- `/review` or the `code-reviewer` subagent for code quality
- `test-writer` subagent to write tests in isolation

---

## Keeping CLAUDE.md sharp

CLAUDE.md is team infrastructure. Treat it like code:
- When Claude repeatedly makes the same mistake, add a rule
- When a rule isn't changing Claude's behaviour, remove it
- Keep rules specific and verifiable
- Prune regularly — every rule competes for attention

---

## Branch and PR conventions

| Type | Branch name |
|------|-------------|
| Feature | `feat/<slug>` |
| Bug fix | `fix/<slug>` |
| Chore/tooling | `chore/<slug>` |
| AI-driven task | `claude/<task-slug>` |

PRs require: Summary, Test Plan, and issue link. See `.github/PULL_REQUEST_TEMPLATE.md`.
