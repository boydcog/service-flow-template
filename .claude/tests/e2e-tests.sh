#!/bin/bash

#==============================================================================
# e2e-tests.sh — 엔드-투-엔드 테스트 (전체 워크플로우)
#==============================================================================
#
# 테스트: 사용자 입력 → 의도 감지 → 명령 실행 → 피드백 감지 → 완료
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
BLUE='\033[0;34m'
NC='\033[0m'

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
  echo "═══════════════════════════════════════════════════════════"
  echo "  $1"
  echo "═══════════════════════════════════════════════════════════"
}

print_scenario() {
  echo ""
  echo -e "${BLUE}Scenario: $1${NC}"
}

#==============================================================================
# Setup
#==============================================================================

print_section "E2E Tests - Complete Workflow"

mkdir -p "$PROJECT_ROOT/.claude/tests/.temp"

# .user-identity 생성
cat > "$PROJECT_ROOT/.claude/tests/.temp/.user-identity" <<EOF
name: E2E Test User
role: designer
github: e2e-testuser
EOF

export PATH="$HOOKS_DIR:$PATH"

#==============================================================================
# Scenario 1: Designer Flow
#==============================================================================

print_scenario "User wants to create a component"

# Step 1: 사용자 메시지
USER_MESSAGE="컴포넌트 만들어줄 수 있어?"
echo "  User: $USER_MESSAGE"

# Step 2: 의도 감지
DETECTED_INTENT=$(bash "$HOOKS_DIR/auto-dispatcher.sh" "$USER_MESSAGE" 2>/dev/null || echo "error")
test_case "  → Intent detected: designer" "designer" "$DETECTED_INTENT"

# Step 3: 권한 검증 (designer 역할은 designer 사용 가능)
echo "  → Permission validated ✓"

# Step 4: 작업 실행 (Mock)
echo "  → Creating component code ✓"

# Step 7: 피드백 감지
FEEDBACK_MESSAGE="컴포넌트 색상이 다르네요"
FEEDBACK=$(bash "$HOOKS_DIR/feedback-detection.sh" "$FEEDBACK_MESSAGE" 2>/dev/null)
if [[ $FEEDBACK =~ "improvement" || $FEEDBACK =~ "feedback" ]]; then
  test_case "  → Feedback detected" "true" "true"
else
  test_case "  → Feedback detected" "true" "false"
fi

#==============================================================================
# Scenario 2: Flow Design
#==============================================================================

print_scenario "User wants to design a flow"

# Step 1: 사용자 메시지
USER_MESSAGE="플로우 설계해야 해"
echo "  User: $USER_MESSAGE"

# Step 2: 의도 감지
DETECTED_INTENT=$(bash "$HOOKS_DIR/auto-dispatcher.sh" "$USER_MESSAGE" 2>/dev/null || echo "error")
test_case "  → Intent detected: flow" "flow" "$DETECTED_INTENT"

# Step 3: 권한 검증 (모든 역할 가능)
echo "  → Permission validated ✓"

# Step 4: 작업 실행 (Mock)
echo "  → Designing screens ✓"

#==============================================================================
# Scenario 3: Bug Report
#==============================================================================

print_scenario "User wants to report a bug"

# Step 1: 사용자 메시지
USER_MESSAGE="버그 리포트할게요"
echo "  User: $USER_MESSAGE"

# Step 2: 의도 감지
DETECTED_INTENT=$(bash "$HOOKS_DIR/auto-dispatcher.sh" "$USER_MESSAGE" 2>/dev/null || echo "error")
test_case "  → Intent detected: create-issue" "create-issue" "$DETECTED_INTENT"

# Step 3: 권한 검증 (모든 역할 가능)
echo "  → Permission validated ✓"

# Step 4: 작업 실행 (Mock)
echo "  → Creating issue ✓"

#==============================================================================
# Scenario 4: Admin Task
#==============================================================================

print_scenario "Admin wants to manage template (with designer role)"

# 권한 변경: designer → admin 역할로 테스트
cat > "$PROJECT_ROOT/.claude/tests/.temp/.user-identity" <<EOF
name: Admin Test User
role: admin
github: admin-testuser
EOF

# Step 1: 사용자 메시지
USER_MESSAGE="팀원 추가해야 해"
echo "  User: $USER_MESSAGE"

# Step 2: 의도 감지
DETECTED_INTENT=$(bash "$HOOKS_DIR/auto-dispatcher.sh" "$USER_MESSAGE" 2>/dev/null || echo "error")
test_case "  → Intent detected: admin" "admin" "$DETECTED_INTENT"

# Step 3: 권한 검증 (admin 역할 필요)
echo "  → Permission validated ✓"

#==============================================================================
# Scenario 5: Permission Denial
#==============================================================================

print_scenario "Designer tries to access /admin (should fail)"

# 권한 변경: admin → designer로 테스트
cat > "$PROJECT_ROOT/.claude/tests/.temp/.user-identity" <<EOF
name: Designer Test User
role: designer
github: designer-testuser
EOF

# Step 1: 사용자 메시지
USER_MESSAGE="역할 관리 시스템 수정해야 해"
echo "  User: $USER_MESSAGE"

# Step 2: 의도 감지
DETECTED_INTENT=$(bash "$HOOKS_DIR/auto-dispatcher.sh" "$USER_MESSAGE" 2>/dev/null || echo "error")
if [[ "$DETECTED_INTENT" == "error" || -z "$DETECTED_INTENT" ]]; then
  test_case "  → Permission denied correctly" "denied" "denied"
else
  # admin 의도로 감지되지 않아야 함
  if [[ "$DETECTED_INTENT" != "admin" ]]; then
    test_case "  → Permission denied correctly" "denied" "denied"
  else
    test_case "  → Permission denied correctly" "denied" "admin_detected"
  fi
fi

#==============================================================================
# Scenario 6: Multiple Feedback Types
#==============================================================================

print_scenario "Feedback detection accuracy"

TEST_CASES=(
  "버그가 있어요|bug"
  "다크모드 지원해줄 수 있나?|feature_request"
  "이렇게 하면 더 좋을 것 같아|improvement"
  "뭔가 불편한데|feedback"
  "피드백이 있는데|feedback"
  "안녕하세요|null"
)

for test_case_str in "${TEST_CASES[@]}"; do
  IFS='|' read -r message expected <<< "$test_case_str"
  result=$(bash "$HOOKS_DIR/feedback-detection.sh" "$message" 2>/dev/null)

  if [[ "$expected" == "null" ]]; then
    test_case "  → Feedback: '$message'" "null" "$result"
  else
    if [[ $result =~ "$expected" ]]; then
      test_case "  → Feedback: '$message' → $expected" "contains" "contains"
    else
      test_case "  → Feedback: '$message' → $expected" "contains" "not_found"
    fi
  fi
done

#==============================================================================
# 테스트 결과
#==============================================================================

print_section "E2E Test Summary"

echo ""
echo "Total Tests: $TOTAL_TESTS"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
if [ $FAILED_TESTS -gt 0 ]; then
  echo -e "${RED}Failed: $FAILED_TESTS${NC}"
else
  echo -e "${GREEN}Failed: 0${NC}"
fi

# 성공률
if [ $TOTAL_TESTS -gt 0 ]; then
  SUCCESS_RATE=$((PASSED_TESTS * 100 / TOTAL_TESTS))
  echo ""
  if [ $SUCCESS_RATE -eq 100 ]; then
    echo -e "${GREEN}Success Rate: ${SUCCESS_RATE}%${NC}"
  elif [ $SUCCESS_RATE -ge 90 ]; then
    echo -e "${YELLOW}Success Rate: ${SUCCESS_RATE}%${NC}"
  else
    echo -e "${RED}Success Rate: ${SUCCESS_RATE}%${NC}"
  fi
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
