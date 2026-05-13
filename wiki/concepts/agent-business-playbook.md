# Agent Business Playbook

The complete operational framework for running a one-person (or small-team) AI agent agency at $5K-10K/month per customer. Synthesized from Nick (Orgo) and Anthropic's Skills team.

---

## The Offer

**Sell AI employees, not AI agents.**

- $5K/month (OpenClaw harness) — $10K/month (Hermes harness)
- Unlimited everything: agents, usage, monitoring, support, security, changes
- Reality: customer needs 1-3 agents; you control real cost
- 48 hours from contract to first running agent
- Talk in **business outcomes** (revenue, deals closed, hours back) — not "time saved"
- Customer never touches: tokens, models, computer infrastructure, security

**Why this works:** Removing friction is the product. Most SMEs/executives can't set this up themselves and don't want to.

---

## Target Verticals

### Tier 1 — Start Here
- Marketing agencies
- Law firms
- Insurance agencies
- Manufacturers
- Wholesalers
- Real estate agencies

### Avoid (regulatory burden)
- Healthcare
- Finance

### Why these verticals
- Legacy industries that *want* to be AI-native
- Lots of people = lots of inefficiency
- Decision makers have direct buying authority
- Universal pain pattern across all of them

---

## Universal Executive Pain

Every decision-maker, across every vertical, has the same problems:
- Too many emails
- Too many meetings
- Too many follow-ups
- Too many open loops
- Context fragmented across people, projects, tools

**Solve this base layer with one template**, then layer vertical-specific skills on top.

---

## The Stack

| Layer | Tool | Why |
|---|---|---|
| Harness | **Hermes Agent** | Self-evolving, reliable, lets you charge 2x. Doesn't break like OpenClaw |
| Compute | **Orgo** | Cloud computers per customer, one workspace per client, sandboxed |
| Tool connector | **Composio** | One MCP → 1000+ apps (Gmail, Slack, Notion, etc.), handles auth |
| Agent identity | **Agent Mail** | Each agent gets its own email — sends/receives, alerts you on failures |
| Memory | **Obsidian vault** | Markdown second brain, persistent context across sessions ✓ |
| Builder agent | **Claude Code** or **Codex** | Use agents to build customer agents |
| Default model | **GPT 5.5** | Most efficient tool calls, generous usage |
| Cheap model | **GLM 5.1 (ZAI)** or **Kimi** | Open-source, lighter tasks |
| Long coding | **Opus 4.7** | Connected via Claude Code for long horizon coding |

---

## MCP Integration Architecture

How Claude Code (local) and Hermes (VPS) share the same tool layer.

```
   Laptop                                              VPS
   ┌──────────────────────────────┐                  ┌────────────────────────┐
   │  Claude Code (terminal)      │                  │  Hermes Agent          │
   │     │                        │                  │  + Hermes Workspace    │
   │     ├─ MCP: Hermes ──────────┼──── HTTP ────────┤  hermes mcp serve      │
   │     ├─ MCP: Composio (HTTP)  │                  │                        │
   │     ├─ MCP: Memory           │                  │  Same MCPs connected:  │
   │     └─ MCP: GitHub           │                  │  ├─ Composio           │
   │                              │                  │  ├─ Agent Mail (REST)  │
   │  Pushes to GitHub ───────────┼─────┐            │  └─ Memory             │
   └──────────────────────────────┘     │            │                        │
                            ┌───────────▼─────────┐  │  Pulls from GitHub ←──┤
                            │      GitHub         │  └────────────────────────┘
                            │  bespokesolutions   │
                            └─────────────────────┘
```

### Key principle

**Hermes itself is one of the MCPs Claude Code uses.** From the laptop, in Claude Code, you can give Hermes tasks — and Hermes (on the VPS) executes them. Claude Code becomes the developer console; Hermes is the production runtime.

### MCP Stack

| MCP | Transport | Purpose |
|---|---|---|
| **hermes** | HTTP (to VPS) | Send tasks to Hermes; read its session/conversation state |
| **composio** | HTTP | One URL → Gmail, Calendar, LinkedIn, Slack, Notion, 1000+ more |
| **memory** | stdio (local npx) | Anthropic official knowledge graph — entities + relations across sessions |
| **github** | stdio (local npx) | Repo management without leaving Claude Code |

### Setup

Run once per machine after populating `.env`:

```bash
bash scripts/setup-mcps.sh
```

The script reads keys from `.env` and registers each MCP with Claude Code via `claude mcp add`. Idempotent — safe to re-run.

Verify:
```bash
claude mcp list
```

### Agent Mail special case

Agent Mail doesn't ship an MCP server yet. Integrate it via REST API directly inside skills that need to send/receive email as the agent. The API is HTTP-based and trivial to call from any agent.

### Sync loop (laptop → Hermes)

```
laptop: edit skill in Claude Code
     ↓
laptop: /ship (commit + push)
     ↓
GitHub
     ↓
VPS: cron every 60s → git pull
     ↓
Hermes: reload skills
     ↓
new skill is live, callable via the hermes MCP
```

---

## Internal/Customer-Facing Tools

| Tool | Purpose |
|---|---|
| **Granola** | Every meeting auto-transcribed → syncs to Trello as requests |
| **Trello** | Customer-facing kanban (backlog → to-do → doing → done). Prevents scope creep |
| **Loom** | Async updates to customers when you ship something |
| **Calendly** | Booking link |
| **Superhuman** | Email firehose management |
| **Asana** | Internal tasks (not customer-facing) |

---

## Building Agents With Agents

You don't need to know how to manually configure agents. Use this pattern:

1. Spin up an Orgo VM for the customer
2. From your own agent (Telegram, etc.), tell it: "Set up this computer, install Hermes, configure for [customer]"
3. The orchestrator agent uses Orgo MCP to provision everything
4. Use sub-agents in parallel for research:
   - Perplexity MCP — current docs/news
   - Exa AI MCP — real-time web search
   - Context 7 MCP — up-to-date GitHub docs
   - Twitter/X MCP — community setup patterns
   - Firecrawl MCP — site scraping

---

## Reliability Patterns (Critical)

Your customers become dependent. When things break, it's expensive. Build these from day one:

1. **Watchdog scripts** — auto-restart gateways when they crash (especially Telegram/iMessage)
2. **Self-alerting agents** — agent emails you (via Agent Mail) when a skill fails or cron breaks
3. **Sandbox per customer** — separate Orgo VM per customer, blast radius contained
4. **One workspace per customer** in Orgo — manage all their agents from there

---

## Skills as the New Paradigm (Anthropic)

> "Stop rebuilding agents. Start building skills instead."

### Skills are
- Organized folders with markdown + scripts
- Progressive disclosure: only metadata shown until needed
- Composable: an agent can have hundreds, picks the right one at runtime
- Versionable in Git, shareable, zippable
- Open standard via `agentskills.io`

### Three types of skills

| Type | What | Example |
|---|---|---|
| **Foundational** | General capabilities | Document editing, slide styling, EHR analysis |
| **Third-party** | Built by tool vendors | Browserbase stagehand skill, Notion deep research |
| **Enterprise/team** | Built for one org | Internal coding standards, custom workflow |

### The full architecture
```
Agent loop + runtime (Hermes / OpenClaw / Cloud Code)
    + MCP servers (connection to outside world)
    + Skills (procedural expertise)
    = Vertical-specific agent
```

### Skill format (Hermes-compatible)
```yaml
---
name: skill-name
description: One-line capability description
version: 1.0.0
author: Bespoke Solutions
license: proprietary
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: tag1, tag2
---

# Skill body — markdown instructions + scripts referenced
```

---

## Acquiring Customers

- **Content > cold outreach** — get known so calls are warm before they happen
- **Never sell to cold audience** — start free for case studies if needed
- **Demo with their own data** — show audit/agent working on their business in 2 minutes
- **Niche by geography or sub-vertical** — "real estate agencies in Florida" beats "real estate"

---

## What Bespoke Solutions Sells

**Product**: Bespoke AI Employee — fully managed agent for executives

**Bundle:**
- 1-3 named AI employees per customer (with emails, memory, personality)
- Orgo workspace for the customer
- Hermes harness
- Universal executive skill pack (email, calendar, follow-up, meeting notes, open-loop management)
- Vertical-specific skill pack (one per target market)
- 48-hour onboarding
- Trello-managed request queue, unlimited iteration

**Pricing**: €4K-€8K/month per customer

**Moat**: The vertical-specific skill packs Bespoke builds and improves. Each customer makes the skills smarter.

---

## Related

- [[../projects/sales-agent|Sales Agent]]
- [[../projects/brand-assets|Brand Assets]]
- [[sales-playbook|Sales Playbook]]
- [[ai-native-development|AI-Native Development]]
- [[agent-architecture|Agent Architecture]]
- [[../research/target-verticals|Target Verticals]]
