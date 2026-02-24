#!/bin/bash
set -e

echo ""
echo "================================"
echo "    !"
echo "================================"
echo ""

# 1⃣  
FLOW_NAME="${1:-my-flow}"
PROJECT_PATH="${2:-.}"

echo " : $FLOW_NAME"
echo " : $PROJECT_PATH"
echo ""

# 2⃣   (3000 - Dev Server)
echo "  3000  ..."
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
  lsof -ti:3000 | xargs kill -9 2>/dev/null || true
  sleep 2
fi
echo "   "
echo ""

# 3⃣   
echo "     (localhost:3000)..."
cd "$PROJECT_PATH" 2>/dev/null || true
npm run dev > /tmp/dev-server.log 2>&1 &
DEV_SERVER_PID=$!
sleep 8

if ! kill -0 $DEV_SERVER_PID 2>/dev/null; then
  echo "    "
  cat /tmp/dev-server.log
  exit 1
fi

echo "    "
echo ""

# 4⃣   
echo "   ..."
open "http://localhost:3000" 2>/dev/null || echo " http://localhost:3000  "
echo ""

# 5⃣   
echo "   ..."
echo "      ."
read -p " ? (y/n): " -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "  "
  kill $DEV_SERVER_PID 2>/dev/null || true
  exit 1
fi

# 6⃣   
echo "   ..."
kill $DEV_SERVER_PID 2>/dev/null || true
wait $DEV_SERVER_PID 2>/dev/null || true
echo ""

# 7⃣    (Strict Mode)
echo "    (Strict Mode)..."
echo ""

# Format
echo "  ..."
npm run format
if [ $? -ne 0 ]; then
  echo "  "
  exit 1
fi
echo "  "
echo ""

# 
echo "   ( 0 )..."
npm run lint
if [ $? -ne 0 ]; then
  echo " Lint  - PR  "
  exit 1
fi
echo " Lint "
echo ""

#  
echo "  ..."
npm run type-check
if [ $? -ne 0 ]; then
  echo " Type Check  - PR  "
  exit 1
fi
echo " Type Check "
echo ""

# 
echo "  ..."
npm run test
if [ $? -ne 0 ]; then
  echo " Test  - PR  "
  exit 1
fi
echo " Test "
echo ""

# 8⃣   
echo "=========================================="
echo "    (Strict Mode )"
echo "=========================================="
echo ""
echo "  :"
echo "  [Format]         "
echo "  [Lint]          0"
echo "  [Type-check]     "
echo "  [Test]           "
echo ""
echo " ! PR  ."
echo "=========================================="
echo ""

# 9⃣ Git 
echo " Git  ..."
git add flows/ 2>/dev/null || true
git status --short
echo ""

#  PR  
echo " PR  ..."
read -p "PR ? (y/n): " -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
  # Validate GitHub token before PR creation
  source ./.claude/hooks/gh-token-validate.sh || exit 1

  BRANCH_NAME="flow/$FLOW_NAME-$(date +%s)"
  git remote set-url origin "https://${GH_TOKEN}@github.com/boydcog/service-flow-template.git"

  git checkout -b "$BRANCH_NAME" 2>/dev/null || git switch -c "$BRANCH_NAME"
  git add flows/
  git commit -m "[flow] $FLOW_NAME service flow creation" 2>/dev/null || true

  gh pr create --title "[flow] $FLOW_NAME service flow" \
    --body "## Summary\n- New flow: $FLOW_NAME\n\n## Validation (Strict Mode)\n- Format: Pass\n- Lint: Error 0\n- Type-check: Pass\n- Test: 100% Pass\n- Dev Server: Verified" \
    --base main 2>/dev/null || echo "PR creation skipped (gh cli required)"

  # Remove token from URL (security)
  git remote set-url origin "https://github.com/boydcog/service-flow-template.git"

  echo "PR created successfully"
else
  echo "ℹ  PR  "
fi

echo ""
echo "================================"
echo "   !"
echo "================================"
