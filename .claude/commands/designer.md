# /designer — 컴포넌트 제작/수정/확장

## 개요

Emocog 테마를 기반으로 재사용 가능한 컴포넌트를 만들거나, 기존 컴포넌트를 수정/확장합니다.

**권한**: designer 이상 (admin, developer, designer)

---

## Claude 실행 지시

이 명령을 실행할 때 Claude가 따라야 할 단계:

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

#### 1-2. 권한 검증 (admin, developer, designer만 가능)
```bash
# 사용자 정보 로드
USER_NAME=$(grep '^name:' .user-identity | sed 's/name: //')
USER_ROLE=$(grep '^role:' .user-identity | sed 's/role: //')

# 권한 검증: admin, developer, designer만 가능
if [[ "$USER_ROLE" != "admin" && "$USER_ROLE" != "developer" && "$USER_ROLE" != "designer" ]]; then
  echo "❌ 권한 없음"
  echo "역할 [$USER_ROLE]은 /designer를 사용할 수 없습니다"
  echo "필요한 권한: admin, developer, designer"
  echo ""
  echo "현재 역할이 할 수 있는 작업:"
  echo "- /flow — 플로우 설계"
  echo "- /create-issue — 이슈 제보"
  exit 1
fi

echo "✅ 권한 확인 완료"
echo "역할: $USER_ROLE | 사용자: $USER_NAME"
echo ""
echo "이 세션에서는 /designer를 사용해서 컴포넌트를 제작/수정합니다."
```

### 2단계: 프레임워크 선택 (AskUserQuestion)
- Web (Next.js, Vite + React, Remix)
- Native (React Native + Gluestack)

### 3단계: 컴포넌트 탐색 및 목록 표시
- 현재 등록된 컴포넌트 수와 목록 출력
- 각 컴포넌트의 스토리 파일 존재 여부 표시

### 4단계: 3-way 액션 선택 (AskUserQuestion)
1. 새 컴포넌트 생성 (create)
2. 기존 컴포넌트 확장 (extend) — 스토리/변형 추가
3. 기존 컴포넌트 수정 (modify) — 코드 직접 수정

### 5단계: 액션별 처리

**create (새 컴포넌트 생성)**:
- 이름 입력 시 덮어쓰기 방지 검사 (동일 이름 파일 존재 확인)
- 존재하면 경고 후 사용자 확인 요청 (y/n)
- n 선택 시 "확장" 또는 "수정" 안내 후 중단
- 컴포넌트 정보 수집 (이름, 설명, 유형)
- 코드 생성 (`.claude/spec/component-spec.md` 참조)

**extend (기존 컴포넌트 확장)**:
- 부분 일치 검색으로 컴포넌트 찾기
- Props 인터페이스만 표시
- 확장 옵션 선택: 스토리 추가 / 변형 추가
- 스토리 추가 시 export 이름 충돌 검사

**modify (기존 컴포넌트 수정)**:
- 부분 일치 검색으로 컴포넌트 검색
- 전체 코드 표시
- diff 확인 후 저장
- 사용자가 n 선택 시 원본 유지

### 6단계: 검증 (Strict Mode)
- `npm run verify:fast` 실행
- 검증 항목: 컴포넌트 파일, 스토리 파일, Default 스토리, Props 정의, any 타입 금지
- 실패 시 최대 3회 재시도
- 재시도 실패 시 PR 생성 불가

### 7단계: Storybook 실행 및 사용자 검증 요청

**Storybook 시작**:
```bash
# 포트 6006 정리 및 재시작
npm run storybook
# 브라우저 자동 띄우기: http://localhost:6006
```

**사용자 검증 요청 (AskUserQuestion)**:
```
개발이 완료되었습니다!

이제 Storybook에서 다음을 확인해주세요:

1. 시각적 일치성
 - 모든 상태(default, hover, active, disabled) 정상 표시
 - Figma 디자인과 일치

2. 기능 동작
 - Props 변경 시 컴포넌트 정상 업데이트
 - 다양한 크기/색상 변형 작동

3. 접근성
 - 키보드 탭 이동 가능 (interactive 컴포넌트)
 - 스크린 리더 호환성

4. 반응형
 - 모바일 (375px)
 - 태블릿 (768px)
 - 데스크톱 (1920px)

검증이 완료되셨나요?

[O] 완료 - 모두 정상
[X] 미완료 - 수정 필요
[?] 질문 있음
```

### 8단계: 검증 결과 처리

#### 검증 완료 
```
감사합니다!

개발자에게 공유할 준비가 되었습니다.

[Yes] PR 생성 & 개발자 알림
[No] 로컬에만 저장 (나중에 공유)
[Edit] 코드 수정 후 재검증
```

#### 미완료 (수정 필요) 
```
어떤 부분을 수정할까요?

사용자 입력 예:
> Button의 hover 상태가 안보임
> 모바일에서 패딩이 부족해 보임

Claude:
1. 문제 분석
2. 코드 수정
3. Storybook 재확인 요청
4. 재검증 플로우
```

#### 질문 있음 
```
어떤 부분이 궁금하신가요?

사용자 질문 → Claude 답변 → 재검증 요청
```

### 9단계: PR 생성 또는 로컬 저장

**PR 생성 선택 시**:
- 브랜치 명: `component/{component-name}`
- PR 제목: `[designer] {사용자명}: {컴포넌트명}`
- PR 본문: 변경사항 + 검증 정보 + 스크린샷
- 라벨: `enhancement` (자동 할당)
- 검증 정보 포함:
 - 검증자: 사용자명
 - 검증 일시: YYYY-MM-DD HH:MM:SS
 - 검증 항목: 시각적 일치, 기능, 접근성, 반응형

**로컬 저장 선택 시**:
```
.claude/state/pending-shares/designer/
└── button_component.json
```

### 10단계: 불만/피드백 감지 및 Issue 공유 (선택)

**피드백 감지**:
```
개발 중 또는 완료 후 사용자가 다음과 같이 표현하면:

"Button의 색상이 Figma와 다르네요"
"미디엄 사이즈가 필요해요"
"버그: 클릭이 안됨"

Claude가 감지하고 물어봅니다:
```

**Issue 공유 확인 (AskUserQuestion)**:
```
불만/추가요청을 감지했습니다.

다음을 Issue로 등록하시겠습니까?

제목: "Button 컴포넌트: 색상 불일치"

[Yes - Bug] 버그로 등록
[Yes - Enhancement] 개선요청으로 등록
[No] 로컬에만 저장
[Edit] 내용 수정
```

**Issue 생성**:
- 라벨: bug 또는 enhancement (선택한 유형)
- 내용: 사용자 피드백 + 맥락 정보
- 작성자: 사용자명 + 역할

---

## 사용 방법

### 명령어 실행
```bash
/designer
```

### 단계별 진행 (요약)
```
1. 프레임워크 선택 (Web/Native)
2. 액션 선택 (생성/확장/수정)
3. 정보 입력 (이름, 설명 등)
4. 코드 생성
5. 검증 (Strict Mode)
6. Storybook 실행
7. 사용자 검증 요청
8. 검증 결과 처리
9. PR 생성 또는 로컬 저장
10. 불만/피드백 → Issue 공유
```

---

## 워크플로우 다이어그램

```
1. 사용자 입력
 ├─ 프레임워크 선택
 ├─ 컴포넌트 목록 표시
 └─ 액션 선택 (생성/확장/수정)

2. 액션 처리
 ├─ [생성] 덮어쓰기 방지 → 코드/스토리 생성
 ├─ [확장] 검색 → API 확인 → 스토리/변형 추가
 └─ [수정] 검색 → 코드 표시 → diff 확인 후 저장

3. 검증 (Strict Mode)
 ├─ npm run verify:fast
 ├─ Format + Lint + Type-check + Test
 └─ 실패 시 최대 3회 재시도

4. Storybook 실행
 ├─ 포트 6006 정리
 ├─ npm run storybook
 └─ 브라우저 자동 띄우기

5. 사용자 검증
 ├─ Storybook에서 시각적/기능/접근성 확인
 └─ 검증 결과 입력

6. 검증 결과 처리
 ├─ 완료 → PR 공유 확인
 ├─ 미완료 → 수정 → 재검증
 └─ 질문 → 답변 → 재검증

7. PR 생성 또는 로컬 저장
 ├─ git checkout -b component/{name}
 ├─ git add/commit/push
 └─ gh pr create로 자동 PR 생성
 또는 로컬 저장

8. 불만/피드백 감지
 └─ Issue 공유 확인 → Issue 생성 또는 로컬 저장
```

---

## 컴포넌트 탐색 절차

### 현재 컴포넌트 목록 (Web 예시)

```
현재 등록된 WEB 컴포넌트 (25개):

 - accordion [story]
 - alert [story]
 - avatar [story]
 - badge [story]
 - button [story]
 - card [story]
 - checkbox [story]
 - dialog [story]
 - form [story]
 - header [story]
 - input [story]
 - navbar [story]
 - popover [story]
 - pricing-card [story]
 - radio [story]
 - select [story]
 - sidebar [story]
 - skeleton [story]
 - stat-card [story]
 - switch [story]
 - table [story]
 - tabs [story]
 - toast [story]
 - tooltip [story]
```

### 부분 일치 검색

| 검색어 | 결과 |
|--------|------|
| "btn" | button |
| "card" | card, stat-card, pricing-card |
| "input" | input |
| "tab" | table, tabs |
| "select" | select |

---

## 덮어쓰기 방지 절차

새 컴포넌트 생성 시 동일 이름 파일이 이미 존재하면:

```
[WARNING] 'button.tsx' 파일이 이미 존재합니다: components/web/ui/button.tsx

기존 컴포넌트를 덮어쓰면 코드가 손실됩니다.

덮어쓰시겠습니까?
[Yes] 기존 파일 덮어쓰기
[No] 취소

→ No 선택 시:
[TIP] '기존 컴포넌트 확장' 또는 '기존 컴포넌트 수정'을 사용해보세요.
```

---

## 검증 항목 (Strict Mode)

```
 Format (Prettier)
 - 라인 너비: 100
 - 세미콜론: 필수
 - 트레일링 콤마: all

 Lint (ESLint)
 - react/prop-types: error
 - @typescript-eslint/no-unused-vars: error
 - @typescript-eslint/no-any: error
 - 경고(warn)도 실패로 처리

 Type-check (TypeScript)
 - strict: true
 - noUnusedLocals: true
 - noUnusedParameters: true

 Test (Unit + Integration)
 - 통과율: 100%
```

---

## PR 본문 포맷

```markdown
## 변경사항

- 새 Button 컴포넌트 생성
- 5가지 variant 지원 (default, outlined, ghost, destructive, link)
- 3가지 크기 지원 (sm, md, lg)

## 검증 정보

- **검증자**: 박나현
- **검증 완료**: 2026-02-25 14:30:00
- **검증 항목**:
 - [x] 시각적 일치성 — Figma와 일치
 - [x] 기능 동작 — 모든 상태 정상
 - [x] 접근성 — 키보드 네비게이션 가능
 - [x] 반응형 — 모바일/태블릿/데스크톱 정상

## 테스트

- [x] 모든 테스트 통과
- [x] Storybook 렌더링 확인
- [x] 품질 검증 (Strict Mode)

## 참고

- Storybook: http://localhost:6006
```

---

## 상태 저장 (로컬 Fallback)

### 검증 상태
```
.claude/state/validations/designer/
├── button_20260225_143000.json
└── input_20260225_150000.json
```

**파일 내용**:
```json
{
 "component": "Button",
 "status": "validation_passed",
 "validator": "박나현",
 "validation_date": "2026-02-25T14:30:00Z",
 "notes": "모든 상태 정상",
 "pr_created": false
}
```

### 보류 중인 공유
```
.claude/state/pending-shares/designer/
└── button_to_share.json
```

---

## 참고 자료

- [컴포넌트 스펙](../spec/component-spec.md)
- [검증 및 공유 플로우](../spec/validation-flow.md)
- [PR 템플릿](../templates/pr-template.md)
- [Emocog 테마](../manifests/theme.yaml)
- [GitHub 기본 라벨](https://github.com/boydcog/service-flow-template/labels)
