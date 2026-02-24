#!/bin/bash
# 권한 검증 유틸리티
# 사용: verify_permission <skill_name> [user_role]
# 예: verify_permission "admin" "designer"
#     verify_permission "/admin"

set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
cd "$PROJECT_DIR"

# ──────────────────────────────────────
# 인자 검증
# ──────────────────────────────────────
if [ $# -lt 1 ]; then
    echo "❌ 사용법: verify_permission <skill> [role]"
    echo "예: verify_permission admin"
    echo "예: verify_permission admin designer"
    exit 1
fi

SKILL_NAME="${1#/}"  # /admin → admin
USER_ROLE="${2:-unknown}"

# ──────────────────────────────────────
# 사용자 신원 로드 (인자가 없으면)
# ──────────────────────────────────────
if [ "$USER_ROLE" = "unknown" ] && [ -f .user-identity ]; then
    USER_ROLE=$(grep '^role:' .user-identity 2>/dev/null | sed 's/role: //' | tr -d '\n' || echo "unknown")
fi

# ──────────────────────────────────────
# roles.yaml에서 허용된 역할 추출
# ──────────────────────────────────────
ROLES_FILE=".claude/manifests/roles.yaml"

if [ ! -f "$ROLES_FILE" ]; then
    echo "❌ roles.yaml을 찾을 수 없습니다: $ROLES_FILE"
    exit 1
fi

# 스킬별 필요 역할 정의 (CLAUDE.md 기반)
case "$SKILL_NAME" in
    admin)
        REQUIRED_ROLES="admin developer"
        ;;
    designer)
        REQUIRED_ROLES="admin developer designer"
        ;;
    flow)
        REQUIRED_ROLES="admin developer designer pm"
        ;;
    setup)
        REQUIRED_ROLES="admin developer designer pm"
        ;;
    create-issue)
        REQUIRED_ROLES="admin developer designer pm"
        ;;
    admin-status)
        REQUIRED_ROLES="admin developer designer pm"
        ;;
    *)
        echo "❌ 알 수 없는 스킬: $SKILL_NAME"
        exit 1
        ;;
esac

# ──────────────────────────────────────
# 권한 검증
# ──────────────────────────────────────
if echo "$REQUIRED_ROLES" | grep -qw "$USER_ROLE"; then
    echo "✅ 권한 확인: /$SKILL_NAME 사용 가능 (역할: $USER_ROLE)"
    exit 0
else
    echo "❌ 권한 없음"
    echo ""
    echo "필요 역할: $REQUIRED_ROLES"
    echo "현재 역할: $USER_ROLE"
    echo ""
    echo "요청: /$SKILL_NAME 사용"
    exit 1
fi
