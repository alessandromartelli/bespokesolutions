---
name: fix-issue
description: Fix a GitHub issue end-to-end using Explore → Plan → Build → Verify → Ship, with tests and a PR when requested.
version: 1.0.0
author: Bespoke Solutions
license: proprietary
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [bug-fix, github, workflow, full-cycle]
    related_skills: [plan, review, ship]
---

# Fix Issue

Fix a GitHub issue end-to-end while keeping changes surgical and verified.

## Hermes Invocation

Load this skill when the user asks to fix a GitHub issue, issue URL, issue number, bug report, or failing behavior.

Input is an issue number, issue URL, or bug description supplied by the user. If only a number or GitHub URL is provided, fetch details with `gh issue view <issue>`. If the user writes Claude-style syntax such as `/fix-issue 123`, treat it as a normal instruction.

## Workflow

1. Resolve the issue context:
   - Run `gh issue view <issue>` for GitHub issue numbers/URLs.
   - Read the bug description and acceptance criteria.
2. Understand the problem:
   - Reproduce the issue or identify the failing path.
   - Search the codebase for relevant code.
   - Read nearby tests and project conventions (`README.md`, `CLAUDE.md`, `AGENTS.md`, CI config).
3. State a root-cause hypothesis before writing code.
4. Implement the fix with surgical changes only.
5. Write or update a failing test that reproduces the issue, then verify it passes after the fix.
6. Run repository-appropriate verification.
7. If the user asked to ship, commit, push, and open a PR using the `ship` skill procedure.

## Verification

Use the repository's documented verification commands. For Bespoke Solutions Node projects, default to:

```
npm run lint && npm run typecheck && npm test
```

If these scripts do not exist, inspect `README.md`, `CLAUDE.md`, `AGENTS.md`, `package.json`, `pyproject.toml`, or CI config to identify the correct checks.

## Commit and PR Safety

Do not push or open a PR unless the user requested shipping or approved it.
Before committing:
- Show/inspect changed files with `git status --short`.
- Ensure no `.env`, secrets, credentials, tokens, or unrelated files are staged.
- Use a message like `fix: <short description> (closes #<issue>)` when an issue number exists.

PR body should include:
- What the bug was
- What the fix does
- How to verify it is fixed
