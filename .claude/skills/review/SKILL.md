---
name: review
description: Review the current branch diff for correctness, security, style, and surgical violations.
---

Review the changes on the current branch: $ARGUMENTS

Run `git diff main...HEAD` to get the full diff.

Check for:

**Correctness**
- Does the code do what it's supposed to do?
- Are edge cases handled?
- Could this break existing behaviour?

**Surgical violations** (IMPORTANT — flag every one)
- Changes outside the stated task scope
- Reformatted or refactored code the task didn't require
- Removed comments or code that wasn't rendered unnecessary

**Security**
- Injection vulnerabilities (SQL, XSS, command injection)
- Secrets or credentials in code
- Insecure input handling at system boundaries

**Simplicity**
- Is there a simpler way to achieve the same result?
- Are there unrequested abstractions or premature generalization?

**Style**
- Follows project conventions in CLAUDE.md?
- Functions do one thing?
- No magic numbers?

Output a structured review:
```
## Review: <branch or description>

### Summary
One paragraph assessment.

### Issues
- 🔴 MUST FIX: <issue> (file:line)
- 🟡 SHOULD FIX: <issue> (file:line)
- 🟢 SUGGESTION: <issue> (file:line)

### Surgical Violations
List any changes outside task scope (or "None").

### Verdict
APPROVE / REQUEST CHANGES
```
