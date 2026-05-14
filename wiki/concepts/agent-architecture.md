# Agent Architecture

The standard pattern for building capable, maintainable agents.

---

## The Five Layers

```
┌─────────────────────────────┐
│           Tools             │  Actions: bash, file I/O, web search, APIs
├─────────────────────────────┤
│           Skills            │  Reusable workflows: /wiki, /spec, /plan
├─────────────────────────────┤
│        CLAUDE.md            │  Project context, rules, schema
├─────────────────────────────┤
│       System Prompt         │  Persona, constraints, tone
├─────────────────────────────┤
│            LLM              │  Claude Opus 4.7 — reasoning engine
└─────────────────────────────┘
```

Each layer narrows and sharpens what the LLM does. The LLM alone is just a text predictor.

---

## When to Use Each Surface

| Use case | Surface |
|---|---|
| Single call (classify, summarize, extract) | Claude API |
| Multi-step pipeline, you control the loop | Claude API + tool use |
| Open-ended agent, you host compute | Claude API agentic loop |
| Stateful agent, Anthropic hosts compute | Managed Agents |

---

## Adaptive Thinking

Use `thinking: {type: "adaptive"}` on Opus 4.7. Claude decides how much to think based on complexity. Do not set `budget_tokens` — deprecated on 4.7.

---

## Web Search

Server-side tool — declare it, Claude calls it, no client execution needed:

```python
tools=[{"type": "web_search_20260209", "name": "web_search"}]
```

---

## Related

- [[ai-native-development|AI-Native Development]]
- [[../projects/bespoke-solutions|Bespoke Solutions]]
