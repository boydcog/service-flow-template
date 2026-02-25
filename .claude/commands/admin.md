# /admin — 템플릿 관리

## 개요

템플릿 규칙, 팀 관리, 테마 설정을 담당합니다. 회사 전체의 표준을 유지하는 역할입니다.

**권한**: admin, developer 전용
**Implementation**: `.claude/hooks/admin-workflow.sh` + 유틸 스크립트

---

## 실행 지시 (Claude Code)

### 0단계: Git 동기화 및 마이그레이션 (필수)

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
  # Pull 실패 시 Rebase abort + Stash + 재시도
  echo "⚠️  Git pull 충돌 감지, 복구 시도 중..."
  git rebase --abort 2>/dev/null || true

  # Stash 저장
  STASHED="false"
  STASH_RESULT=$(git stash 2>&1)
  if echo "$STASH_RESULT" | grep -q "Saved working directory"; then
    STASHED="true"
    echo "  • 로컬 변경사항 임시 저장됨"
  fi

  # 재시도
  PULL_RESULT2=$(git pull --rebase origin main 2>&1 || echo "pull-failed-again")
  if echo "$PULL_RESULT2" | grep -q "pull-failed-again"; then
    git rebase --abort 2>/dev/null || true
    if [ "$STASHED" = "true" ]; then
      git stash pop 2>/dev/null || true
    fi
    echo "❌ Git pull 실패 (네트워크 오류 또는 충돌)"
    echo "   수동 처리 필요: git status 확인 후 다시 시도"
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

# ──────────────────────────────────────
# 3. 마이그레이션 감지 및 자동 실행
# ──────────────────────────────────────
CURRENT_SCHEMA=$(cat ".claude/state/_schema_version.txt" 2>/dev/null || echo "v1")
TARGET_SCHEMA=$(cat ".claude/migrations/_target_version.txt" 2>/dev/null || echo "v1")

if [ "$CURRENT_SCHEMA" != "$TARGET_SCHEMA" ]; then
  echo ""
  echo "🔄 마이그레이션 감지: $CURRENT_SCHEMA → $TARGET_SCHEMA"
  MIGRATION_SCRIPT=".claude/migrations/${CURRENT_SCHEMA}-to-${TARGET_SCHEMA}.sh"

  if [ -f "$MIGRATION_SCRIPT" ]; then
    if bash "$MIGRATION_SCRIPT"; then
      echo "✅ 마이그레이션 완료"
    else
      echo "❌ 마이그레이션 실패"
      exit 1
    fi
  else
    echo "❌ 마이그레이션 스크립트 없음: $MIGRATION_SCRIPT"
    echo "   관리자에게 문의하세요"
    exit 1
  fi
fi

echo ""
```

### 1단계: 선행 조건 확인

#### 1-1. 신원 파일 확인
```bash
if [ ! -f .user-identity ]; then
  echo "❌ 사용자 신원이 설정되지 않았습니다"
  echo "먼저 /setup을 실행해주세요"
  exit 1
fi
```

#### 1-2. 권한 검증 (admin, developer만 가능)
```bash
# .user-identity에서 사용자 정보 로드 (이미 설정됨)
USER_NAME=$(grep '^name:' .user-identity | sed 's/name: //')
USER_ROLE=$(grep '^role:' .user-identity | sed 's/role: //')
USER_GITHUB=$(grep '^github:' .user-identity | sed 's/github: //')

# 권한 검증: admin 또는 developer만 가능
if [[ "$USER_ROLE" != "admin" && "$USER_ROLE" != "developer" ]]; then
  echo "❌ 권한 없음"
  echo "역할 [$USER_ROLE]은 /admin을 사용할 수 없습니다"
  echo "필요한 권한: admin, developer"
  echo ""
  echo "현재 역할이 할 수 있는 작업:"
  echo "- /designer — 컴포넌트 제작"
  echo "- /flow — 플로우 설계"
  echo "- /create-issue — 이슈 제보"
  exit 1
fi

echo "✅ 권한 확인 완료"
echo "신원: $USER_NAME ($USER_ROLE)"
echo "GitHub: $USER_GITHUB"
echo ""
echo "이 세션에서는 /admin을 사용해서 템플릿을 관리합니다."
```

#### 1-3. GitHub 토큰 검증
```bash
# .gh-token 파일 확인
if [ ! -f .gh-token ]; then
  echo ""
  echo "⚠️ GitHub 토큰 파일이 없습니다"
  echo "다음 URL에서 Personal Access Token 생성:"
  echo "https://github.com/settings/tokens"
  echo ""
  echo "Token 입력:"
  read -s GH_TOKEN
  echo "$GH_TOKEN" > .gh-token
  chmod 600 .gh-token
  git update-index --skip-worktree .gh-token
fi

# 토큰 유효성 검증
GH_TOKEN=$(cat .gh-token)
if [ -z "$GH_TOKEN" ]; then
  echo "❌ .gh-token 파일이 비어있습니다"
  exit 1
fi

echo "✅ GitHub 토큰 검증 완료"
```

### 2단계: 관리 옵션 선택 (AskUserQuestion)
```
관리 옵션을 선택하세요:
 1. 컴포넌트 스펙 관리 (.claude/spec/)
 2. 팀원 관리 (.claude/manifests/team.yaml)
 3. 테마 업데이트 (.claude/manifests/theme.yaml)
 4. 역할 및 권한 관리 (.claude/manifests/roles.yaml)
 5. CHANGELOG 작성
 6. 변경사항 확인 → bash .claude/hooks/check-status.sh
```

### 3단계: 워크플로우 자동 실행
각 옵션별로:
1. 파일 수정 (Read → Edit/Write)
2. CHANGELOG 업데이트
3. 다음 명령 자동 실행:
```bash
bash .claude/hooks/admin-workflow.sh "{작업 설명}" "{변경 내용}" "$USER_NAME"
```

### 4단계: 결과 확인
```bash
# PR 링크 자동 표시
# 변경사항 확인
bash .claude/hooks/check-status.sh --pr
```

---

## 빠른 사용 예

### 예 1: 팀원 추가
```
1. /admin 실행
2. "2. 팀원 관리" 선택
3. .claude/manifests/team.yaml 편집 (Add name, role, github)
4. 자동으로 admin-workflow.sh 실행
5. PR 생성됨
```

### 예 2: 테마 업데이트
```
1. /admin 실행
2. "3. 테마 업데이트" 선택
3. .claude/manifests/theme.yaml 편집
4. 자동으로 admin-workflow.sh 실행
5. PR 생성됨
```

### 예 3: 변경사항 확인 (GitHub 진입 없이)
```
1. /admin-status 실행
2. PR 상태, 브랜치 상태, 로컬 변경사항 확인
3. 마이그레이션 상태 확인
```

---

## 연동된 유틸 스크립트

| 스크립트 | 용도 | 자동 호출 |
|---------|------|---------|
| `admin-workflow.sh` | 브랜치 생성 → 커밋 → PR 생성 | admin 작업 완료 후 |
| `check-status.sh` | 상태 확인 (PR/브랜치/로컬) | 수동 또는 option 6 |
| `create-pr.sh` | PR 생성 (저수준) | admin-workflow에서 호출 |
| `startup.sh` | 세션 시작 (마이그레이션 자동) | 매 세션 시작 |

---

## 구현 상세 (아래 옵션별)

---

## 사용 방법

```bash
/admin
```

---

## 단계별 진행

### 1단계: 신원 및 권한 확인

```
 신원: 보이드 (admin)
 권한: 템플릿 관리 가능

다음 단계: 관리 옵션 선택
```

**권한 없음 시**:
```
 designer은 /admin 명령어를 사용할 수 없습니다.
필요 역할: admin 또는 developer
```

### 2단계: 관리 옵션 선택

```
 관리 옵션을 선택하세요:
 1. 컴포넌트 스펙 관리
 2. 팀원 관리
 3. 테마 업데이트
 4. 역할 및 권한 관리
 5. CHANGELOG 작성
 6. 통계 보기

선택:
> 1
```

---

## 옵션 1: 컴포넌트 스펙 관리

### 진행 과정

```
 컴포넌트 스펙 관리
====================

현재 스펙:
- component-spec.md (웹/네이티브 컴포넌트 규칙)
- flow-spec.md (플로우 컨벤션)

액션 선택:
 1. 스펙 수정
 2. 스펙 보기
 3. 버전 관리

선택:
> 1

 component-spec.md 수정:

현재 내용:
────────────────────
# 컴포넌트 생성 규칙

## Props 정의

### 필수 Props vs 선택 Props
...
────────────────────

수정할 섹션:
 1. Props 정의
 2. Emocog 테마 사용
 3. 접근성 (A11y)
 4. 테스트
 5. 체크리스트

선택:
> 2

현재 Emocog 테마 사용 섹션:
────────────────────
#### 색상 사용
```typescript
// Tailwind CSS 유틸리티 클래스
<button className="bg-primary text-primary-foreground">
 Primary Button
</button>

// 또는 CSS 변수 (권장)
<button className="bg-[var(--emocog-primary)] text-[var(--emocog-primary-foreground)]">
 Primary Button
</button>
```
────────────────────

새 내용 입력 (여러 줄 가능, Ctrl+D로 종료):
> #### 색상 사용
>
> Tailwind CSS와 Emocog 테마 변수를 함께 사용합니다.
>
> **권장**:
> - Tailwind 유틸리티 클래스 사용 (성능)
> - CSS 변수로 폴백 (호환성)
>
> ```typescript
> <button className="
> bg-primary text-primary-foreground
> hover:opacity-90 transition-all
> dark:bg-primary dark:text-primary-foreground
> ">
> Primary Button
> </button>
> ```

 스펙이 업데이트되었습니다!

변경 사항:
- Emocog 테마 사용 섹션 업데이트
- 다크 모드 예제 추가

 git worktree 생성 중...
브랜치: main-update-specs (임시)

 CHANGELOG 작성하시겠습니까? (y/n):
> y
```

---

## 옵션 2: 팀원 관리

### 팀원 추가

```
 팀원 관리
============

현재 팀:
- 보이드 (admin)

액션 선택:
 1. 팀원 추가
 2. 팀원 제거
 3. 팀 조회

선택:
> 1

 새 팀원 정보 입력:

이름:
> 홍길동

역할:
 1. admin
 2. developer
 3. designer
 4. pm

선택:
> 3

GitHub 사용자명:
> hong-gildong

이메일:
> hong@example.com

확인:
- 이름: 홍길동
- 역할: designer
- GitHub: hong-gildong
- 이메일: hong@example.com

추가하시겠습니까? (y/n):
> y

========================
 팀원이 추가되었습니다!

업데이트된 팀:
- 보이드 (admin)
- 홍길동 (designer)

team.yaml 업데이트됨
PR 생성 대기 중...
```

### 팀원 제거

```
 팀원 제거
===========

제거할 팀원 선택:
 1. 홍길동 (designer)
 2. 김개발 (developer)

선택 또는 이름 입력:
> 1

정말 홍길동을 제거하시겠습니까? (y/n):
> y

 홍길동이 제거되었습니다.

영향받는 항목:
- 기존 PR (hong-gildong)은 유지됨
- 권한은 즉시 회수됨
```

### 팀 조회

```
 현재 팀 구성
==============

Admins:
- 보이드 (boydcog) - 2024-02-24 가입

Developers:
- 김개발 (kim-dev) - 2024-02-20 가입

Designers:
- 홍길동 (hong-gildong) - 2024-02-24 가입
- 이디자인 (lee-designer) - 2024-02-22 가입

PMs:
- 박기획 (park-pm) - 2024-02-23 가입

총 5명
```

---

## 옵션 3: 테마 업데이트

### Emocog 테마 관리

```
 테마 업데이트
===============

현재 테마:
- Emocog v1.0.0
- 색상: Light + Dark 모드
- 타이포그래피: Poppins 등

액션 선택:
 1. 색상 업데이트
 2. 타이포그래피 변경
 3. 간격(Spacing) 조정
 4. 그림자(Shadows) 변경
 5. ⏱ 애니메이션 수정

선택:
> 1

 색상 업데이트
================

모드 선택:
 1. Light 모드
 2. Dark 모드

선택:
> 1

Light 모드 색상:

현재:
- primary: oklch(0.488 0.243 264.376)
- background: oklch(0.985 0.001 106.423)
- foreground: oklch(0.208 0.042 265.755)

업데이트할 색상 (쉼표로 구분):
> primary, background

Primary 색상 변경:
현재: oklch(0.488 0.243 264.376)
새 값: oklch(0.520 0.260 264.376)

변경하시겠습니까? (y/n):
> y

Background 색상 변경:
현재: oklch(0.985 0.001 106.423)
새 값: oklch(0.980 0.002 106.423)

변경하시겠습니까? (y/n):
> y

 색상이 업데이트되었습니다!

변경 사항:
- Light 모드 primary 업데이트
- Light 모드 background 업데이트

영향받는 파일:
- .claude/manifests/theme.yaml
- components/theme/tokens.css
- components/theme/gluestack-theme.ts

 CSS 변수 재생성 중...
 tokens.css 업데이트됨

 Gluestack 토큰 재생성 중...
 gluestack-theme.ts 업데이트됨
```

---

## 옵션 4: 역할 및 권한 관리

```
 역할 및 권한 관리
===================

현재 역할 정의:
- admin: /setup, /admin, /designer, /flow, /create-issue
- developer: /setup, /admin, /designer, /flow, /create-issue
- designer: /setup, /designer, /flow, /create-issue
- pm: /setup, /flow, /create-issue

액션 선택:
 1. 역할 수정
 2. 권한 추가
 3. 권한 제거
 4. 권한 조회

선택:
> 1

수정할 역할:
 1. admin
 2. developer
 3. designer
 4. pm

선택:
> 3

Designer 역할 현재 설정:
- can_modify_template: false
- can_modify_components: true
- can_modify_specs: false
- can_manage_team: false
- can_create_flows: true

변경할 항목:
 1. can_modify_components: true → false
 2. can_modify_specs: false → true
 3. 기타

선택:
> 2

수정 확인:
- Designer이 스펙 수정 가능?

변경하시겠습니까? (y/n):
> y

 역할이 업데이트되었습니다!

roles.yaml 업데이트됨
PR 생성 대기 중...
```

---

## 옵션 5: CHANGELOG 작성

```
 CHANGELOG 작성
=================

마지막 항목:
- v1.0.0 (2024-02-20): 초기 템플릿 출시

새 버전 번호:
> 1.1.0

변경 유형 선택 (복수 선택 가능):
 [ ] Features
 [ ] Bugfixes
 [ ] Documentation
 [ ] Refactoring
 [ ] Dependencies

선택 (쉼표로 구분):
> , 

Features:
> 팀원 추가 기능 개선
> 테마 색상 업데이트 자동화

Documentation:
> 컴포넌트 스펙 명확화
> 플로우 예제 추가

========================
 CHANGELOG가 업데이트되었습니다!

생성된 항목:
- v1.1.0 (2024-02-24)
 - Features: 2개
 - Documentation: 2개

PR 생성 대기 중...
```

---

## 옵션 6: 통계 보기

```
 템플릿 통계
==============

 컴포넌트:
- Web: 12개
- Native: 5개
- 총합: 17개

 서비스 플로우:
- 활성 브랜치: 3개
- 완료된 플로우: 2개

 팀 구성:
- Admin: 1명
- Developer: 1명
- Designer: 2명
- PM: 1명
- 총합: 5명

 문서:
- 스펙 파일: 2개
- 템플릿: 2개
- 명령어: 5개

 최근 활동:
- PR 생성 (지난 7일): 8개
- 이슈 생성 (지난 7일): 12개
- 커밋 (지난 7일): 25개

 성장 추세:
- 컴포넌트 추가: +3개 (지난 월)
- 팀원 추가: +2명 (지난 월)
- PR 병합: +12개 (지난 월)
```

---

## PR 생성 및 검토

```
 PR 생성
==========

변경 사항 요약:
- 컴포넌트 스펙 업데이트
- team.yaml에 팀원 추가
- 테마 색상 업데이트
- CHANGELOG 작성

PR 정보:
제목: [admin] 보이드: v1.1.0 템플릿 업데이트
분기: main-update-specs → main
파일 수: 5개

========================
 PR이 생성되었습니다!

 PR 링크: https://github.com/{owner}/{repo}/pull/789
 상태: Open (리뷰 대기 중)

병합 전 체크리스트:
- [ ] 모든 파일이 검토됨
- [ ] 테스트 통과
- [ ] CHANGELOG 포함됨
- [ ] 2명 이상 승인
```

---

## 워크플로우

### Admin 작업 프로세스

```
1. /admin 실행
 ↓
2. 관리 옵션 선택
 ↓
3. git worktree 자동 생성 (메인 브랜치 보호)
 ↓
4. 파일 수정
 ↓
5. CHANGELOG 업데이트 (자동)
 ↓
6. PR 자동 생성
 ↓
7. 다른 admin/developer 승인
 ↓
8. main 브랜치로 자동 병합
```

### 메인 브랜치 보호

- `git worktree`를 사용하여 메인 브랜치 직접 수정 방지
- 모든 변경은 PR을 통해 코드 리뷰 후 병합
- force-push 불가 (메인 브랜치)

---

## 사례: PR #3 GitHub 보안 개선 (2026-02-25)

### 과정

1. **리뷰 확인**
   - PR: GitHub 토큰 인증 기반 API 호출
   - Qodo 자동 리뷰: 4가지 보안 이슈 + 4가지 개선 제안 확인

2. **이슈 해결** (2개 커밋)
   - Commit 1: 보안 및 에러 처리 강화
     - jq, GH_TOKEN 검증 추가
     - 민감한 정보 노출 제거
     - curl 에러 감지 개선
   - Commit 2: 코드 중복 제거
     - post-designer.sh, post-flow.sh 중복 로직 제거
     - create-pr.sh 호출로 통합 (80줄 감소)

3. **PR 댓글 작성**
   - 모든 Qodo 제안 적용 상황 정리
   - 커밋 히스토리 명시
   - 코드 변경 영향도 요약

### 결과
- 3개 커밋 (초기 + 보안 강화 + 코드 개선)
- 95줄 감소
- 모든 Qodo 리뷰 이슈 해결

### 적용 방법
```bash
# 1. PR 리뷰 확인
# → Qodo 자동 리뷰 분석

# 2. 문제 해결
# → 각 이슈별 커밋 생성

# 3. PR 댓글 작성
# → 적용된 개선사항 정리

# 4. Merge
# → GitHub에서 "Squash and merge" 또는 "Create merge commit"
```

---

## 체크리스트

admin 작업 완료 전 확인:

- [ ] 변경 사항이 명확합니다
- [ ] CHANGELOG를 작성했습니다
- [ ] PR 템플릿을 사용했습니다
- [ ] 다른 admin에게 검토 요청했습니다
- [ ] 테스트를 실행했습니다 (해당 시)
- [ ] 문서를 업데이트했습니다
- [ ] 팀에 공지했습니다 (주요 변경 시)

---

## 참고

- [Roles 정의](../manifests/roles.yaml)
- [Team 관리](../manifests/team.yaml)
- [Emocog 테마](../manifests/theme.yaml)
- [컴포넌트 스펙](../spec/component-spec.md)
- [PR 템플릿](../templates/pr-template.md)
