# Sales Agent

Multi-agent pipeline for autonomous prospecting and outreach at Bespoke Solutions.

> **Internal tool** — this is how Bespoke finds and closes its own clients, not a product sold to customers.

---

## Sub-components

| Component | Target | Status |
|---|---|---|
| `prospect-manufacturing` | Manufacturing SMEs, BAB + South of France | Data sources identified, workflow being mapped |

---

## Architecture

Five focused agents, human approval gate before anything sends.

```
Prospector → Researcher → Strategist → Copywriter → [You approve] → Send
```

| Agent | File | Job |
|---|---|---|
| Prospector | `.claude/agents/sales-prospector.md` | Finds leads from web/maps/LinkedIn based on criteria |
| Researcher | `.claude/agents/sales-researcher.md` | Deep-dives one prospect, builds full profile + pain score |
| Strategist | `.claude/agents/sales-strategist.md` | Decides warmth, channel, angle, goal, sequence |
| Copywriter | `.claude/agents/sales-copywriter.md` | Writes all 4 touches, ready for review |

Orchestrated via `/sales` skill (`.claude/skills/sales/SKILL.md`).

---

## Decision Matrix

Every outreach decision is made by crossing three inputs:

**Warmth** (Hot / Warm / Cold)
× **Vertical** (Law firm / Marketing agency / Insurance / Manufacturer / Wholesaler / Real estate — see [[../research/target-verticals|Target Verticals]])
× **Funnel Stage** (Discover / Nurture / Demo-ready / Closing)

= Channel + Goal + Angle + Tone

See [[../concepts/sales-playbook|Sales Playbook]] for the full matrix.

---

## Workflow

```
/sales prospect "criteria"       → find leads
/sales research "business"       → deep-dive one
/sales strategize "slug"         → build strategy
/sales draft "slug"              → write messages
→ review in Obsidian → approve → send manually
/sales pipeline                  → see all status
```

---

## What goes in inbox/

| File pattern | Created by | Contains |
|---|---|---|
| `prospects-YYYY-MM-DD.md` | Prospector | List of leads with pain signals |
| `research-<slug>.md` | Researcher | Full prospect profile + pain score |
| `strategy-<slug>.md` | Strategist | Channel, angle, goal, sequence plan |
| `outreach-<slug>.md` | Copywriter | 4-touch message sequence, approval checkbox |

---

## Assets needed before outreach

See [[brand-assets|Brand Assets]] for the full list. Minimum before first outreach:
- [ ] Email signature set up
- [ ] LinkedIn profile polished
- [ ] One-liner for Bespoke (what we do in one sentence)
- [ ] At least one case study or "what we could do for you" demo template per vertical

---

## Related

- [[../concepts/sales-playbook|Sales Playbook]]
- [[../concepts/agent-business-playbook|Agent Business Playbook]]
- [[brand-assets|Brand Assets]]
- [[../research/target-verticals|Target Verticals]]
- [[bespoke-solutions|Bespoke Solutions]]
