#!/bin/bash
set -e

echo "품질 검증 프로세스 (Strict Mode) 시작..."
echo ""

# 1단계 Lint (ESLint - Error 레벨)
echo "[1] Lint 검사 중..."
npm run lint
if [ $? -ne 0 ]; then
  echo "[FAIL] Lint 실패 (에러 0개 필수)"
  exit 1
fi
echo "[PASS] Lint 통과"
echo ""

# 2단계 Type Check (TypeScript - Strict)
echo "[2] Type Check 중..."
npm run type-check
if [ $? -ne 0 ]; then
  echo "[FAIL] Type Check 실패"
  exit 1
fi
echo "[PASS] Type Check 통과"
echo ""

# 3단계 Format (Prettier)
echo "[3] 코드 포맷 정상화 중..."
npm run format
echo "[PASS] 포맷 자동 수정 완료"
echo ""

# 4단계 Test (Unit Test)
echo "[4] 테스트 실행 중..."
npm run test
if [ $? -ne 0 ]; then
  echo "[FAIL] 테스트 실패"
  exit 1
fi
echo "[PASS] 테스트 통과"
echo ""

# 5단계 Playwright Screenshot Validation
echo "[5] Playwright 스크린샷 검증 중..."
bash scripts/playwright-validate.sh
if [ $? -ne 0 ]; then
  echo "[FAIL] 스크린샷 검증 실패"
  exit 1
fi
echo "[PASS] 스크린샷 검증 통과"
echo ""

echo "=========================================="
echo "[SUCCESS] 모든 검증 완료 (Strict Mode 통과)"
echo "=========================================="
echo ""

echo "검증 결과:"
echo "  [Lint]        PASS - 에러 0개"
echo "  [Type-check]  PASS - 타입 검증 통과"
echo "  [Format]      PASS - 코드 포맷 정상"
echo "  [Test]        PASS - 모든 테스트 통과"
echo "  [Screenshot]  PASS - UI 검증 완료"
echo ""
echo "완료! PR 생성 가능합니다."
