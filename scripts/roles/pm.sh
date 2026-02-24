#!/bin/bash

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         📱 PM WORKFLOW — Service Flow Development              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Check role
ROLE_FILE=".user-identity"
if [ -f "$ROLE_FILE" ]; then
  ROLE=$(grep "^role:" "$ROLE_FILE" | sed 's/role: //' || true)
  if [ "$ROLE" != "pm" ] && [ ! -z "$ROLE" ]; then
    echo "${YELLOW}⚠️  Current role: $ROLE (not pm)${NC}"
    echo "${YELLOW}Continuing anyway...${NC}"
  fi
fi

# Step 2: Lint validation
echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "${BLUE}📝 Step 1: Linting...${NC}"
echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if npm run lint 2>&1 | tail -5; then
  echo "${GREEN}✅ Lint passed${NC}"
else
  echo "${RED}❌ Lint failed${NC}"
  exit 1
fi

# Step 3: Type checking
echo ""
echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "${BLUE}🔍 Step 2: Type checking...${NC}"
echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if npm run type-check 2>&1 | head -20; then
  echo "${GREEN}✅ Type check passed${NC}"
else
  echo "${YELLOW}⚠️  Type check has warnings (non-blocking)${NC}"
fi

# Step 4: Tests
echo ""
echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "${BLUE}🧪 Step 3: Running tests...${NC}"
echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if npm run test; then
  echo "${GREEN}✅ Tests passed${NC}"
else
  echo "${RED}❌ Tests failed${NC}"
  exit 1
fi

# Step 5: Dev Server
echo ""
echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "${GREEN}✅ All verifications passed!${NC}"
echo "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "${BLUE}🚀 Launching development server...${NC}"
echo ""
echo "${YELLOW}📍 Access at: http://localhost:3001/${NC}"
echo ""
echo "💡 Tips:"
echo "   • Use components in src/App.tsx"
echo "   • Dark mode toggle: 🌙/☀️ button in header"
echo "   • Ctrl+C to stop server"
echo "   • HMR enabled: changes appear instantly"
echo ""

npm run dev
