---
name: fix-issue
description: Fix a GitHub issue end-to-end. Runs the full Explore → Plan → Build → Verify → Ship cycle.
disable-model-invocation: true
---

Fix GitHub issue: $ARGUMENTS

1. Run `gh issue view $ARGUMENTS` to get the full issue details
2. Understand the problem — read the error, reproduce steps, and affected files
3. Search the codebase for the relevant code
4. Form a hypothesis. State it explicitly before writing any code.
5. Implement the fix — surgical changes only, nothing unrelated
6. Write a failing test that reproduces the issue, then verify it passes after the fix
7. Run: `npm run lint && npm run typecheck && npm test`
8. Fix any lint/type errors before continuing
9. Commit with message: `fix: <short description> (closes #$ARGUMENTS)`
10. Push and open a PR using `gh pr create`

PR body must include:
- What the bug was
- What the fix does
- How to verify it's fixed
