# Dropshipping Niches Research

> **Status**: Demo / proof-of-concept. Not part of Bespoke's strategic direction.
>
> This page exists as a working example of what an agent can produce. The script `agents/dropship-research.py` demonstrates a Claude-powered web research agent. Useful as reference when building research-style skills.

---

## What This Is

A standalone Python agent that uses Claude Opus 4.7 with server-side web search to research and evaluate dropshipping product niches. Built during early scaffolding as a "can we get a working agent in 5 minutes" exercise.

Run it:
```bash
export ANTHROPIC_API_KEY=sk-ant-...
python3 agents/dropship-research.py
```

---

## Why It's Here, Not in the Bin

The agent itself is a useful reference for:
- Streaming Claude responses
- Server-side web search tool usage
- Adaptive thinking pattern
- Single-file Python agent structure

If you're building a new research-style skill or agent for a customer, this file is a working starting point.

---

## What It's NOT

- A product line
- A revenue channel for Bespoke
- A vertical we target

Bespoke sells AI Employees to SMEs (see [[../projects/bespoke-solutions|Bespoke Solutions]]). We're not in dropshipping.

---

## Related

- [[../projects/bespoke-solutions|Bespoke Solutions]]
- [[../concepts/agent-architecture|Agent Architecture]]
