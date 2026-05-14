#!/usr/bin/env bash
# Bespoke Solutions — New Machine Setup
#
# Run once per machine after cloning the repo.
# 1. Creates local config files (.env, CLAUDE.local.md, settings.local.json)
# 2. Installs the MCP stack into Claude Code (reads keys from .env)
#
# MCP stack:
#   - Hermes Agent (AI Employee harness on VPS)
#   - Composio (Gmail, Calendar, LinkedIn, Slack, Notion, 1000+ apps)
#   - Anthropic Memory (knowledge graph across sessions)
#   - GitHub (repo management)

set -euo pipefail

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RESET='\033[0m'

echo -e "${BOLD}Bespoke Solutions — setup${RESET}"
echo ""

# ────────────────────────────────────────────────────────────────────────
# 1. Local config files
# ────────────────────────────────────────────────────────────────────────

echo -e "${BOLD}Local config${RESET}"

if [ ! -f .env ]; then
  cp .env.example .env
  echo -e "${GREEN}✓${RESET} Created .env — fill in your API keys before continuing"
else
  echo -e "  .env already exists, skipping"
fi

if [ ! -f CLAUDE.local.md ]; then
  if [ -f CLAUDE.local.md.example ]; then
    cp CLAUDE.local.md.example CLAUDE.local.md
    echo -e "${GREEN}✓${RESET} Created CLAUDE.local.md — add personal Claude overrides"
  fi
else
  echo -e "  CLAUDE.local.md already exists, skipping"
fi

if [ ! -f .claude/settings.local.json ]; then
  echo '{"permissions":{"allow":[]}}' > .claude/settings.local.json
  echo -e "${GREEN}✓${RESET} Created .claude/settings.local.json"
else
  echo -e "  .claude/settings.local.json already exists, skipping"
fi

echo ""

# ────────────────────────────────────────────────────────────────────────
# 2. Load .env
# ────────────────────────────────────────────────────────────────────────

ENV_FILE="${ENV_FILE:-.env}"

if [ ! -f "$ENV_FILE" ]; then
  echo "❌ $ENV_FILE not found. Copy .env.example to .env and fill in values."
  exit 1
fi

# shellcheck disable=SC1090
set -a; source "$ENV_FILE"; set +a

# ────────────────────────────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────────────────────────────

require_var() {
  local var="$1"
  if [ -z "${!var:-}" ]; then
    echo -e "${YELLOW}⚠${RESET}  Skipping: $var is not set in $ENV_FILE"
    return 1
  fi
  return 0
}

mcp_add_safe() {
  # Idempotent — removes the MCP if it exists, then adds it fresh
  local name="$1"
  shift
  claude mcp remove "$name" 2>/dev/null || true
  claude mcp add "$name" "$@"
}

# ────────────────────────────────────────────────────────────────────────
# 3. MCP stack
# ────────────────────────────────────────────────────────────────────────

echo -e "${BOLD}MCP servers${RESET}"

# — Hermes —
echo "  Hermes..."
if require_var HERMES_API_KEY; then
  if [ -n "${HERMES_MCP_URL:-}" ]; then
    mcp_add_safe hermes \
      --transport http \
      "$HERMES_MCP_URL" \
      --headers "Authorization:Bearer $HERMES_API_KEY"
    echo -e "${GREEN}✓${RESET} Hermes (remote VPS) registered"
  elif command -v hermes >/dev/null 2>&1; then
    mcp_add_safe hermes -- hermes mcp serve
    echo -e "${GREEN}✓${RESET} Hermes (local) registered"
  else
    echo -e "${YELLOW}⚠${RESET}  Neither HERMES_MCP_URL nor local hermes binary found. Skipping."
  fi
fi

# — Composio —
echo "  Composio..."
if require_var COMPOSIO_API_KEY; then
  if [ -n "${COMPOSIO_TOOL_ROUTER_URL:-}" ]; then
    # Unified tool-router — one MCP exposes everything connected in the dashboard
    mcp_add_safe composio \
      --transport http \
      "$COMPOSIO_TOOL_ROUTER_URL" \
      --headers "X-API-Key:$COMPOSIO_API_KEY"
    echo -e "${GREEN}✓${RESET} Composio tool-router registered"
  else
    # Per-app MCPs (set COMPOSIO_<APP>_URL in .env for each app you've connected)
    for app in gmail calendar linkedin slack notion; do
      url_var="COMPOSIO_${app^^}_URL"
      url="${!url_var:-}"
      if [ -n "$url" ]; then
        mcp_add_safe "composio-$app" \
          --transport http \
          "$url" \
          --headers "X-API-Key:$COMPOSIO_API_KEY"
        echo -e "${GREEN}✓${RESET} composio-$app registered"
      fi
    done
  fi
fi

# — Anthropic Memory —
echo "  Memory..."
mcp_add_safe memory -- npx -y @modelcontextprotocol/server-memory
echo -e "${GREEN}✓${RESET} Memory registered"

# — GitHub —
echo "  GitHub..."
if require_var GITHUB_TOKEN; then
  mcp_add_safe github \
    --env "GITHUB_PERSONAL_ACCESS_TOKEN=$GITHUB_TOKEN" \
    -- npx -y @modelcontextprotocol/server-github
  echo -e "${GREEN}✓${RESET} GitHub registered"
fi

# ────────────────────────────────────────────────────────────────────────
# Done
# ────────────────────────────────────────────────────────────────────────

echo ""
echo -e "${BOLD}Done.${RESET} Next steps:"
echo "  1. Fill in .env with your API keys (if not done)"
echo "  2. Restart Claude Code for new MCPs to appear"
echo "  3. Verify: claude mcp list"
echo "  4. Read docs/ai-workflow.md"
echo ""
echo "  Note: Agent Mail has no MCP server yet — accessed via REST API"
echo "  from within skills. See wiki/concepts/agent-business-playbook.md"
echo ""
