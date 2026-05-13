#!/usr/bin/env bash
# One-time setup for new team members.
set -e

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RESET='\033[0m'

echo -e "${BOLD}Bespoke Solutions — dev setup${RESET}"
echo ""

# .env
if [ ! -f .env ]; then
  cp .env.example .env
  echo -e "${GREEN}✓${RESET} Created .env from .env.example — fill in your values"
else
  echo -e "  .env already exists, skipping"
fi

# CLAUDE.local.md
if [ ! -f CLAUDE.local.md ]; then
  cp CLAUDE.local.md.example CLAUDE.local.md
  echo -e "${GREEN}✓${RESET} Created CLAUDE.local.md — add your personal Claude overrides"
else
  echo -e "  CLAUDE.local.md already exists, skipping"
fi

# .claude/settings.local.json
if [ ! -f .claude/settings.local.json ]; then
  echo '{"permissions":{"allow":[]}}' > .claude/settings.local.json
  echo -e "${GREEN}✓${RESET} Created .claude/settings.local.json — add personal permission overrides"
else
  echo -e "  .claude/settings.local.json already exists, skipping"
fi

echo ""
echo -e "${BOLD}MCP servers${RESET}"
echo "Installing recommended MCP servers for Claude Code..."

install_mcp() {
  local name=$1
  local cmd=$2
  if claude mcp list 2>/dev/null | grep -q "^$name"; then
    echo -e "  $name already installed, skipping"
  else
    echo -e "  Installing $name..."
    eval "$cmd" && echo -e "${GREEN}✓${RESET} $name installed" || echo -e "${YELLOW}⚠${RESET}  $name failed — install manually: $cmd"
  fi
}

install_mcp "github"   "claude mcp add github   -- npx -y @modelcontextprotocol/server-github"
install_mcp "notion"   "claude mcp add notion   -- npx -y @modelcontextprotocol/server-notion"
install_mcp "supabase" "claude mcp add supabase -- npx -y @modelcontextprotocol/server-supabase"

echo ""
echo -e "${BOLD}Done.${RESET} Next steps:"
echo "  1. Fill in .env with your values"
echo "  2. Edit CLAUDE.local.md with personal preferences"
echo "  3. Read docs/onboarding.md"
echo "  4. Open Claude Code: claude"
echo ""
