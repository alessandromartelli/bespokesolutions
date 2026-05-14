---
name: ship
description: Run final checks, commit, push, and open a PR after all verification passes and the user has approved shipping.
version: 1.0.0
author: Bespoke Solutions
license: proprietary
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ship, deploy, git, workflow]
    related_skills: [review, fix-issue]
---

# Ship

Run final checks, commit, push, and open a PR after the work is verified and the user has approved shipping.

## Hermes Invocation

Load this skill when the user asks to ship, commit, push, open a PR, or finish the current work.

Input is an optional branch/issue/summary supplied by the user. If the user writes Claude-style syntax such as `/ship`, treat it as a normal instruction.

## Safety Gate

Do not push or open a PR unless the user explicitly asked to ship or approved that action. Before committing or pushing, inspect changed files and confirm there are no secrets, credentials, `.env` files, tokens, or unrelated changes staged.

## Workflow

1. Run the repository's full verification suite.

   For Bespoke Solutions Node projects, default to:

   ```
   npm run lint && npm run typecheck && npm test
   ```

   If these scripts do not exist, inspect `README.md`, `CLAUDE.md`, `AGENTS.md`, `package.json`, `pyproject.toml`, or CI config to identify the correct checks.

2. Use the `review` skill procedure to self-check the diff for surgical violations and issues.
   - If there are 🔴 MUST FIX items, stop and fix them.

3. Check staged and unstaged changes:

   ```
   git status --short
   git diff --cached --name-only
   ```

4. Commit with a descriptive message:
   - Subject: imperative mood, ≤72 chars, explains why not just what.
   - Body if needed: context, tradeoffs, issue reference.

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

7. Report the PR URL when done.
