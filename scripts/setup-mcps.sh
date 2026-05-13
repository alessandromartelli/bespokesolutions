#!/usr/bin/env bash
# Bespoke Solutions — MCP Setup
#
# Installs and registers the operational MCP stack with Claude Code:
#   - Hermes Agent (control plane for the AI Employee on the VPS)
#   - Composio (Gmail, Calendar, and 1000+ other apps)
#   - Anthropic Memory (knowledge graph across sessions)
#   - GitHub (repo management)
#
# Run this once per machine. Reads keys from .env (you must populate it first).

set -euo pipefail

# ────────────────────────────────────────────────────────────────────────
# Load .env
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
    echo "⚠️  Skipping: $var is not set in $ENV_FILE"
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
# 1. Hermes MCP
# ────────────────────────────────────────────────────────────────────────

echo "──── Hermes MCP ────"
if require_var HERMES_API_KEY; then
  if [ -n "${HERMES_MCP_URL:-}" ]; then
    # Remote Hermes on VPS
    mcp_add_safe hermes \
      --transport http \
      "$HERMES_MCP_URL" \
      --headers "Authorization:Bearer $HERMES_API_KEY"
    echo "✅ Hermes (remote) registered"
  elif command -v hermes >/dev/null 2>&1; then
    # Local Hermes binary
    mcp_add_safe hermes -- hermes mcp serve
    echo "✅ Hermes (local) registered"
  else
    echo "⚠️  Neither HERMES_MCP_URL nor local hermes binary found. Skipping."
  fi
fi

# ────────────────────────────────────────────────────────────────────────
# 2. Composio MCP(s)
# ────────────────────────────────────────────────────────────────────────
# Composio exposes each connected app as its own MCP URL OR via a unified
# tool-router URL. Get the URL(s) from the Composio dashboard after
# connecting each app, then set them in .env.

echo "──── Composio MCPs ────"
if require_var COMPOSIO_API_KEY; then

  if [ -n "${COMPOSIO_TOOL_ROUTER_URL:-}" ]; then
    # Unified tool-router — preferred. One MCP exposes everything you've connected.
    mcp_add_safe composio \
      --transport http \
      "$COMPOSIO_TOOL_ROUTER_URL" \
      --headers "X-API-Key:$COMPOSIO_API_KEY"
    echo "✅ Composio tool-router registered"
  else
    # Per-app MCPs (set the URLs in .env for the apps you've connected)
    for app in gmail calendar linkedin slack notion; do
      url_var="COMPOSIO_${app^^}_URL"
      url="${!url_var:-}"
      if [ -n "$url" ]; then
        mcp_add_safe "composio-$app" \
          --transport http \
          "$url" \
          --headers "X-API-Key:$COMPOSIO_API_KEY"
        echo "✅ composio-$app registered"
      fi
    done
  fi
fi

# ────────────────────────────────────────────────────────────────────────
# 3. Anthropic Memory MCP (knowledge graph)
# ────────────────────────────────────────────────────────────────────────

echo "──── Memory MCP ────"
mcp_add_safe memory -- npx -y @modelcontextprotocol/server-memory
echo "✅ Memory registered"

# ────────────────────────────────────────────────────────────────────────
# 4. GitHub MCP
# ────────────────────────────────────────────────────────────────────────

echo "──── GitHub MCP ────"
if require_var GITHUB_TOKEN; then
  mcp_add_safe github \
    --env "GITHUB_PERSONAL_ACCESS_TOKEN=$GITHUB_TOKEN" \
    -- npx -y @modelcontextprotocol/server-github
  echo "✅ GitHub registered"
fi

# ────────────────────────────────────────────────────────────────────────
# Done
# ────────────────────────────────────────────────────────────────────────

echo ""
echo "════════════════════════════════════"
echo "  MCP Setup Complete"
echo "════════════════════════════════════"
echo ""
echo "Verify with:  claude mcp list"
echo ""
echo "Note: Agent Mail does not currently ship an MCP server. It is"
echo "accessed via REST API from agents/skills. See agents/agentmail.py"
echo "for the helper (build when ready)."
echo ""
echo "Restart Claude Code for the new MCPs to be visible."
