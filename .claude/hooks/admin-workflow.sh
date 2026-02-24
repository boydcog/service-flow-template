#!/bin/bash
# Admin Workflow: 템플릿 관리 작업 완료 후 PR 자동 생성
# 사용: ./admin-workflow.sh <action> <description>
# 예: ./admin-workflow.sh "팀원 추가" "홍길동 (designer) 추가"

set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
cd "$PROJECT_DIR"

# ──────────────────────────────────────
# 인자 검증
# ──────────────────────────────────────
if [ $# -lt 2 ]; then
    echo "❌ 사용법: ./admin-workflow.sh <action> <description>"
    exit 1
fi

ACTION="$1"
DESCRIPTION="$2"
USER_NAME="${3:-admin}"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# ──────────────────────────────────────
# 브랜치 생성 및 전환
# ──────────────────────────────────────
BRANCH_NAME="admin/$(date +%s)"
echo "🌿 브랜치 생성: $BRANCH_NAME"

if ! git checkout -b "$BRANCH_NAME" 2>/dev/null; then
    echo "❌ 브랜치 생성 실패"
    exit 1
fi

# ──────────────────────────────────────
# CHANGELOG 업데이트 (있는 경우)
# ──────────────────────────────────────
if [ -f "CHANGELOG.md" ]; then
    echo "📝 CHANGELOG 업데이트 중..."

    # CHANGELOG 맨 앞에 추가
    TEMP_CHANGELOG=$(mktemp)
    cat > "$TEMP_CHANGELOG" <<EOF
## [Unreleased]

### Added
- $DESCRIPTION (by $USER_NAME)

### Modified
- Updated at $TIMESTAMP

---

EOF
    cat CHANGELOG.md >> "$TEMP_CHANGELOG"
    mv "$TEMP_CHANGELOG" CHANGELOG.md

    git add CHANGELOG.md
    echo "✓ CHANGELOG 업데이트됨"
fi

# ──────────────────────────────────────
# 변경사항 커밋
# ──────────────────────────────────────
echo "📤 변경사항 커밋 중..."

git add -A || true

COMMIT_MSG="admin: $ACTION"
if git diff --cached --quiet; then
    echo "⚠️  커밋할 변경사항이 없습니다"
else
    git commit -m "$COMMIT_MSG" || true
fi

# ──────────────────────────────────────
# PR 생성
# ──────────────────────────────────────
PR_TITLE="[admin] $USER_NAME: $ACTION"
PR_BODY="## 변경 사항

$DESCRIPTION

**작성자**: $USER_NAME
**시간**: $TIMESTAMP

---

### 체크리스트

- [ ] 변경사항이 명확합니다
- [ ] CHANGELOG에 기록했습니다
- [ ] 다른 admin에게 검토 요청했습니다

### 리뷰

- [ ] admin 승인
- [ ] developer 승인 (필요 시)
"

echo "📝 PR 생성 중: $PR_TITLE"

bash "$PROJECT_DIR/.claude/hooks/create-pr.sh" "$BRANCH_NAME" "$PR_TITLE" "$PR_BODY"

# ──────────────────────────────────────
# 상태 기록
# ──────────────────────────────────────
ADMIN_LOG=".claude/state/logs/admin-actions.log"
echo "[$TIMESTAMP] $ACTION | $BRANCH_NAME" >> "$ADMIN_LOG" 2>/dev/null || true

echo ""
echo "✅ Admin 워크플로우 완료"
echo ""
