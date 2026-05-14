---
name: code-simplify
description: Review recently changed code for over-engineering and simplify it. Use after building a feature or before review/ship.
version: 1.0.0
author: Bespoke Solutions
license: proprietary
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [refactor, simplify, code-quality, workflow]
    related_skills: [review, ship]
---

# Code Simplify

Review recently changed code for over-engineering and simplify it without changing behavior.

## Hermes Invocation

Load this skill when the user asks to simplify, refactor for clarity, reduce complexity, or review changed code for over-engineering.

Input is the file/path/range or branch diff supplied by the user. If no target is provided, inspect the current branch diff with `git diff main...HEAD`.

If the user writes Claude-style syntax such as `/code-simplify <target>`, treat it as a normal instruction, not as a native Hermes slash command.

## Workflow

1. Identify the target:
   - user-specified file/path/range, or
   - `git diff main...HEAD` when no target is provided.
2. For each changed section, ask:
   - Is this the minimum code that solves the problem?
   - Are there unrequested abstractions?
   - Could this be written in half as many lines with no loss of clarity?
   - Would a senior engineer call this overcomplicated?
3. Apply simplifications that:
   - Remove speculative generalization
   - Collapse unnecessary indirection
   - Replace verbose patterns with idiomatic ones
   - Delete code that adds complexity without value
4. Preserve behavior and public interfaces unless the user explicitly approved a breaking change.
5. Run repository-appropriate verification.

## Do Not Simplify

- Code outside the target diff or requested path
- Code whose complexity exists for a documented reason
- Code that would break tests if simplified
- Public APIs, migrations, or data formats without explicit approval

## Verification

Use the repository's documented verification commands. For Bespoke Solutions Node projects, default to:

```
npm run lint && npm run typecheck && npm test
```

If these scripts do not exist, inspect `README.md`, `CLAUDE.md`, `AGENTS.md`, `package.json`, `pyproject.toml`, or CI config to identify the correct checks.

## Report

Report what changed and why, with concise before/after notes for each simplification.
