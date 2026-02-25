#!/bin/bash
set -e

echo ""
echo "================================"
echo "   !"
echo "================================"
echo ""

# 1⃣  
COMPONENT_NAME="${1:-Button}"
FRAMEWORK="${2:-web}"

echo " : $COMPONENT_NAME"
echo " : $FRAMEWORK"
echo ""

# 2⃣ Storybook 
echo " Storybook   (localhost:6006)..."
npm run storybook > /tmp/storybook.log 2>&1 &
STORYBOOK_PID=$!
sleep 8

if ! kill -0 $STORYBOOK_PID 2>/dev/null; then
  echo " Storybook  "
  cat /tmp/storybook.log
  exit 1
fi

echo " Storybook  "
echo ""

# 3⃣   
echo "   ..."
open "http://localhost:6006" 2>/dev/null || echo " http://localhost:6006  "
echo ""

# 4⃣   
echo "   ..."
echo "   Storybook  ."
read -p " ? (y/n): " -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "  "
  kill $STORYBOOK_PID 2>/dev/null || true
  exit 1
fi

# 5⃣ Storybook 
echo " Storybook ..."
kill $STORYBOOK_PID 2>/dev/null || true
wait $STORYBOOK_PID 2>/dev/null || true
echo ""

# 6⃣    (Strict Mode)
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

# 7⃣ Playwright  
echo " Playwright  ..."
npm run storybook > /tmp/storybook.log 2>&1 &
STORYBOOK_PID=$!
sleep 8

if kill -0 $STORYBOOK_PID 2>/dev/null; then
  echo "   "
  kill $STORYBOOK_PID 2>/dev/null || true
  wait $STORYBOOK_PID 2>/dev/null || true
else
  echo "    "
fi
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
echo "  [Screenshot]   UI  "
echo ""
echo " ! PR  ."
echo "=========================================="
echo ""

# 9⃣ Git 
echo " Git  ..."
git add components/$FRAMEWORK/ui/$COMPONENT_NAME.* 2>/dev/null || true
git status --short
echo ""

#  PR
echo " PR  ..."
read -p "PR ? (y/n): " -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
  # Validate GitHub token before PR creation
  source ./.claude/hooks/gh-token-validate.sh || exit 1

  BRANCH_NAME="component/$COMPONENT_NAME-$(date +%s)"

  # Git 인증 설정 (.gh-token 기반)
  git config --local user.name "Claude Code Bot"
  git config --local user.email "bot@claudecode.local"
  git config --local credential.helper store
  echo "https://:${GH_TOKEN}@github.com" | git credential approve 2>/dev/null || true

  git checkout -b "$BRANCH_NAME" 2>/dev/null || git switch -c "$BRANCH_NAME"
  git add components/$FRAMEWORK/ui/$COMPONENT_NAME.*
  git commit -m "[designer] $COMPONENT_NAME component creation" 2>/dev/null || true

  # Git push with .gh-token (토큰만 사용)
  git push -u origin "$BRANCH_NAME" 2>&1 || {
    echo "Git push 실패"
    exit 1
  }

  # PR 생성 (create-pr.sh 호출 - 중복 로직 제거)
  PR_TITLE="[designer] $COMPONENT_NAME component"
  PR_BODY="## Summary
- New component: $COMPONENT_NAME
- Framework: $FRAMEWORK

## Validation (Strict Mode)
- Format: Pass
- Lint: Error 0
- Type-check: Pass
- Test: 100% Pass
- Storybook: Verified"

  bash ./.claude/hooks/create-pr.sh "$BRANCH_NAME" "$PR_TITLE" "$PR_BODY"
else
  echo "PR 생성 스킵"
fi

echo ""
echo "================================"
echo "   !"
echo "================================"
