#!/bin/bash
# 변경사항 적용 상태 확인
# 사용: ./check-status.sh [--pr | --branch | --local]

set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
cd "$PROJECT_DIR"

MODE="${1:-all}"

# ──────────────────────────────────────
# 색상 정의
# ──────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# ──────────────────────────────────────
# 함수: PR 상태 확인
# ──────────────────────────────────────
check_pr_status() {
    echo -e "${BLUE}📊 PR 상태 확인${NC}"
    echo ""

    if ! command -v gh &>/dev/null; then
        echo -e "${RED}❌ gh CLI가 설치되지 않았습니다${NC}"
        return 1
    fi

    # 로컬 브랜치에 대한 PR 검색
    CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "main")
    PR_LIST=$(gh pr list --head "$CURRENT_BRANCH" --json number,title,state,isDraft --limit 5 2>/dev/null || echo "")

    if [ -z "$PR_LIST" ]; then
        echo -e "${YELLOW}ℹ️  현재 브랜치의 PR이 없습니다${NC}"
        echo "   브랜치: $CURRENT_BRANCH"
        return 0
    fi

    # PR 목록 출력
    echo "$PR_LIST" | jq -r '.[] |
        "PR #\(.number): \(.title) [\(.state)\(if .isDraft then " (Draft)" else "" end)]"'

    # 병합된 PR 확인
    echo ""
    echo -e "${BLUE}✅ 최근 병합된 PR${NC}"
    MERGED=$(gh pr list --state merged --limit 3 --json number,title,mergedAt 2>/dev/null || echo "")

    if [ -n "$MERGED" ]; then
        echo "$MERGED" | jq -r '.[] |
            "PR #\(.number): \(.title) (병합: \(.mergedAt | split("T")[0]))"' || echo "병합된 PR이 없습니다"
    fi
}

# ──────────────────────────────────────
# 함수: 로컬 브랜치 상태
# ──────────────────────────────────────
check_branch_status() {
    echo -e "${BLUE}🌿 브랜치 상태${NC}"
    echo ""

    CURRENT=$(git branch --show-current)
    echo -e "현재 브랜치: ${GREEN}$CURRENT${NC}"

    # 원격 상태
    if git remote -v | grep -q origin; then
        git fetch origin 2>/dev/null || true

        BEHIND=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo "0")
        AHEAD=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "0")

        if [ "$BEHIND" -gt 0 ]; then
            echo -e "📤 로컬 커밋 (미푸시): ${YELLOW}$BEHIND개${NC}"
        fi

        if [ "$AHEAD" -gt 0 ]; then
            echo -e "📥 원격 커밋 (미병합): ${YELLOW}$AHEAD개${NC}"
        fi

        if [ "$BEHIND" -eq 0 ] && [ "$AHEAD" -eq 0 ]; then
            echo -e "✅ main 브랜치와 동기화됨"
        fi
    fi

    # 스테이징된 파일
    STAGED=$(git diff --cached --name-only 2>/dev/null | wc -l)
    if [ "$STAGED" -gt 0 ]; then
        echo -e "📝 스테이징된 파일: ${YELLOW}$STAGED개${NC}"
    fi

    # 수정된 파일
    MODIFIED=$(git diff --name-only 2>/dev/null | wc -l)
    if [ "$MODIFIED" -gt 0 ]; then
        echo -e "⚠️  수정된 파일 (미스테이징): ${YELLOW}$MODIFIED개${NC}"
    fi

    # Untracked 파일
    UNTRACKED=$(git ls-files --others --exclude-standard 2>/dev/null | wc -l)
    if [ "$UNTRACKED" -gt 0 ]; then
        echo -e "❓ Untracked 파일: ${YELLOW}$UNTRACKED개${NC}"
    fi
}

# ──────────────────────────────────────
# 함수: 로컬 변경사항
# ──────────────────────────────────────
check_local_changes() {
    echo -e "${BLUE}💾 로컬 변경사항${NC}"
    echo ""

    # 최근 커밋
    echo -e "최근 커밋:"
    git log --oneline -3 2>/dev/null | sed 's/^/  /'

    echo ""

    # 변경 통계
    echo -e "변경 통계:"
    git diff --stat origin/main..HEAD 2>/dev/null || echo "  변경사항 없음"
}

# ──────────────────────────────────────
# 함수: 마이그레이션 상태
# ──────────────────────────────────────
check_migration_status() {
    echo -e "${BLUE}🔄 마이그레이션 상태${NC}"
    echo ""

    CURRENT=$(cat .claude/state/_schema_version.txt 2>/dev/null || echo "unknown")
    TARGET=$(cat .claude/migrations/_target_version.txt 2>/dev/null || echo "unknown")

    echo "현재 스키마: $CURRENT"
    echo "목표 스키마: $TARGET"

    if [ "$CURRENT" = "$TARGET" ]; then
        echo -e "✅ 스키마가 최신 버전입니다"
    else
        echo -e "${YELLOW}⚠️  마이그레이션 필요: $CURRENT → $TARGET${NC}"
        echo "다음 세션 시작 시 자동으로 마이그레이션됩니다."
    fi
}

# ──────────────────────────────────────
# 함수: 전체 현황
# ──────────────────────────────────────
check_all() {
    echo "========================================"
    echo "Service Flow Template — 상태 확인"
    echo "========================================"
    echo ""

    check_local_changes
    echo ""
    check_branch_status
    echo ""
    check_pr_status
    echo ""
    check_migration_status

    echo ""
    echo "========================================"
}

# ──────────────────────────────────────
# 메인 로직
# ──────────────────────────────────────
case "$MODE" in
    --pr)
        check_pr_status
        ;;
    --branch)
        check_branch_status
        ;;
    --local)
        check_local_changes
        ;;
    --migration)
        check_migration_status
        ;;
    *)
        check_all
        ;;
esac

echo ""
