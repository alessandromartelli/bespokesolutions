# Team Onboarding — Bespoke Solutions

Get set up for AI-native development in 10 minutes.

---

## 1. Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

Verify:
```bash
claude --version
```

You need an Anthropic account. Log in:
```bash
claude auth login
```

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
- Install recommended MCP servers

---

## 4. Fill in your `.env`

Open `.env` and add the values. Ask a teammate for any shared secrets — never send them over Slack/email, use a secrets manager.

---

## 5. Add your personal Claude overrides (optional)

`CLAUDE.local.md` is yours — it is gitignored and never shared. Use it for:
- Personal preferences ("always use Vim keybindings in shell commands")
- Machine-specific paths
- Reminders that only apply to you

See `CLAUDE.local.md.example` for ideas.

---

## 6. Connect MCP servers

Our standard MCP stack. Run each command once:

```bash
# GitHub (required)
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# Notion (if you use it for specs/docs)
claude mcp add notion -- npx -y @modelcontextprotocol/server-notion

# Supabase (if working on backend/DB)
claude mcp add supabase -- npx -y @modelcontextprotocol/server-supabase
```

Check what's connected:
```bash
claude mcp list
```

---

## 7. Verify Claude Code sees the project

Open Claude Code in the repo root:
```bash
claude
```

Ask it: `"What slash commands are available?"` — you should see `/spec`, `/plan`, `/fix-issue`, `/review`, `/code-simplify`, `/ship`.

---

## 8. Read the workflow doc

`docs/ai-workflow.md` explains how we work day-to-day. Read it before your first task.

---

## How we work

| Task | Command |
|------|---------|
| Start a new feature | `/spec <description>` |
| Plan implementation | `/plan docs/specs/<slug>.md` |
| Fix a GitHub issue | `/fix-issue <number>` |
| Review your diff | `/review` |
| Simplify after building | `/code-simplify` |
| Ship to PR | `/ship` |

---

## Branch naming

| Type | Pattern |
|------|---------|
| Feature | `feat/<slug>` |
| Bug fix | `fix/<slug>` |
| Chore | `chore/<slug>` |
| AI-driven task | `claude/<task-slug>` |

---

## Questions?

Read `docs/ai-workflow.md`. If still stuck, open a GitHub issue tagged `question`.
