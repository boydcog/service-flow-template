#!/bin/bash

#==============================================================================
# unit-tests.sh — 단위 테스트 (Intent Detection, Permission, Feedback)
#==============================================================================
#
# 테스트: auto-dispatcher.sh, permission-validation.sh, feedback-detection.sh
#
#==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
HOOKS_DIR="$PROJECT_ROOT/.claude/hooks"

# 색상
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# 테스트 통계
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

#==============================================================================
# 테스트 유틸리티
#==============================================================================

test_case() {
  local name="$1"
  local expected="$2"
  local actual="$3"

  TOTAL_TESTS=$((TOTAL_TESTS + 1))

  if [ "$expected" = "$actual" ]; then
    echo -e "${GREEN}✓${NC} $name"
    PASSED_TESTS=$((PASSED_TESTS + 1))
  else
    echo -e "${RED}✗${NC} $name"
    echo "  Expected: $expected"
    echo "  Actual: $actual"
    FAILED_TESTS=$((FAILED_TESTS + 1))
  fi
}

print_section() {
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  $1"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

#==============================================================================
# Intent Detection 테스트
#==============================================================================

print_section "1. Intent Detection Tests (auto-dispatcher.sh)"

# Setup: .user-identity 파일 생성
mkdir -p "$PROJECT_ROOT/.claude/tests/.temp"
cat > "$PROJECT_ROOT/.claude/tests/.temp/.user-identity" <<EOF
name: Test User
role: designer
github: testuser
EOF

export PATH="$HOOKS_DIR:$PATH"

# 테스트 1: Designer 의도 감지
result=$(bash "$HOOKS_DIR/auto-dispatcher.sh" "컴포넌트 만들어줄 수 있어?" 2>/dev/null || echo "error")
test_case "Designer intent detection" "designer" "$result"

# 테스트 2: Flow 의도 감지
result=$(bash "$HOOKS_DIR/auto-dispatcher.sh" "플로우 설계해야 해" 2>/dev/null || echo "error")
test_case "Flow intent detection" "flow" "$result"

# 테스트 3: Create-Issue 의도 감지
result=$(bash "$HOOKS_DIR/auto-dispatcher.sh" "버그 제보하고 싶어" 2>/dev/null || echo "error")
test_case "Create-Issue intent detection" "create-issue" "$result"

# 테스트 4: 명시적 명령어 감지
result=$(bash "$HOOKS_DIR/auto-dispatcher.sh" "/designer" 2>/dev/null || echo "error")
test_case "Explicit command detection" "designer" "$result"

#==============================================================================
# Permission Validation 테스트
#==============================================================================

print_section "2. Permission Validation Tests"

# Designer (admin 역할로 테스트)
cat > "$PROJECT_ROOT/.claude/tests/.temp/.user-identity" <<EOF
name: Admin User
role: admin
github: adminuser
EOF

# designer 커맨드는 admin도 사용 가능 (admin은 designer 권한 포함)
# 이 테스트는 스크립트 직접 실행이 아니라 권한 검증 로직을 테스트

echo -e "${YELLOW}Note:${NC} Permission validation requires environment setup"
echo "  Tested via: /designer, /flow, /create-issue, /admin commands"

#==============================================================================
# Feedback Detection 테스트
#==============================================================================

print_section "3. Feedback Detection Tests (feedback-detection.sh)"

# 테스트 1: 버그 감지
result=$(bash "$HOOKS_DIR/feedback-detection.sh" "버그가 있어요" 2>/dev/null)
if [[ $result =~ "bug" ]]; then
  test_case "Bug feedback detection" "contains_bug" "contains_bug"
else
  test_case "Bug feedback detection" "contains_bug" "not_detected"
fi

# 테스트 2: 기능 요청 감지
result=$(bash "$HOOKS_DIR/feedback-detection.sh" "다크모드 지원해줄 수 있나요?" 2>/dev/null)
if [[ $result =~ "feature_request" ]]; then
  test_case "Feature request detection" "contains_feature" "contains_feature"
else
  test_case "Feature request detection" "contains_feature" "not_detected"
fi

# 테스트 3: 개선 제안 감지
result=$(bash "$HOOKS_DIR/feedback-detection.sh" "이렇게 하면 더 좋을 것 같아" 2>/dev/null)
if [[ $result =~ "improvement" ]]; then
  test_case "Improvement suggestion detection" "contains_improvement" "contains_improvement"
else
  test_case "Improvement suggestion detection" "contains_improvement" "not_detected"
fi

# 테스트 4: 피드백 없음 감지
result=$(bash "$HOOKS_DIR/feedback-detection.sh" "안녕하세요" 2>/dev/null)
test_case "No feedback detection" "null" "$result"

#==============================================================================
# 테스트 결과
#==============================================================================

print_section "Test Summary"

echo ""
echo "Total Tests: $TOTAL_TESTS"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
if [ $FAILED_TESTS -gt 0 ]; then
  echo -e "${RED}Failed: $FAILED_TESTS${NC}"
else
  echo -e "${GREEN}Failed: 0${NC}"
fi

echo ""

# 정리
rm -rf "$PROJECT_ROOT/.claude/tests/.temp"

# 종료 코드
if [ $FAILED_TESTS -gt 0 ]; then
  exit 1
else
  exit 0
fi
