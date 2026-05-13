---
name: ship
description: Final checks, commit, and open a PR. Run after all verification passes.
disable-model-invocation: true
version: 1.0.0
author: Bespoke Solutions
license: proprietary
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: ship, deploy, git, workflow
---

Ship the current work: $ARGUMENTS

1. Run the full verification suite:
   ```
   npm run lint && npm run typecheck && npm test
   ```
   If anything fails, stop and fix it first.

2. Run `/review` to self-check the diff for surgical violations and issues.
   If there are 🔴 MUST FIX items, stop and fix them.

3. Check that no `.env` files, secrets, or credentials are staged:
   ```
   git diff --cached --name-only
   ```

4. Commit with a descriptive message:
   - Subject: imperative mood, ≤72 chars, explains WHY not WHAT
   - Body (if needed): context, tradeoffs, issue reference

5. Push to the feature branch:
   ```
   git push -u origin <branch>
   ```

6. Open a PR with `gh pr create` using this template:
   ```
   ## Summary
   - What changed and why (2-3 bullets)

   ## Test Plan
   - [ ] How to verify this works
   - [ ] Edge cases tested

   ## Related
   Closes #<issue> (if applicable)
   ```

Report the PR URL when done.
