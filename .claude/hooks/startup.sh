#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
cd "$PROJECT_DIR"

STATUS=""

echo "=== Service Flow Template — Session Start ==="
echo ""

# ──────────────────────────────────────
# 1. 의존성 감지
# ──────────────────────────────────────
HAS_GIT="false"
HAS_GH="false"
HAS_BREW="false"

command -v git &>/dev/null && HAS_GIT="true"
command -v gh &>/dev/null && HAS_GH="true"
command -v brew &>/dev/null && HAS_BREW="true"

if [ "$HAS_GIT" = "true" ]; then
  STATUS="$STATUS
OK git 설치됨"
else
  STATUS="$STATUS
FAIL git 미설치"
fi

if [ "$HAS_GH" = "true" ]; then
  STATUS="$STATUS
OK gh CLI 설치됨"
else
  STATUS="$STATUS
WARN gh CLI 미설치"
fi

# ──────────────────────────────────────
# 2. 사용자 신원 & Git Remote 로드
# ──────────────────────────────────────
USER_NAME=""
USER_ROLE="unknown"
USER_GITHUB=""
USER_COMMANDS=""
GIT_REMOTE_URL=""

if [ -f .user-identity ]; then
  USER_NAME=$(grep '^name:' .user-identity 2>/dev/null | sed 's/name: //' | tr -d '\n' || echo "")
  USER_ROLE=$(grep '^role:' .user-identity 2>/dev/null | sed 's/role: //' | tr -d '\n' || echo "unknown")
  USER_GITHUB=$(grep '^github:' .user-identity 2>/dev/null | sed 's/github: //' | tr -d '\n' || echo "")

  echo "✅ 안녕하세요, $USER_NAME ($USER_ROLE)!"
  STATUS="$STATUS
OK 사용자: $USER_NAME ($USER_ROLE)"

  # GitHub 사용자명으로 repository URL 구성
  if [ -n "$USER_GITHUB" ]; then
    GIT_REMOTE_URL="git@github.com:${USER_GITHUB}/service-flow-template.git"
  fi

  # 역할별 권한 로드 (roles.yaml 기반)
  if [ -f ".claude/manifests/roles.yaml" ]; then
    # 사용자 역할에 해당하는 commands 추출
    USER_COMMANDS=$(grep -A 10 "^  $USER_ROLE:" ".claude/manifests/roles.yaml" 2>/dev/null | grep "commands:" | sed 's/.*commands: \[//' | sed 's/\].*//' || echo "")

    if [ -n "$USER_COMMANDS" ]; then
      echo "📋 권한: $USER_COMMANDS"
      STATUS="$STATUS
OK 권한 로드: $USER_ROLE"
    fi
  fi
else
  STATUS="$STATUS
WARN 사용자 미설정"
fi

# ──────────────────────────────────────
# 3. GH 토큰 로드 및 Git 인증 설정
# ──────────────────────────────────────
GH_TOKEN_LOADED="false"
if [ -f .gh-token ]; then
  TOKEN_CONTENT=$(cat .gh-token | tr -d '[:space:]')
  if [ -n "$TOKEN_CONTENT" ]; then
    chmod 600 .gh-token 2>/dev/null || true
    export GH_TOKEN="$TOKEN_CONTENT"
    GH_TOKEN_LOADED="true"

    # Git 인증 설정 (.gh-token 기반)
    git config --local user.name "Claude Code Bot"
    git config --local user.email "bot@claudecode.local"
    git config --local credential.helper store

    # Git credential에 토큰 정보 저장 (.gh-token만 사용)
    echo "https://:${GH_TOKEN}@github.com" | git credential approve 2>/dev/null || true

    echo "✅ GitHub 토큰 로드됨"
    echo "✅ Git 인증 설정 완료 (.gh-token 기반)"
    STATUS="$STATUS
OK GitHub 토큰 로드"
  else
    STATUS="$STATUS
WARN .gh-token 파일이 비어있음"
  fi
else
  STATUS="$STATUS
FAIL GitHub 토큰 없음"
fi

# ──────────────────────────────────────
# 4. 로컬 파일 보호 (git pull에서 덮어쓰기 방지)
# ──────────────────────────────────────
if [ "$HAS_GIT" = "true" ]; then
  if [ -f .user-identity ]; then
    git update-index --skip-worktree .user-identity 2>/dev/null || true
  fi
  if [ -f .gh-token ]; then
    git update-index --skip-worktree .gh-token 2>/dev/null || true
  fi
fi

# ──────────────────────────────────────
# 5. Git 초기화 및 remote 설정 (HTTPS 우선)
# ──────────────────────────────────────
GIT_READY="false"
CURRENT_BRANCH="main"

if [ "$HAS_GIT" = "true" ]; then
  # ──────────────────────────────────────
  # 5.1. Git 저장소 초기화 또는 확인
  # ──────────────────────────────────────
  if [ ! -d ".git" ]; then
    echo "Git 저장소를 초기화 중입니다..."
    git init 2>/dev/null || true
    GIT_READY="true"
    CURRENT_BRANCH="main"
  else
    GIT_READY="true"
    CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "main")
  fi

  # ──────────────────────────────────────
  # 5.2. Git Remote 설정 또는 확인
  # ──────────────────────────────────────
  CURRENT_REMOTE=$(git config --get remote.origin.url 2>/dev/null || echo "")

  if [ -z "$CURRENT_REMOTE" ]; then
    # Remote가 없으면 설정
    REMOTE_URL=""

    # 우선순위 1: .user-identity에서 GitHub 사용자명 사용
    if [ -n "$GIT_REMOTE_URL" ]; then
      REMOTE_URL="$GIT_REMOTE_URL"
    # 우선순위 2: .git-remote-url 파일
    elif [ -f ".git-remote-url" ]; then
      REMOTE_URL=$(cat .git-remote-url | tr -d '[:space:]')
    # 우선순위 3: GitHub API (gh token 있을 때)
    elif [ -f ".gh-token" ] && [ "$HAS_GH" = "true" ]; then
      GH_TOKEN=$(cat .gh-token | tr -d '[:space:]')
      REMOTE_URL=$(curl -s -H "Authorization: token $GH_TOKEN" https://api.github.com/user/repos \
        | grep -o '"clone_url":"[^"]*"' | head -1 | sed 's/"clone_url":"//' | sed 's/"$//' 2>/dev/null || echo "")
    fi

    # 기본값 (boydcog의 service-flow-template)
    if [ -z "$REMOTE_URL" ]; then
      REMOTE_URL="git@github.com:boydcog/service-flow-template.git"
    fi

    git remote add origin "$REMOTE_URL" 2>/dev/null || true
    STATUS="$STATUS
OK Git Remote 설정: $REMOTE_URL"
  else
    STATUS="$STATUS
OK Git Remote 확인됨: $CURRENT_REMOTE"
  fi

  # ──────────────────────────────────────
  # 5.5. 잔여 worktree 정리
  # ──────────────────────────────────────
  WORKTREE_DIR="${PROJECT_DIR}/../.worktrees"
  if [ -d "$WORKTREE_DIR" ]; then
    git worktree prune 2>/dev/null || true
    CLEANED=0
    for wt in "$WORKTREE_DIR"/*/; do
      if [ -d "$wt" ]; then
        if git worktree remove --force "$wt" 2>/dev/null; then
          CLEANED=$((CLEANED + 1))
        fi
      fi
    done
    if [ "$CLEANED" -gt 0 ]; then
      STATUS="$STATUS
WARN 잔여 worktree ${CLEANED}개 정리됨"
    fi
    rmdir "$WORKTREE_DIR" 2>/dev/null || true
  fi

  # ──────────────────────────────────────
  # 6. Git Pull 재시도 (stash+rebase+pop)
  # ──────────────────────────────────────
  if [ "$GIT_READY" = "true" ]; then
    # 메인 브랜치로 전환
    if [ "$CURRENT_BRANCH" != "main" ]; then
      git checkout main 2>/dev/null || git checkout -f main 2>/dev/null || true
      CURRENT_BRANCH="main"
    fi

    # pull 시도
    PULL_RESULT=$(git pull --rebase origin main 2>&1 || echo "pull-failed")
    if echo "$PULL_RESULT" | grep -q "pull-failed"; then
      git rebase --abort 2>/dev/null || true
      STASHED="false"

      # stash
      STASH_RESULT=$(git stash 2>&1)
      if echo "$STASH_RESULT" | grep -q "Saved working directory"; then
        STASHED="true"
      fi

      # 재시도
      PULL_RESULT2=$(git pull --rebase origin main 2>&1 || echo "pull-failed")
      if echo "$PULL_RESULT2" | grep -q "pull-failed"; then
        git rebase --abort 2>/dev/null || true
        if [ "$STASHED" = "true" ]; then
          git stash pop 2>/dev/null || true
        fi
        STATUS="$STATUS
WARN git pull 실패 (오프라인 또는 네트워크 오류)"
      else
        if [ "$STASHED" = "true" ]; then
          git stash pop 2>/dev/null || true
        fi
        STATUS="$STATUS
OK git pull 완료 (stash+rebase 복구)"
      fi
    else
      STATUS="$STATUS
OK git pull 완료"
    fi
  fi

  # ──────────────────────────────────────
  # 7. 마이그레이션 감지 및 자동 실행
  # ──────────────────────────────────────
  CURRENT_SCHEMA=$(cat ".claude/state/_schema_version.txt" 2>/dev/null || echo "v1")
  TARGET_SCHEMA=$(cat ".claude/migrations/_target_version.txt" 2>/dev/null || echo "v1")

  if [ "$CURRENT_SCHEMA" != "$TARGET_SCHEMA" ]; then
    echo "🔄 마이그레이션 감지: $CURRENT_SCHEMA → $TARGET_SCHEMA"

    # 마이그레이션 스크립트 자동 실행
    MIGRATION_SCRIPT=".claude/migrations/${CURRENT_SCHEMA}-to-${TARGET_SCHEMA}.sh"
    if [ -f "$MIGRATION_SCRIPT" ]; then
      echo "마이그레이션 실행 중..."
      if bash "$MIGRATION_SCRIPT"; then
        echo "✅ 마이그레이션 완료"
        STATUS="$STATUS
OK 마이그레이션: $CURRENT_SCHEMA → $TARGET_SCHEMA"
      else
        echo "⚠️  마이그레이션 중 오류 발생"
        STATUS="$STATUS
WARN 마이그레이션 실패: $CURRENT_SCHEMA → $TARGET_SCHEMA"
      fi
    else
      echo "⚠️  마이그레이션 스크립트를 찾을 수 없습니다: $MIGRATION_SCRIPT"
      STATUS="$STATUS
WARN 마이그레이션 스크립트 없음: $MIGRATION_SCRIPT"
    fi
  fi
fi

# ──────────────────────────────────────
# 8. 활성 플로우 복구
# ──────────────────────────────────────
ACTIVE_FLOW=""
if [ -f ".claude/state/_active_flow.txt" ]; then
  ACTIVE_FLOW=$(cat ".claude/state/_active_flow.txt" | tr -d '[:space:]')
  if [ -n "$ACTIVE_FLOW" ]; then
    STATUS="$STATUS
OK 활성 플로우: $ACTIVE_FLOW"
  fi
fi

# ──────────────────────────────────────
# 9. Web-Native 컴포넌트 동기화 확인
# ──────────────────────────────────────
echo ""
echo "🔄 컴포넌트 동기화 확인 중..."
if [ -f .claude/hooks/check-sync.sh ]; then
  if ./.claude/hooks/check-sync.sh 2>&1 | grep -q "✅"; then
    echo "✅ 모든 컴포넌트가 동기화되었습니다"
  else
    echo "⚠️  컴포넌트 동기화 경고 — 자세한 내용은 ./.claude/hooks/check-sync.sh 실행"
  fi
else
  echo "⚠️  동기화 스크립트를 찾을 수 없습니다"
fi

# ──────────────────────────────────────
# 10. 프로젝트 컴포넌트 자동 동기화
# ──────────────────────────────────────
echo ""
echo "🔄 프로젝트 컴포넌트 자동 동기화 중..."
if [ -d projects ] && [ -f scripts/sync-components.sh ]; then
  SYNC_COUNT=0
  for project_dir in projects/*/; do
    if [ -d "$project_dir" ] && [ "$(basename "$project_dir")" != ".gitkeep" ]; then
      if bash scripts/sync-components.sh "$project_dir" >/dev/null 2>&1; then
        SYNC_COUNT=$((SYNC_COUNT + 1))
      fi
    fi
  done
  if [ $SYNC_COUNT -gt 0 ]; then
    echo "✅ $SYNC_COUNT개 프로젝트 컴포넌트 동기화 완료"
    STATUS="$STATUS
OK $SYNC_COUNT개 프로젝트 동기화"
  fi
else
  echo "ℹ️  활성 프로젝트 없음"
fi

# ──────────────────────────────────────
# 11. 최종 상태 리포트
# ──────────────────────────────────────
echo ""

# 컴포넌트 개수 계산 (오류 안전)
WEB_COUNT=0
NATIVE_COUNT=0
if [ -d "components/web/ui" ]; then
  WEB_COUNT=$(find components/web/ui -name "*.tsx" 2>/dev/null | wc -l || echo 0)
  WEB_COUNT=$((WEB_COUNT))
fi
if [ -d "components/native/ui" ]; then
  NATIVE_COUNT=$(find components/native/ui -name "*.tsx" 2>/dev/null | wc -l || echo 0)
  NATIVE_COUNT=$((NATIVE_COUNT))
fi

echo "의존성:"
echo "  git: $HAS_GIT"
echo "  gh: $HAS_GH"
echo "  brew: $HAS_BREW"
echo ""
echo "프로젝트 상태:"
echo "  웹 컴포넌트: ${WEB_COUNT}개"
echo "  네이티브 컴포넌트: ${NATIVE_COUNT}개"
echo "  활성 플로우: ${ACTIVE_FLOW:-미설정}"
echo "  현재 브랜치: $CURRENT_BRANCH"
echo "  GH 토큰: $GH_TOKEN_LOADED"
echo "  git 연결: $GIT_READY"
echo ""
echo "명령어: /setup  /admin  /designer  /flow  /create-issue"
echo ""
