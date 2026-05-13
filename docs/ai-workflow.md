# AI Workflow at Bespoke Solutions

> 80%+ of our code is written by agentic AI. This document explains how we work.

---

## Philosophy

We are a Software 3.0 company. We don't write most code by hand — we direct AI agents toward verifiable goals and review the results. The human role is:

1. Define clear success criteria
2. Review diffs, not prose descriptions
3. Catch surgical violations and over-engineering
4. Maintain `CLAUDE.md`, `CONTEXT.md`, and the `wiki/` as the team's shared memory

Karpathy's 4 rules are embedded in `CLAUDE.md` because they target the specific failure modes we see most: agents that guess instead of asking, agents that over-engineer, agents that touch more than they should, and agents that report done before verifying.

---

## The Wiki-First Methodology

Every session reads the wiki before acting. Every session writes back to the wiki when knowledge changes.

### At session start
The `UserPromptSubmit` hook automatically injects `CONTEXT.md` and `wiki/index.md`. Claude opens every session knowing what's active and what knowledge exists.

### Before any task
1. Check `wiki/` for prior knowledge on the topic
2. Read relevant pages fully before proceeding
3. The wiki beats your training — if it says something different from general defaults, follow the wiki

### After any task
1. Run `/save` — capture decisions, findings, and patterns
2. Update `CONTEXT.md` if active work or decisions changed
3. Update `wiki/index.md` if a new page was created

This is mandatory, not optional. See `CLAUDE.md` for the hard rules.

---

## Daily Workflow

### Starting a new feature or build
```
/spec <feature description>
```
Writes a spec to `docs/specs/`. Review and commit before implementation.

### Planning implementation
```
/plan docs/specs/<slug>.md
```
Claude explores the codebase in plan mode and produces a file-level plan. Approve before any code is written.

### Building
Work through the plan one logical unit at a time. Each unit = clean passing commit.

### Verifying
After each unit:
```bash
npm run lint && npm run typecheck && npm test
```
Don't move forward until all checks pass.

### Reviewing your diff
```
/review
```
Catches surgical violations before shipping. Run before every PR.

### Shipping
```
/ship
```
Runs final checks, commits, pushes, opens the PR.

### Capturing knowledge
```
/save
```
After any session that produced knowledge, run `/save`. The wiki only compounds if outcomes flow back into it.

---

## Wiki Commands

| Command | What it does |
|---|---|
| `/wiki <topic>` | Research a topic and add to the wiki |
| `/wiki process-inbox` | Process raw notes in `inbox/` into wiki pages |
| `/wiki update-index` | Regenerate `wiki/index.md` |
| `/wiki lint` | Find broken links, orphan pages, stale content |
| `/save` | Save the current conversation to the wiki + update CONTEXT.md |
| `/ingest <url>` | Feed Claude a URL, integrate findings into the wiki |

---

## Sales Pipeline Commands

| Command | What it does |
|---|---|
| `/sales prospect "criteria"` | Find new leads |
| `/sales research "business"` | Deep-dive one prospect |
| `/sales strategize "slug"` | Build outreach strategy from the playbook |
| `/sales draft "slug"` | Write 4-touch message sequence |
| `/sales pipeline` | Full pipeline status |
| `/sales close <slug> <outcome>` | Feed outcomes back into the playbook |

See [[../wiki/projects/sales-agent|Sales Agent]] for the full architecture.

---

## Fixing bugs

```
/fix-issue <issue-number>
```
Runs the full cycle: explore → reproduce → fix → test → ship.

---

## Context Management

- `/clear` between unrelated tasks — stale context degrades output
- Use subagents for deep exploration: `"Use a subagent to investigate how X works"`
- Keep `CLAUDE.md` under 300 lines — bloated files get ignored
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
- Outreach messages before they send (sales pipeline approval gate)

**Delegate to agents:**
- `/security-review` for security audits
- `/review` or the `code-reviewer` subagent for code quality
- `test-writer` subagent to write tests in isolation

---

## Keeping CLAUDE.md and the wiki sharp

CLAUDE.md is team infrastructure. The wiki is team memory. Both decay if not maintained.

- When Claude repeatedly makes the same mistake, add a rule to `CLAUDE.md`
- When a rule isn't changing behaviour, remove it
- Run `/wiki lint` periodically — clean broken links, orphan pages
- Update `CONTEXT.md` after any session that shifted strategy or active work
- Prune regularly — every rule and page competes for attention

---

## Branch and PR conventions

| Type | Branch name |
|---|---|
| Feature | `feat/<slug>` |
| Bug fix | `fix/<slug>` |
| Chore/tooling | `chore/<slug>` |
| AI-driven task | `claude/<task-slug>` |

PRs require: Summary, Test Plan, and issue/spec link. See `.github/PULL_REQUEST_TEMPLATE.md`.

---

## The Stack We Use Internally and Sell to Customers

| Layer | Tool |
|---|---|
| Agent harness | Hermes Agent |
| Compute (per customer) | Orgo |
| Tool connector | Composio |
| Agent identity | Agent Mail |
| Memory | Obsidian vault + this wiki |
| Build environment | Claude Code / Codex |
| Default model | GPT 5.5 |
| Heavy reasoning | Claude Opus 4.7 |

We are our own first customer. Everything we deploy to clients, we run for ourselves first.

See [[../wiki/concepts/agent-business-playbook|Agent Business Playbook]] for the full operational framework.
