---
name: review
description: Review the current branch diff for correctness, security, style, simplicity, and surgical violations.
version: 1.0.0
author: Bespoke Solutions
license: proprietary
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [review, code-quality, security, workflow]
    related_skills: [code-simplify, ship]
---

# Review

Review the current branch diff or user-specified changes for correctness, security, style, simplicity, and surgical scope.

## Hermes Invocation

Load this skill when the user asks for review, pre-commit review, PR review, diff review, or a check for surgical violations.

Input is the branch diff, PR, file/path, or description supplied by the user. If no target is provided, run `git diff main...HEAD`. If the user writes Claude-style syntax such as `/review`, treat it as a normal instruction.

## Workflow

1. Get the relevant diff:
   - current branch: `git diff main...HEAD`
   - staged changes: `git diff --cached`
   - user-specified file/path/PR when provided
2. Read nearby context for any changed code that is not understandable from the diff alone.
3. Check the categories below.
4. Report findings with severity and file/line references where possible.

## Review Checklist

### Correctness
- Does the code do what it is supposed to do?
- Are edge cases handled?
- Could this break existing behavior?

### Surgical Violations
- Changes outside the stated task scope
- Reformatted or refactored code the task did not require
- Removed comments or code that was not rendered unnecessary

### Security
- Injection vulnerabilities: SQL, XSS, command injection
- Secrets or credentials in code
- Insecure input handling at system boundaries

### Simplicity
- Is there a simpler way to achieve the same result?
- Are there unrequested abstractions or premature generalization?

### Style
- Follows project conventions in `CLAUDE.md`, `AGENTS.md`, or local docs
- Functions do one thing
- No unexplained magic numbers

## Output Format

```
## Review: <branch or description>

### Summary
One paragraph assessment.

### Issues
- 🔴 MUST FIX: <issue> (file:line)
- 🟡 SHOULD FIX: <issue> (file:line)
- 🟢 SUGGESTION: <issue> (file:line)

### Surgical Violations
List any changes outside task scope, or "None".

### Verdict
APPROVE / REQUEST CHANGES
```
