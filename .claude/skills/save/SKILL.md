# /save

Save the current conversation as a wiki entry and update CONTEXT.md.

## Usage

```
/save
/save <title>
```

## Behavior

1. Review the current conversation — identify the durable knowledge: decisions made, concepts explained, research found, problems solved, patterns that worked or didn't
2. If a title is provided, use it. Otherwise infer the best title from the conversation.
3. Determine the right wiki subfolder:
   - New concept or explanation → `wiki/concepts/`
   - Project decision or update → `wiki/projects/`
   - Research findings → `wiki/research/`
4. Check if a relevant page already exists. If yes, integrate into it. If no, create a new page.
5. Write only what would be useful to a future reader — not the back-and-forth, just the conclusions and decisions.
6. Add a `## Related` section linking to connected pages.
7. Update `wiki/index.md` if it's a new page.
8. Update `HOME.md` Recent Entries if it's a new page.
9. **Update `CONTEXT.md`** — this is mandatory:
   - Update the Active Work table to reflect current state
   - Update Key Decisions Made if a new decision was reached
   - Update any outdated status entries

## What to save vs skip

**Save:**
- Decisions and their rationale
- Concepts that were explained or clarified
- Research findings
- Patterns that worked or didn't work
- Anything you'd want to know at the start of the next session

**Skip:**
- Debugging back-and-forth that led nowhere
- Temporary context that won't matter next session
- Things already well-documented in the wiki with no new information

## After saving

Confirm to the user:
- Which wiki page was created or updated
- What was added to CONTEXT.md
- Whether wiki/index.md was updated
