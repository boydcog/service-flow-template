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

  # Git 인증 설정 (.gh-token 기반)
  git config --local user.name "Claude Code Bot"
  git config --local user.email "bot@claudecode.local"
  git config --local credential.helper store
  echo "https://:${GH_TOKEN}@github.com" | git credential approve

  git checkout -b "$BRANCH_NAME" 2>/dev/null || git switch -c "$BRANCH_NAME"
  git add flows/
  git commit -m "[flow] $FLOW_NAME service flow creation" 2>/dev/null || true

  # Git push with .gh-token (토큰만 사용)
  git push -u origin "$BRANCH_NAME" 2>&1 || {
    echo "Git push 실패"
    exit 1
  }

  # GitHub API로 PR 생성 (.gh-token만 사용, jq 기반 안전 파싱)
  REPO_URL=$(git remote get-url origin | sed 's|.*github.com[:/]||' | sed 's|\.git$||')
  IFS='/' read -r OWNER REPO_NAME <<< "$REPO_URL"

  PR_BODY="## Summary
- New flow: $FLOW_NAME

## Validation (Strict Mode)
- Format: Pass
- Lint: Error 0
- Type-check: Pass
- Test: 100% Pass
- Dev Server: Verified"

  PR_DATA=$(jq -n \
    --arg title "[flow] $FLOW_NAME service flow" \
    --arg body "$PR_BODY" \
    --arg head "$BRANCH_NAME" \
    --arg base "main" \
    '{title: $title, body: $body, head: $head, base: $base}')

  PR_RESPONSE=$(curl -s -X POST \
    -H "Authorization: token $GH_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    -H "Content-Type: application/json" \
    -d "$PR_DATA" \
    "https://api.github.com/repos/$OWNER/$REPO_NAME/pulls")

  PR_NUMBER=$(echo "$PR_RESPONSE" | jq -r '.number // empty' 2>/dev/null)

  if [ -n "$PR_NUMBER" ]; then
    echo "PR 생성 성공: #$PR_NUMBER"
  else
    echo "PR 생성 실패"
  fi
else
  echo "PR 생성 스킵"
fi

echo ""
echo "================================"
echo "   !"
echo "================================"
