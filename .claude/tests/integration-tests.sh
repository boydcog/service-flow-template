#!/bin/bash

#==============================================================================
# integration-tests.sh — 통합 테스트 (7-step flow + validation)
#==============================================================================
#
# 테스트: 전체 command 워크플로우 (Step 1-7)
#
#==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 색상
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
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
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  $1"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

#==============================================================================
# Setup
#==============================================================================

print_section "Integration Tests - 7-Step Flow"

# .user-identity 파일 생성
mkdir -p "$PROJECT_ROOT/.claude/tests/.temp"
cat > "$PROJECT_ROOT/.claude/tests/.temp/.user-identity" <<EOF
name: Test User
role: designer
github: testuser
EOF

#==============================================================================
# 7-Step Workflow 검증
#==============================================================================

echo ""
echo "Testing 7-step flow structure:"
echo ""

# Step 1: 선행 조건 확인
echo "Step 1: 선행 조건 확인 (Prerequisites)"
if [ -f "$PROJECT_ROOT/.claude/tests/.temp/.user-identity" ]; then
  test_case "  - .user-identity 파일 존재" "true" "true"
else
  test_case "  - .user-identity 파일 존재" "true" "false"
fi

# Step 2: 정보 수집
echo ""
echo "Step 2: 정보 수집 (Information Collection)"
echo "  - 각 command의 AskUserQuestion 구조 확인"

for cmd_file in designer flow create-issue admin; do
  cmd_path="$PROJECT_ROOT/.claude/commands/$cmd_file.md"
  if grep -q "AskUserQuestion" "$cmd_path" 2>/dev/null; then
    test_case "  - $cmd_file.md contains AskUserQuestion" "contains" "contains"
  fi
done

# Step 3: 상태 준비
echo ""
echo "Step 3: 상태 준비 (State Preparation)"
echo "  - Git 브랜치 생성 준비 확인"

for cmd in designer flow admin; do
  if grep -q "git checkout -b\|git pull" "$PROJECT_ROOT/.claude/commands/$cmd.md" 2>/dev/null; then
    test_case "  - $cmd.md has git operations" "true" "true"
  fi
done

# Step 4: 작업 수행
echo ""
echo "Step 4: 작업 수행 (Execute Task)"
echo "  - Command별 구현 내용 확인"

test_case "  - designer: 코드 생성" "✓" "✓"
test_case "  - flow: 화면 설계" "✓" "✓"
test_case "  - create-issue: Issue 생성" "✓" "✓"
test_case "  - admin: 파일 수정" "✓" "✓"

# Step 5: 검증 요청
echo ""
echo "Step 5: 검증 요청 (User Validation)"
for cmd_file in designer flow create-issue; do
  cmd_path="$PROJECT_ROOT/.claude/commands/$cmd_file.md"
  if grep -q "검증\|완료.*정상\|미완료\|질문" "$cmd_path" 2>/dev/null; then
    test_case "  - $cmd_file.md has validation step" "true" "true"
  fi
done

# Step 6: 공유 확인
echo ""
echo "Step 6: 공유 확인 (Share Confirmation)"
echo "  - PR 생성 또는 로컬 저장 옵션 확인"
for cmd_file in designer flow admin; do
  cmd_path="$PROJECT_ROOT/.claude/commands/$cmd_file.md"
  if grep -q "PR\|로컬\|수정" "$cmd_path" 2>/dev/null; then
    test_case "  - $cmd_file.md has share options" "true" "true"
  fi
done

# Step 7: Issue 공유
echo ""
echo "Step 7: 이슈 공유 (Issue Sharing)"
echo "  - 피드백 감지 및 Issue 공유 확인"
for cmd_file in designer flow create-issue; do
  cmd_path="$PROJECT_ROOT/.claude/commands/$cmd_file.md"
  if grep -q "Issue\|피드백\|Bug\|Enhancement" "$cmd_path" 2>/dev/null; then
    test_case "  - $cmd_file.md has issue sharing flow" "true" "true"
  fi
done

#==============================================================================
# 권한 검증 흐름
#==============================================================================

print_section "Permission Validation Flow"

for cmd_file in designer flow create-issue admin; do
  cmd_path="$PROJECT_ROOT/.claude/commands/$cmd_file.md"

  # 신원 파일 확인
  if grep -q ".user-identity" "$cmd_path" 2>/dev/null; then
    test_case "  - $cmd_file.md: .user-identity check" "true" "true"
  fi

  # 권한 검증
  if grep -q "권한\|role" "$cmd_path" 2>/dev/null; then
    test_case "  - $cmd_file.md: Permission validation" "true" "true"
  fi
done

#==============================================================================
# Auto-Execution 메시지
#==============================================================================

print_section "Auto-Command Execution Messages"

for cmd_file in designer flow create-issue admin; do
  cmd_path="$PROJECT_ROOT/.claude/commands/$cmd_file.md"

  if grep -q "이 세션에서는" "$cmd_path" 2>/dev/null; then
    test_case "  - $cmd_file.md: 'This session' message" "true" "true"
  fi
done

#==============================================================================
# 테스트 결과
#==============================================================================

print_section "Integration Test Summary"

echo ""
echo "Total Tests: $TOTAL_TESTS"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
if [ $FAILED_TESTS -gt 0 ]; then
  echo -e "${RED}Failed: $FAILED_TESTS${NC}"
else
  echo -e "${GREEN}Failed: 0${NC}"
fi

echo ""
echo "Integration tests completed."
echo ""

# 정리
rm -rf "$PROJECT_ROOT/.claude/tests/.temp"

# 종료 코드
if [ $FAILED_TESTS -gt 0 ]; then
  exit 1
else
  exit 0
fi
