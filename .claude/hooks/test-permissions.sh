#!/bin/bash
# 권한 검증 테스트 스크립트
# 모든 역할과 스킬 조합 테스트

set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
cd "$PROJECT_DIR"

# ──────────────────────────────────────
# 색상 정의
# ──────────────────────────────────────
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ──────────────────────────────────────
# 테스트 결과 추적
# ──────────────────────────────────────
PASSED=0
FAILED=0

test_permission() {
    local skill="$1"
    local role="$2"
    local expected="$3"

    if bash .claude/hooks/verify-permissions.sh "$skill" "$role" &>/dev/null; then
        result="PASS"
    else
        result="FAIL"
    fi

    if [ "$result" = "$expected" ]; then
        echo -e "${GREEN}✅${NC} /$skill (역할: $role) → $result ${GREEN}예상 대로${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}❌${NC} /$skill (역할: $role) → $result ${RED}예상: $expected${NC}"
        FAILED=$((FAILED + 1))
    fi
}

# ──────────────────────────────────────
# 테스트 케이스
# ──────────────────────────────────────
echo ""
echo "=========================================="
echo "권한 검증 테스트 시작"
echo "=========================================="
echo ""

# Admin 역할 테스트
echo -e "${BLUE}📋 Admin 역할 테스트${NC}"
test_permission "admin" "admin" "PASS"
test_permission "designer" "admin" "PASS"
test_permission "flow" "admin" "PASS"
test_permission "setup" "admin" "PASS"
test_permission "create-issue" "admin" "PASS"
test_permission "admin-status" "admin" "PASS"
echo ""

# Developer 역할 테스트
echo -e "${BLUE}📋 Developer 역할 테스트${NC}"
test_permission "admin" "developer" "PASS"
test_permission "designer" "developer" "PASS"
test_permission "flow" "developer" "PASS"
test_permission "setup" "developer" "PASS"
test_permission "create-issue" "developer" "PASS"
test_permission "admin-status" "developer" "PASS"
echo ""

# Designer 역할 테스트
echo -e "${BLUE}📋 Designer 역할 테스트${NC}"
test_permission "admin" "designer" "FAIL"
test_permission "designer" "designer" "PASS"
test_permission "flow" "designer" "PASS"
test_permission "setup" "designer" "PASS"
test_permission "create-issue" "designer" "PASS"
test_permission "admin-status" "designer" "PASS"
echo ""

# PM 역할 테스트
echo -e "${BLUE}📋 PM 역할 테스트${NC}"
test_permission "admin" "pm" "FAIL"
test_permission "designer" "pm" "FAIL"
test_permission "flow" "pm" "PASS"
test_permission "setup" "pm" "PASS"
test_permission "create-issue" "pm" "PASS"
test_permission "admin-status" "pm" "PASS"
echo ""

# ──────────────────────────────────────
# 결과 요약
# ──────────────────────────────────────
echo "=========================================="
echo "테스트 결과"
echo "=========================================="
echo ""

TOTAL=$((PASSED + FAILED))
PERCENTAGE=$((PASSED * 100 / TOTAL))

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ 모든 테스트 통과!${NC}"
    echo "통과: $PASSED / $TOTAL ($PERCENTAGE%)"
else
    echo -e "${RED}❌ 테스트 실패${NC}"
    echo "통과: $PASSED"
    echo "실패: $FAILED"
    echo "합계: $TOTAL"
fi

echo ""

exit $FAILED
