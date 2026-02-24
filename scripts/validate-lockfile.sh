#!/bin/bash
# 의존성 lockfile 검증 스크립트
# package.json 변경 시 pnpm-lock.yaml이 업데이트되었는지 확인
# 용도: Pre-commit 훅, GitHub Actions, 수동 검증

set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
cd "$PROJECT_DIR"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ──────────────────────────────────────
# Git 상태 확인
# ──────────────────────────────────────
echo "검증: package.json vs pnpm-lock.yaml"
echo ""

# package.json이 수정되었는지 확인 (staged + unstaged)
if git diff --name-only HEAD | grep -q "package.json"; then
  PACKAGE_MODIFIED="HEAD"
elif git diff --cached --name-only | grep -q "package.json"; then
  PACKAGE_MODIFIED="staged"
elif git diff --name-only | grep -q "package.json"; then
  PACKAGE_MODIFIED="unstaged"
else
  PACKAGE_MODIFIED="no"
fi

# pnpm-lock.yaml이 수정되었는지 확인
if git diff --name-only HEAD | grep -q "pnpm-lock.yaml"; then
  LOCKFILE_MODIFIED="HEAD"
elif git diff --cached --name-only | grep -q "pnpm-lock.yaml"; then
  LOCKFILE_MODIFIED="staged"
elif git diff --name-only | grep -q "pnpm-lock.yaml"; then
  LOCKFILE_MODIFIED="unstaged"
else
  LOCKFILE_MODIFIED="no"
fi

# ──────────────────────────────────────
# 케이스 분석
# ──────────────────────────────────────
case "$PACKAGE_MODIFIED:$LOCKFILE_MODIFIED" in
  "no:no")
    # 변경사항 없음
    echo -e "${GREEN}✅ package.json 변경 없음${NC}"
    exit 0
    ;;

  "staged:staged"|"staged:HEAD"|"staged:unstaged")
    # package.json이 staged 상태이고 lockfile도 수정됨
    echo -e "${GREEN}✅ package.json과 pnpm-lock.yaml 모두 커밋 준비됨${NC}"
    exit 0
    ;;

  "unstaged:unstaged"|"unstaged:HEAD"|"unstaged:staged")
    # package.json이 unstaged 상태인데 lockfile도 있음
    echo -e "${GREEN}✅ package.json 변경 감지, pnpm-lock.yaml 업데이트됨${NC}"
    exit 0
    ;;

  "HEAD:HEAD"|"HEAD:staged"|"HEAD:unstaged")
    # 이미 커밋된 경우 (일반적이지 않음)
    echo -e "${GREEN}✅ 변경사항이 커밋됨${NC}"
    exit 0
    ;;

  "staged:no")
    # package.json이 커밋 대기 중인데 lockfile이 없음
    echo -e "${RED}❌ 오류: package.json이 커밋 대기 중이지만 pnpm-lock.yaml이 업데이트되지 않았습니다.${NC}"
    echo ""
    echo "해결 방법:"
    echo "  1. pnpm install 실행"
    echo "  2. git add pnpm-lock.yaml"
    echo "  3. git commit 다시 시도"
    echo ""
    echo "변경된 의존성:"
    git diff --cached package.json | grep -E '^\+.*"@' | sed 's/^+/  /' || true
    exit 1
    ;;

  "unstaged:no")
    # package.json이 수정되었는데 lockfile이 없음
    echo -e "${YELLOW}⚠️  경고: package.json이 수정되었지만 pnpm-lock.yaml이 업데이트되지 않았습니다.${NC}"
    echo ""
    echo "변경된 의존성:"
    git diff package.json | grep -E '^\+.*"@' | sed 's/^+/  /' || true
    echo ""
    echo "해결 방법:"
    echo "  pnpm install"
    exit 0
    ;;

  *)
    echo -e "${GREEN}✅ 검증 통과${NC}"
    exit 0
    ;;
esac
