---
name: code-simplify
description: Review recently changed code for over-engineering and simplify it. Run after building a feature.
version: 1.0.0
author: Bespoke Solutions
license: proprietary
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: refactor, simplify, code-quality, workflow
---

Simplify the code changed in: $ARGUMENTS

Run `git diff main...HEAD` (or read the specified file/path).

For each changed section, ask:
1. Is this the minimum code that solves the problem?
2. Are there unrequested abstractions?
3. Could this be written in half as many lines with no loss of clarity?
4. Would a senior engineer call this overcomplicated?

Apply simplifications that:
- Remove speculative generalization
- Collapse unnecessary indirection
- Replace verbose patterns with idiomatic ones
- Delete code that adds complexity without value

Do NOT simplify:
- Code outside the changed diff
- Code whose complexity exists for a documented reason
- Code that would break tests if simplified

After each change, run `npm run lint && npm run typecheck && npm test` to verify nothing broke.

Report: what you simplified and why, with before/after for each change.
