#!/bin/bash
set -e

echo ""
echo "================================"
echo "✅ 서비스 플로우 생성 완료!"
echo "================================"
echo ""

# 1️⃣ 플로우 정보
FLOW_NAME="${1:-my-flow}"
PROJECT_PATH="${2:-.}"

echo "📦 플로우: $FLOW_NAME"
echo "📂 경로: $PROJECT_PATH"
echo ""

# 2️⃣ 포트 정리 (3000 - Dev Server)
echo "🧹 포트 3000 정리 중..."
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
  lsof -ti:3000 | xargs kill -9 2>/dev/null || true
  sleep 2
fi
echo "✅ 포트 정리 완료"
echo ""

# 3️⃣ 개발 서버 시작
echo "🚀 개발 서버 실행 중 (localhost:3000)..."
cd "$PROJECT_PATH" 2>/dev/null || true
npm run dev > /tmp/dev-server.log 2>&1 &
DEV_SERVER_PID=$!
sleep 8

if ! kill -0 $DEV_SERVER_PID 2>/dev/null; then
  echo "❌ 개발 서버 시작 실패"
  cat /tmp/dev-server.log
  exit 1
fi

echo "✅ 개발 서버 실행 중"
echo ""

# 4️⃣ 브라우저 자동 오픈
echo "🌐 브라우저 자동 오픈..."
open "http://localhost:3000" 2>/dev/null || echo "🔗 http://localhost:3000 에서 확인하세요"
echo ""

# 5️⃣ 사용자 검증 대기
echo "👀 플로우 검증 중..."
echo "   개발 서버에서 기능을 확인하세요."
read -p "검증 완료? (y/n): " -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "❌ 검증 취소됨"
  kill $DEV_SERVER_PID 2>/dev/null || true
  exit 1
fi

# 6️⃣ 개발 서버 종료
echo "🛑 개발 서버 종료..."
kill $DEV_SERVER_PID 2>/dev/null || true
wait $DEV_SERVER_PID 2>/dev/null || true
echo ""

# 7️⃣ 품질 검증 실행 (Strict Mode)
echo "📊 품질 검증 시작 (Strict Mode)..."
echo ""

# Format
echo "✨ 포맷 정상화..."
npm run format
if [ $? -ne 0 ]; then
  echo "❌ 포맷 실패"
  exit 1
fi
echo "✅ 포맷 완료"
echo ""

# 린트
echo "📋 린트 검사 (에러 0개 필수)..."
npm run lint
if [ $? -ne 0 ]; then
  echo "❌ Lint 실패 - PR 생성 불가"
  exit 1
fi
echo "✅ Lint 통과"
echo ""

# 타입 체크
echo "🔤 타입 체크..."
npm run type-check
if [ $? -ne 0 ]; then
  echo "❌ Type Check 실패 - PR 생성 불가"
  exit 1
fi
echo "✅ Type Check 통과"
echo ""

# 테스트
echo "🧪 테스트 실행..."
npm run test
if [ $? -ne 0 ]; then
  echo "❌ Test 실패 - PR 생성 불가"
  exit 1
fi
echo "✅ Test 통과"
echo ""

# 8️⃣ 최종 검증 요약
echo "=========================================="
echo "✅ 품질 검증 완료 (Strict Mode 통과)"
echo "=========================================="
echo ""
echo "📊 검증 결과:"
echo "  [Format]      ✅ 코드 포맷 정상"
echo "  [Lint]        ✅ 에러 0개"
echo "  [Type-check]  ✅ 타입 검증 통과"
echo "  [Test]        ✅ 모든 테스트 통과"
echo ""
echo "🎉 완료! PR 생성 가능합니다."
echo "=========================================="
echo ""

# 9️⃣ Git 준비
echo "🔄 Git 변경사항 확인..."
git add flows/ 2>/dev/null || true
git status --short
echo ""

# 🔟 PR 생성 확인
echo "📝 PR 생성 준비..."
read -p "PR을 생성하시겠습니까? (y/n): " -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
  BRANCH_NAME="flow/$FLOW_NAME-$(date +%s)"
  git checkout -b "$BRANCH_NAME" 2>/dev/null || git switch -c "$BRANCH_NAME"
  git add flows/
  git commit -m "[flow] $FLOW_NAME 서비스 플로우 생성" 2>/dev/null || true

  gh pr create --title "[flow] $FLOW_NAME 서비스 플로우" \
    --body "## 요약\n- 새 플로우: $FLOW_NAME\n\n## 검증 (Strict Mode)\n- ✅ 포맷: 통과\n- ✅ 린트: 에러 0개\n- ✅ 타입체크: 통과\n- ✅ 테스트: 100% 통과\n- ✅ 개발 서버: 기능 검증 완료" \
    --base main 2>/dev/null || echo "PR 생성 스킵 (gh cli 필요)"

  echo "✅ PR 생성 완료"
else
  echo "ℹ️  PR 생성 스킵됨"
fi

echo ""
echo "================================"
echo "🎉 모든 작업 완료!"
echo "================================"
