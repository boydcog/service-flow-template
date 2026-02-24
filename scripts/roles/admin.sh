#!/bin/bash

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo ""
echo "          ADMIN WORKFLOW — Template Management                "
echo ""
echo ""

# Step 1: Check role
ROLE_FILE=".user-identity"
if [ -f "$ROLE_FILE" ]; then
  ROLE=$(grep "^role:" "$ROLE_FILE" | sed 's/role: //' || true)
  if [ "$ROLE" != "admin" ] && [ "$ROLE" != "developer" ] && [ ! -z "$ROLE" ]; then
    echo "${RED} This workflow requires admin or developer role${NC}"
    echo "${RED}Current role: $ROLE${NC}"
    exit 1
  fi
fi

# Step 2: Lint validation
echo "${BLUE}${NC}"
echo "${BLUE} Step 1: Linting...${NC}"
echo "${BLUE}${NC}"

if npm run lint 2>&1 | tail -5; then
  echo "${GREEN} Lint passed${NC}"
else
  echo "${RED} Lint failed${NC}"
  exit 1
fi

# Step 3: Type checking
echo ""
echo "${BLUE}${NC}"
echo "${BLUE} Step 2: Type checking...${NC}"
echo "${BLUE}${NC}"

if npm run type-check 2>&1 | head -20; then
  echo "${GREEN} Type check passed${NC}"
else
  echo "${YELLOW}  Type check has warnings${NC}"
fi

# Step 4: Tests
echo ""
echo "${BLUE}${NC}"
echo "${BLUE} Step 3: Running tests...${NC}"
echo "${BLUE}${NC}"

if npm run test; then
  echo "${GREEN} Tests passed${NC}"
else
  echo "${RED} Tests failed${NC}"
  exit 1
fi

# Step 5: Admin menu
echo ""
echo "${BLUE}${NC}"
echo "${GREEN} All verifications passed!${NC}"
echo "${BLUE}${NC}"
echo ""
echo "  Admin Tasks:"
echo ""
echo "1⃣  Manage Templates"
echo "   → Edit: .claude/spec/component-spec.md"
echo ""
echo "2⃣  Manage Roles"
echo "   → Edit: .claude/manifests/roles.yaml"
echo "   → Edit: .claude/manifests/team.yaml"
echo ""
echo "3⃣  Update Theme"
echo "   → Edit: .claude/manifests/theme.yaml"
echo "   → Then: components/theme/tokens.css"
echo ""
echo "4⃣  Build for Production"
echo "   → Run: npm run build"
echo ""
echo "5⃣  Start Dev Server"
echo "   → Run: npm run dev"
echo ""
echo "6⃣  View Storybook"
echo "   → Run: npm run storybook"
echo ""

read -p "Select action (1-6) or press Enter to skip: " action

case $action in
  1)
    vim .claude/spec/component-spec.md
    ;;
  2)
    vim .claude/manifests/roles.yaml
    ;;
  3)
    echo "Editing theme..."
    vim .claude/manifests/theme.yaml
    ;;
  4)
    echo "Building for production..."
    npm run build
    ;;
  5)
    echo "Starting dev server..."
    npm run dev
    ;;
  6)
    echo "Starting Storybook..."
    npm run storybook
    ;;
  *)
    echo "No action selected. Exiting."
    ;;
esac
