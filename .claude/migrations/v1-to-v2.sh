#!/bin/bash
# Migration: v1 → v2
# 목적: gitignore 파일 구조 표준화 및 로컬 상태 초기화
# 개선 사항:
#   1. .user-identity, .gh-token 보호 확인
#   2. flows/ 디렉토리 상태 정리
#   3. .claude/state/ 초기화

set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
cd "$PROJECT_DIR"

echo "🔄 마이그레이션 시작: v1 → v2"
echo ""

# ──────────────────────────────────────
# 1. 사용자 신원 파일 보호 확인
# ──────────────────────────────────────
if [ -f ".user-identity" ]; then
    echo "✓ .user-identity 파일 발견"
    git update-index --skip-worktree .user-identity 2>/dev/null || true
    echo "  ✓ git skip-worktree 적용됨"
else
    echo "ℹ️  .user-identity 파일 없음 (초기 설정 필요)"
fi

# ──────────────────────────────────────
# 2. GitHub 토큰 파일 보호 확인
# ──────────────────────────────────────
if [ -f ".gh-token" ]; then
    echo "✓ .gh-token 파일 발견"
    chmod 600 .gh-token 2>/dev/null || true
    git update-index --skip-worktree .gh-token 2>/dev/null || true
    echo "  ✓ git skip-worktree 적용됨"
    echo "  ✓ 권한 설정됨 (600)"
else
    echo "ℹ️  .gh-token 파일 없음"
fi

# ──────────────────────────────────────
# 3. flows/ 디렉토리 상태 정리
# ──────────────────────────────────────
if [ -d "flows" ]; then
    echo "✓ flows/ 디렉토리 발견"

    # flows/.gitignore 확인
    if [ -f "flows/.gitignore" ]; then
        echo "  ✓ flows/.gitignore 이미 존재"
    else
        # flows/.gitignore 생성
        cat > flows/.gitignore <<EOF
# gitignore: Service Flow Template
# flows/ 디렉토리는 각 세션별로 생성되고 공유되지 않습니다.
# 공유 필요 시: git update-index --no-skip-worktree flows/

*
!.gitignore
!README.md
EOF
        echo "  ✓ flows/.gitignore 생성됨"
    fi

    # flows/ git 설정 확인
    if git check-ignore flows/ 2>/dev/null | grep -q flows; then
        echo "  ✓ flows/ gitignore 적용됨"
    else
        echo "  ⚠️  flows/ gitignore 재확인 권장"
    fi
else
    echo "ℹ️  flows/ 디렉토리 없음 (필요시 자동 생성됨)"
fi

# ──────────────────────────────────────
# 4. .claude/state/ 초기화 및 정리
# ──────────────────────────────────────
echo "✓ .claude/state/ 상태 정리 중..."

# 활성 플로우 상태 확인
if [ -f ".claude/state/_active_flow.txt" ]; then
    ACTIVE_FLOW=$(cat .claude/state/_active_flow.txt | tr -d '[:space:]')
    if [ -n "$ACTIVE_FLOW" ]; then
        echo "  ℹ️  활성 플로우 감지: $ACTIVE_FLOW"
    fi
fi

# 불필요한 캐시 정리
if [ -d ".claude/state/cache" ]; then
    rm -rf .claude/state/cache
    echo "  ✓ 캐시 정리됨"
fi

# ──────────────────────────────────────
# 5. 스키마 버전 업데이트
# ──────────────────────────────────────
echo "✓ 스키마 버전 업데이트 중..."
echo "v2" > .claude/state/_schema_version.txt
echo "  ✓ _schema_version.txt = v2"

# ──────────────────────────────────────
# 6. 마이그레이션 로그 기록
# ──────────────────────────────────────
MIGRATION_LOG=".claude/state/logs/migrations.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$TIMESTAMP] Migration v1→v2 completed" >> "$MIGRATION_LOG" 2>/dev/null || true

# ──────────────────────────────────────
# 완료
# ──────────────────────────────────────
echo ""
echo "✅ 마이그레이션 완료: v1 → v2"
echo ""
echo "📋 확인 항목:"
echo "   ✓ 사용자 신원 파일 보호"
echo "   ✓ GitHub 토큰 파일 보호"
echo "   ✓ flows/ 디렉토리 초기화"
echo "   ✓ 상태 파일 정리"
echo ""
