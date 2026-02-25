# /admin-status — 변경사항 확인 (GitHub 진입 없이)

## 개요

GitHub에 직접 진입하지 않고 **CLI에서 변경사항 상태를 확인**합니다.

**권한**: 모든 역할 (admin, developer, designer, pm)
**Implementation**: `.claude/hooks/check-status.sh`
**Intent Detection**:
- "상태 확인", "변경사항 확인", "PR 상태", "브랜치 상태", "적용되었나"

---

## 실행 지시 (Claude Code)

### 0단계: Git 동기화 (필수)

```bash
set -euo pipefail

echo "🔄 최신 상태 동기화 중..."

# ──────────────────────────────────────
# 1. Git Fetch
# ──────────────────────────────────────
git fetch origin 2>&1 | grep -E "From|Fetching" || echo "✓ Fetch 완료"

# ──────────────────────────────────────
# 2. Git Pull (Rebase + Stash 처리)
# ──────────────────────────────────────
PULL_RESULT=$(git pull --rebase origin main 2>&1 || echo "pull-failed")

if echo "$PULL_RESULT" | grep -q "Already up to date"; then
  echo "✅ 이미 최신 상태"
elif echo "$PULL_RESULT" | grep -q "pull-failed"; then
  echo "⚠️  Git pull 충돌 감지, 복구 시도 중..."
  git rebase --abort 2>/dev/null || true

  STASHED="false"
  STASH_RESULT=$(git stash 2>&1)
  if echo "$STASH_RESULT" | grep -q "Saved working directory"; then
    STASHED="true"
    echo "  • 로컬 변경사항 임시 저장됨"
  fi

  PULL_RESULT2=$(git pull --rebase origin main 2>&1 || echo "pull-failed-again")
  if echo "$PULL_RESULT2" | grep -q "pull-failed-again"; then
    git rebase --abort 2>/dev/null || true
    if [ "$STASHED" = "true" ]; then
      git stash pop 2>/dev/null || true
    fi
    echo "❌ Git pull 실패 (네트워크 오류 또는 충돌)"
    exit 1
  else
    if [ "$STASHED" = "true" ]; then
      git stash pop 2>/dev/null || true
    fi
    echo "✅ 최신 커밋 적용됨 (복구 완료)"
  fi
else
  echo "✅ 최신 커밋 적용됨"
fi

echo ""
```

### 1단계: 옵션 선택 (AskUserQuestion - optional)
```
무엇을 확인하시겠습니까?
 1. 전체 상태 (기본)
 2. PR 상태만 (--pr)
 3. 브랜치 상태만 (--branch)
 4. 로컬 변경사항만 (--local)
 5. 마이그레이션 상태만 (--migration)
```

### 2단계: 스크립트 자동 실행
```bash
bash .claude/hooks/check-status.sh [선택한 옵션]
```

### 3단계: 결과 출력
사용자에게 상태를 명확하게 표시

---

## 사용 예

### 예 1: 전체 상태 확인
```bash
/admin-status
# 또는
bash .claude/hooks/check-status.sh

# 출력:
# ========================================
# Service Flow Template — 상태 확인
# ========================================
#
# 로컬 변경사항
# 최근 커밋:
# 3f7a8c2 admin: 팀원 추가
#
# 브랜치 상태
# 현재 브랜치: admin/1708741600
# 로컬 커밋 (미푸시): 1개
#
# PR 상태 확인
# PR #123: [admin] 보이드: 팀원 추가 [OPEN]
#
# 최근 병합된 PR
# PR #122: [designer] 박나현: Button 컴포넌트 (병합: 2026-02-24)
#
# 마이그레이션 상태
# 현재 스키마: v2
# 목표 스키마: v2
# 스키마가 최신 버전입니다
```

### 예 2: PR 상태만 확인
```bash
bash .claude/hooks/check-status.sh --pr

# 출력:
# PR 상태 확인
#
# PR #123: [admin] 보이드: 팀원 추가 [OPEN]
# PR #122: [designer] 박나현: Button 컴포넌트 [MERGED] (2026-02-24)
# PR #121: [flow] 김기획: 온보딩 플로우 [OPEN]
```

### 예 3: 브랜치 상태 확인
```bash
bash .claude/hooks/check-status.sh --branch

# 출력:
# 브랜치 상태
#
# 현재 브랜치: main
# main 브랜치와 동기화됨
#
# 스테이징된 파일: 0개
# 수정된 파일 (미스테이징): 2개
# Untracked 파일: 0개
```

### 예 4: 로컬 변경사항만 확인
```bash
bash .claude/hooks/check-status.sh --local

# 출력:
# 로컬 변경사항
#
# 최근 커밋:
# 3f7a8c2 admin: 팀원 추가
# b4d5e1f admin: 테마 업데이트
# c6f9g2h [designer] 버튼 컴포넌트
#
# 변경 통계:
# manifests/team.yaml | 2 ++
# manifests/theme.yaml | 5 +-
# 1 file changed, 5 insertions(+), 3 deletions(-)
```

### 예 5: 마이그레이션 상태만 확인
```bash
bash .claude/hooks/check-status.sh --migration

# 출력:
# 마이그레이션 상태
#
# 현재 스키마: v2
# 목표 스키마: v2
# 스키마가 최신 버전입니다
```

---

## Intent Detection 예

사용자가 다음과 같이 말하면 자동으로 이 스킬 실행:

```
"변경사항 확인해줘"
→ /admin-status (전체)

"PR 상태 알려줘"
→ /admin-status --pr

"지금 뭐 수정했어?"
→ /admin-status --local

"마이그레이션 되었나?"
→ /admin-status --migration

"브랜치 상태 봐줄래?"
→ /admin-status --branch
```

---

## 로그 확인

### 마이그레이션 로그
```bash
cat .claude/state/logs/migrations.log
# [2026-02-24 16:55:32] Migration v1→v2 completed
```

### PR 이력 로그
```bash
cat .claude/state/logs/pr-history.log
# [2026-02-24 17:00:00] PR#123 created: [admin] 보이드: 팀원 추가
```

### Admin 액션 로그
```bash
cat .claude/state/logs/admin-actions.log
# [2026-02-24 17:00:00] 팀원 추가 | admin/1708741600
```

---

## 문제 해결

### "gh CLI가 설치되지 않았습니다" 오류

PR 상태 확인 불가. 다른 옵션 사용:
```bash
bash .claude/hooks/check-status.sh --local # PR 없이 로컬만 확인
bash .claude/hooks/check-status.sh --branch # PR 없이 브랜치만 확인
```

### "GitHub 토큰을 찾을 수 없습니다"

PR 상태 확인 불가:
```bash
# /setup 재실행
/setup

# 또는 토큰 설정
echo "your-github-token" > .gh-token
```

---

## 관련 스킬

- `/admin` — 템플릿 관리 (파일 수정)
- `/admin-status` — 변경사항 확인 (상태 보기) ← 이것
- `/setup` — 신원 설정
