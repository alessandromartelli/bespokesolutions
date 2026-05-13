---
name: spec
description: Write a detailed spec from a product requirement or user story. Use when starting any non-trivial feature.
version: 1.0.0
author: Bespoke Solutions
license: proprietary
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: spec, planning, development, workflow
---

Interview the user about this requirement: $ARGUMENTS

Ask about:
- Goals and success criteria (how will we know it's done?)
- User-facing behavior and edge cases
- Technical constraints (auth, performance, existing patterns to follow)
- What is explicitly OUT of scope

Use the AskUserQuestion tool to ask questions one at a time. Don't ask obvious questions — dig into the hard parts. Keep asking until you have enough to write a complete spec.

Once done, write the spec to `docs/specs/<slug>.md` with this structure:

```
# <Feature Name>

## Goal
One sentence.

## Background
Why this exists. What problem it solves.

## Success Criteria
- [ ] Verifiable criterion 1
- [ ] Verifiable criterion 2

## Scope
### In Scope
### Out of Scope

## Behaviour
User-facing description of the feature. Edge cases included.

## Technical Notes
Constraints, patterns to follow, files likely to change.

## Open Questions
Any unresolved decisions.
```

After writing, confirm the path and tell the user to open a fresh session with `/plan docs/specs/<slug>.md` to begin implementation.
