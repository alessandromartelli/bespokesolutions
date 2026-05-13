# Dropshipping Niches Research

Research conducted with the dropship research agent (`agents/dropship-research.py`).

---

## How to Run Research

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python3 agents/dropship-research.py
```

The agent uses Claude Opus 4.7 with live web search to find trending niches.

---

## Evaluation Criteria

For each niche the agent evaluates:

| Factor | What to look for |
|---|---|
| Supplier availability | AliExpress, CJDropshipping, Spocket |
| Estimated margin | Target >30% after shipping |
| Competition level | Low = opportunity, saturated = avoid |
| Trend direction | Rising or stable preferred |

---

## Findings

*Run the agent and paste findings here with `/save`.*

---

## Related

- [[../../agents/dropship-research|Dropship Research Agent]]
- [[../projects/bespoke-solutions|Bespoke Solutions]]
