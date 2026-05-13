# Team Onboarding — Bespoke Solutions

Get set up for AI-native development in about 30 minutes.

---

## 1. Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
claude --version
claude auth login
```

You need an Anthropic account.

---

## 2. Clone the repo

```bash
git clone https://github.com/alessandromartelli/bespokesolutions.git
cd bespokesolutions
```

---

## 3. Run the setup script

```bash
bash scripts/setup.sh
```

This will:
- Copy `.env.example` → `.env` for you to fill in
- Copy `CLAUDE.local.md.example` → `CLAUDE.local.md` for personal overrides
- Copy `.claude/settings.local.json.example` → `.claude/settings.local.json`

---

## 4. Fill in your `.env`

Open `.env` and add the values. We use the following services across the company. Ask a teammate for shared keys via 1Password — never paste secrets in Slack or email.

| Variable | What it's for | Where to get it |
|---|---|---|
| `ANTHROPIC_API_KEY` | Claude Opus 4.7 — heavy reasoning, long coding tasks | [console.anthropic.com](https://console.anthropic.com) |
| `OPENAI_API_KEY` | GPT 5.5 — default model for Hermes agents | [platform.openai.com](https://platform.openai.com) |
| `HERMES_API_KEY` | Agent harness | [hermes-agent.org](https://hermes-agent.org/) |
| `ORGO_API_KEY` | Cloud computers for customer agents | [orgo.ai](https://orgo.ai) |
| `COMPOSIO_API_KEY` | One MCP for 1000+ tool integrations | [composio.dev](https://composio.dev) |
| `AGENTMAIL_API_KEY` | Email address per agent | [agentmail.to](https://agentmail.to) |
| `PERPLEXITY_API_KEY` | Real-time research MCP | [perplexity.ai](https://perplexity.ai) |
| `EXA_API_KEY` | Web search MCP | [exa.ai](https://exa.ai) |
| `FIRECRAWL_API_KEY` | Website scraping MCP | [firecrawl.dev](https://firecrawl.dev) |

---

## 5. Open the repo in Obsidian

The repo is also an Obsidian vault.

1. Download [Obsidian](https://obsidian.md)
2. "Open folder as vault" → pick the repo directory
3. Open `HOME.md` — this is your dashboard
4. Browse the wiki via the graph view

Every page Claude writes is browsable in Obsidian. Every page you write or edit in Obsidian is read by Claude.

---

## 6. Add your personal Claude overrides (optional)

`CLAUDE.local.md` is yours — gitignored, never shared. Use it for:
- Personal preferences ("always use Vim keybindings in shell commands")
- Machine-specific paths
- Reminders that only apply to you

See `CLAUDE.local.md.example` for ideas.

---

## 7. Connect MCP servers

Our standard MCP stack. Run each command once:

```bash
# GitHub (required)
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# Memory (Anthropic official — knowledge graph across sessions)
claude mcp add memory -- npx -y @modelcontextprotocol/server-memory

# Perplexity (real-time research)
claude mcp add perplexity -- npx -y perplexity-mcp

# Composio (1000+ tool integrations — once you have an API key)
# See composio.dev for the install command

# Optional: Notion if used for specs/docs
claude mcp add notion -- npx -y @modelcontextprotocol/server-notion
```

Check what's connected:
```bash
claude mcp list
```

---

## 8. Verify Claude Code sees the project

Open Claude Code in the repo root:
```bash
claude
```

On your first message, the session-start hook should inject `CONTEXT.md` and `wiki/index.md`. If it doesn't, check `.claude/settings.json` and the hook configuration.

Ask Claude: `"What slash commands are available?"` — you should see `/spec`, `/plan`, `/fix-issue`, `/review`, `/code-simplify`, `/ship`, `/wiki`, `/save`, `/ingest`, `/sales`.

---

## 9. Read the workflow doc

[docs/ai-workflow.md](ai-workflow.md) explains how we work day-to-day. Read it before your first task.

The wiki-first methodology is mandatory — `CLAUDE.md` enforces it.

---

## How We Work — Quick Reference

| Task | Command |
|---|---|
| Start a new feature | `/spec <description>` |
| Plan implementation | `/plan docs/specs/<slug>.md` |
| Fix a GitHub issue | `/fix-issue <number>` |
| Review your diff | `/review` |
| Simplify after building | `/code-simplify` |
| Ship to PR | `/ship` |
| Research a topic to the wiki | `/wiki <topic>` |
| Save knowledge from this session | `/save` |
| Process raw notes in inbox/ | `/wiki process-inbox` |
| Find prospects (sales) | `/sales prospect "criteria"` |
| Full sales pipeline | See [docs/ai-workflow.md](ai-workflow.md) |

---

## Branch Naming

| Type | Pattern |
|---|---|
| Feature | `feat/<slug>` |
| Bug fix | `fix/<slug>` |
| Chore | `chore/<slug>` |
| AI-driven task | `claude/<task-slug>` |

---

## Questions?

Read [docs/ai-workflow.md](ai-workflow.md). For company context, read [wiki/projects/bespoke-solutions.md](../wiki/projects/bespoke-solutions.md) and [wiki/concepts/agent-business-playbook.md](../wiki/concepts/agent-business-playbook.md).

If still stuck, open a GitHub issue tagged `question`.
