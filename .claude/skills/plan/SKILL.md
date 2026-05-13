---
name: plan
description: Create a concrete implementation plan for a spec or task. Always run before touching code on non-trivial tasks.
---

Read the spec or task description: $ARGUMENTS

Then:
1. Explore the relevant codebase in plan mode — read the files most likely to change
2. Identify existing patterns to follow (don't invent new ones if one exists)
3. List every file that will be created or modified
4. Break the work into logical implementation units (each unit = one commit)
5. State the verification steps (tests to run, commands to check)

Output a plan in this format:

```
## Implementation Plan: <title>

### Assumptions
- List what you're assuming to be true

### Files to Change
- path/to/file.ts — reason

### Implementation Steps
1. Step one (files: foo.ts)
2. Step two (files: bar.ts, baz.ts)
...

### Verification
- [ ] npm test passes
- [ ] npm run lint passes
- [ ] npm run typecheck passes
- [ ] <specific behaviour check>

### Risks / Open Questions
- Anything that could go wrong or needs a decision
```

After presenting the plan, ask for approval before implementing. Do not write any code until the plan is approved.
