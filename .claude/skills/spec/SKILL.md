---
name: spec
description: Write a detailed spec from a product requirement or user story. Use when starting any non-trivial feature.
version: 1.0.0
author: Bespoke Solutions
license: proprietary
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [spec, planning, development, workflow]
    related_skills: [plan]
---

# Spec

Write a detailed spec from a product requirement or user story before implementation planning.

## Hermes Invocation

Load this skill when the user asks to write a spec, refine a requirement, scope a feature, or turn a rough idea into implementation-ready requirements.

Input is the product requirement, user story, or rough idea supplied by the user. If the user writes Claude-style syntax such as `/spec <requirement>`, treat it as a normal instruction.

## Interview

Ask focused questions about:
- Goals and success criteria: how will we know it is done?
- User-facing behavior and edge cases
- Technical constraints: auth, performance, existing patterns to follow
- What is explicitly out of scope

Ask questions one at a time. Do not ask obvious questions; dig into the hard parts. Continue until there is enough information to write a complete spec.

## Output File

Once enough information is gathered, write the spec to `docs/specs/<slug>.md` with this structure:

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

## After Writing

Confirm the path and recommend loading the `plan` skill next with the spec path to begin implementation planning.
