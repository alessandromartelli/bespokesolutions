---
name: plan
description: Create a concrete implementation plan for a spec or task. Use before touching code on non-trivial implementation work.
version: 1.0.0
author: Bespoke Solutions
license: proprietary
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [plan, architecture, development, workflow]
    related_skills: [spec, review]
---

# Plan

Create a concrete implementation plan for a spec or task before modifying code.

## Hermes Invocation

Load this skill when the user asks for an implementation plan, wants to plan before coding, or provides a spec/task that is non-trivial.

Input is the spec path, issue, or task description supplied by the user. If the user writes Claude-style syntax such as `/plan docs/specs/foo.md`, treat it as a normal instruction.

## Workflow

1. Read the spec or task description.
2. Explore the relevant codebase in read-only mode:
   - read files most likely to change
   - inspect existing tests and patterns
   - check project docs (`README.md`, `CLAUDE.md`, `AGENTS.md`) and CI config
3. Identify existing patterns to follow; do not invent a new pattern when one exists.
4. List every file expected to be created or modified.
5. Break the work into logical implementation units. Each unit should be small enough to review independently.
6. State verification steps: tests, linters, type checks, and manual behavior checks.
7. Present the plan and ask for approval before implementing.

## Output Format

```
## Implementation Plan: <title>

### Assumptions
- List what you're assuming to be true

### Files to Change
- path/to/file.ts — reason

### Implementation Steps
1. Step one (files: foo.ts)
2. Step two (files: bar.ts, baz.ts)

### Verification
- [ ] npm test passes
- [ ] npm run lint passes
- [ ] npm run typecheck passes
- [ ] <specific behaviour check>

### Risks / Open Questions
- Anything that could go wrong or needs a decision
```

## Safety

Do not write implementation code until the user approves the plan, unless they explicitly asked for autonomous execution.
