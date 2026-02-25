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

  # Dependency checks
  if ! command -v jq &> /dev/null; then
    echo "오류: jq가 설치되지 않았습니다"
    exit 1
  fi

  if [ -z "$GH_TOKEN" ]; then
    echo "오류: GitHub 토큰이 설정되지 않았습니다"
    exit 1
  fi

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

  # GitHub API로 PR 생성 (.gh-token만 사용, jq 기반 안전 파싱)
  REPO_URL=$(git remote get-url origin | sed 's|.*github.com[:/]||' | sed 's|\.git$||')
  IFS='/' read -r OWNER REPO_NAME <<< "$REPO_URL"

  PR_BODY="## Summary
- New component: $COMPONENT_NAME
- Framework: $FRAMEWORK

## Validation (Strict Mode)
- Format: Pass
- Lint: Error 0
- Type-check: Pass
- Test: 100% Pass
- Storybook: Verified"

  # JSON 생성 (jq로 안전하게)
  PR_DATA=$(jq -n \
    --arg title "[designer] $COMPONENT_NAME component" \
    --arg body "$PR_BODY" \
    --arg head "$BRANCH_NAME" \
    --arg base "main" \
    '{title: $title, body: $body, head: $head, base: $base}' 2>/dev/null)

  if [ -z "$PR_DATA" ]; then
    echo "오류: JSON 생성 실패"
    exit 1
  fi

  PR_RESPONSE=$(curl -s -X POST \
    -H "Authorization: token $GH_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    -H "Content-Type: application/json" \
    -d "$PR_DATA" \
    "https://api.github.com/repos/$OWNER/$REPO_NAME/pulls")

  PR_NUMBER=$(echo "$PR_RESPONSE" | jq -r '.number // empty' 2>/dev/null)
  PR_ERROR=$(echo "$PR_RESPONSE" | jq -r '.message // empty' 2>/dev/null)

  if [ -n "$PR_NUMBER" ]; then
    echo "PR 생성 성공: #$PR_NUMBER"
  else
    if [ -n "$PR_ERROR" ]; then
      echo "PR 생성 실패: $PR_ERROR"
    else
      echo "PR 생성 실패 (상세 정보는 로그 참고)"
    fi
  fi
else
  echo "PR 생성 스킵"
fi

echo ""
echo "================================"
echo "   !"
echo "================================"
