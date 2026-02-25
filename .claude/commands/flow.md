# /flow — 서비스 플로우 생성

## 개요

완성된 컴포넌트를 활용하여 서비스 플로우를 설계합니다. 모든 역할이 사용할 수 있습니다.

**권한**: 모든 역할 (admin, developer, designer, pm)

**특징**:
- PM이 주도 (기획자)
- Designer가 지원 (컴포넌트 추천)
- Developer가 검토 (기술 검증)
- PR을 통해 main에 병합

---

## Claude 실행 지시

이 명령을 실행할 때 Claude가 따라야 할 단계:

### 0단계: Git 동기화 및 마이그레이션 (필수)

```bash
echo "🔄 최신 상태 동기화 중..."

# 1. Git 동기화
git fetch origin
if ! git pull --rebase origin main 2>&1 | grep -q "Already up to date"; then
  echo "✅ 최신 커밋 적용됨"
else
  echo "✅ 이미 최신 상태"
fi

# 2. 마이그레이션 감지 및 자동 실행
CURRENT_SCHEMA=$(cat ".claude/state/_schema_version.txt" 2>/dev/null || echo "v1")
TARGET_SCHEMA=$(cat ".claude/migrations/_target_version.txt" 2>/dev/null || echo "v1")

if [ "$CURRENT_SCHEMA" != "$TARGET_SCHEMA" ]; then
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
    echo "⚠️  마이그레이션 스크립트 없음: $MIGRATION_SCRIPT"
  fi
fi

echo ""
```

### 1단계: 선행 조건 확인

#### 1-1. 신원 파일 확인
`.user-identity` 파일이 없으면 Skill("setup") 먼저 실행

#### 1-2. 권한 검증 (모든 역할 가능)
```bash
if [ ! -f .user-identity ]; then
  echo "❌ 사용자 신원이 설정되지 않았습니다"
  echo "먼저 /setup을 실행해주세요"
  exit 1
fi

# 사용자 정보 로드
USER_NAME=$(grep '^name:' .user-identity | sed 's/name: //')
USER_ROLE=$(grep '^role:' .user-identity | sed 's/role: //')

# 권한 검증: flow는 모든 역할 가능
echo "✅ 권한 확인 완료"
echo "역할: $USER_ROLE | 사용자: $USER_NAME"
echo ""
echo "이 세션에서는 /flow를 사용해서 서비스 플로우를 설계합니다."
```

#### 1-3. 깃 동기화
Git pull --rebase 실행

### 2단계: 플로우 정보 수집 (AskUserQuestion)

#### 2-1. 제품명 선택 또는 입력
```
제품명을 입력하세요:

사전 정의된 예:
- user-onboarding
- payment-flow
- product-dashboard

또는 새로운 이름 입력:
> signup-wizard
```

#### 2-2. 기능 설명 (자유 형식, 바이브코딩)
```
기능을 자유롭게 설명해주세요:

예:
> 사용자 회원가입 플로우
> 1. 이메일 입력 (검증)
> 2. 패스워드 설정 (강도 표시)
> 3. 프로필 정보 (이름, 사진)
> 4. 완료 메시지
```

### 3단계: 브랜치 생성 및 git 설정
```bash
git checkout -b flow/{product-name}
git pull --rebase origin main
```

### 4단계: 컴포넌트 탐색
- 현재 사용 가능한 컴포넌트 목록 표시
- Web 컴포넌트 24개 표시
- 각 컴포넌트의 Props/variants 설명

### 5단계: 화면 설계 및 컴포넌트 매핑

#### 화면 목록 자동 생성
사용자 설명에서 화면 추출:

```
감지된 화면:
1. EmailInput Screen
2. PasswordSetup Screen
3. ProfileInfo Screen
4. Completion Screen
```

#### 컴포넌트 추천
각 화면에 적합한 컴포넌트 자동 추천:

```
Screen 1: EmailInput
├─ 추천 컴포넌트:
│ ├─ Input (email 입력)
│ ├─ Button (다음 버튼)
│ └─ Alert (검증 오류)

Screen 2: PasswordSetup
├─ 추천 컴포넌트:
│ ├─ Input (password 입력)
│ ├─ Progress (강도 표시)
│ └─ Button (다음 버튼)
```

### 6단계: 페이지 생성

생성되는 파일:
```
flows/{product-name}/
├── screens/
│ ├── Screen1.tsx (EmailInput)
│ ├── Screen2.tsx (PasswordSetup)
│ ├── Screen3.tsx (ProfileInfo)
│ └── Screen4.tsx (Completion)
├── page.tsx (메인 플로우)
└── types.ts (타입 정의)
```

**예시 코드 구조**:
```typescript
// flows/signup-wizard/page.tsx
import { useState } from 'react'
import Screen1 from './screens/Screen1'
import Screen2 from './screens/Screen2'
// ...

export default function SignupFlow() {
 const [step, setStep] = useState(0)

 return (
 <div>
 {step === 0 && <Screen1 onNext={() => setStep(1)} />}
 {step === 1 && <Screen2 onNext={() => setStep(2)} />}
 // ...
 </div>
 )
}
```

### 7단계: 검증 (Strict Mode)

```bash
npm run verify:fast
```

검증 항목:
- 컴포넌트 import 정확성
- TypeScript 타입 검증
- ESLint 검사
- 테스트 실행

실패 시 최대 3회 재시도 → PR 생성 불가

### 8단계: Dev 서버 실행 및 사용자 검증 요청

**Dev 서버 시작**:
```bash
npm run dev
# http://localhost:3000 자동 열기
```

**사용자 검증 요청 (AskUserQuestion)**:
```
개발이 완료되었습니다!

이제 Dev 서버에서 다음을 확인해주세요:

1. 플로우 연결
 - 모든 화면이 순서대로 연결됨
 - 네비게이션 버튼 정상 작동
 - 이전 화면 돌아가기 가능

2. 컴포넌트 렌더링
 - 모든 컴포넌트가 정상 표시
 - 레이아웃이 일관성 있음

3. 기능 동작
 - 입력 필드 정상 작동
 - 버튼/링크 클릭 동작
 - 폼 유효성 검증

4. 반응형
 - 모바일 (375px)
 - 태블릿 (768px)
 - 데스크톱 (1920px)

검증이 완료되셨나요?

[O] 완료 - 모두 정상
[X] 미완료 - 수정 필요
[?] 질문 있음
```

### 9단계: 검증 결과 처리

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
> Screen 2에서 버튼이 안보임
> 진행률이 업데이트 안됨

Claude:
1. 문제 분석
2. 코드 수정
3. Dev 서버 재확인 요청
4. 재검증 플로우
```

#### 질문 있음 
```
어떤 부분이 궁금하신가요?

사용자 질문 → Claude 답변 → 재검증 요청
```

### 10단계: PR 생성 또는 로컬 저장

**PR 생성 선택 시**:
- 브랜치 명: `flow/{product-name}`
- PR 제목: `[flow] {사용자명}: {플로우명}`
- PR 본문: 변경사항 + 검증 정보 + 스크린샷
- 라벨: `enhancement`
- flows/ .gitignore 자동 해제: `git update-index --no-skip-worktree flows/`

**로컬 저장 선택 시**:
```
.claude/state/pending-shares/flow/
└── signup-wizard.json
```

### 11단계: 불만/피드백 감지 및 Issue 공유 (선택)

**피드백 감지**:
```
개발 중 또는 완료 후 사용자가:

"첫 화면에서 네비게이션 바 필요해 보임"
"화면 전환 애니메이션이 필요해요"
"모바일에서 글씨가 너무 작음"

Claude가 감지하고 물어봅니다:
```

**Issue 공유 확인 (AskUserQuestion)**:
```
불만/추가요청을 감지했습니다.

다음을 Issue로 등록하시겠습니까?

제목: "회원가입 플로우: 모바일 글씨 크기 조정"

[Yes - Bug] 버그로 등록
[Yes - Enhancement] 개선요청으로 등록
[No] 로컬에만 저장
[Edit] 내용 수정
```

---

## 사용 방법

### 명령어 실행
```bash
/flow
```

### 단계별 진행 (요약)
```
1. 플로우 정보 수집 (제품명, 기능 설명)
2. 브랜치 생성
3. 컴포넌트 탐색
4. 화면 설계 및 컴포넌트 매핑
5. 페이지 생성
6. 검증 (Strict Mode)
7. Dev 서버 실행
8. 사용자 검증 요청
9. 검증 결과 처리
10. PR 생성 또는 로컬 저장
11. 불만/피드백 → Issue 공유
```

---

## 워크플로우 다이어그램

```
1. 사용자 입력
 ├─ 제품명 선택
 └─ 기능 설명 (바이브코딩)

2. 브랜치 생성
 └─ git checkout -b flow/{product-name}

3. 컴포넌트 탐색
 ├─ 사용 가능한 컴포넌트 목록
 └─ 각 컴포넌트 API 설명

4. 화면 설계
 ├─ 기능 설명에서 화면 추출
 └─ 각 화면에 컴포넌트 매핑

5. 페이지 생성
 ├─ flows/{product-name}/screens/*.tsx 생성
 └─ flows/{product-name}/page.tsx (메인)

6. 검증 (Strict Mode)
 └─ npm run verify:fast

7. Dev 서버 실행
 ├─ npm run dev
 └─ http://localhost:3000

8. 사용자 검증
 ├─ 플로우 연결 확인
 ├─ 컴포넌트 렌더링 확인
 ├─ 기능 동작 확인
 └─ 반응형 확인

9. 검증 결과 처리
 ├─ 완료 → PR 공유 확인
 ├─ 미완료 → 수정 → 재검증
 └─ 질문 → 답변 → 재검증

10. PR 생성 또는 로컬 저장
 ├─ git checkout -b flow/{name}
 ├─ git add/commit/push
 ├─ flows/ .gitignore 해제
 └─ gh pr create로 자동 PR 생성

11. 불만/피드백 감지
 └─ Issue 공유 확인 → Issue 생성 또는 로컬 저장
```

---

## 사용 가능한 컴포넌트

### 레이아웃/구조
- header, navbar, sidebar, card, container

### 입력
- input, button, select, checkbox, radio, switch, form

### 표시
- badge, avatar, alert, tooltip, toast, skeleton

### 고급
- dialog, popover, tabs, accordion, table, pricing-card

**전체 25개 컴포넌트 사용 가능**

---

## PR 본문 포맷

```markdown
## 변경사항

- 새 회원가입 플로우 생성 (4개 화면)
- 이메일 검증 + 비밀번호 설정 + 프로필 정보
- 완료 확인 메시지

## 화면 구성

1. EmailInput — 이메일 입력 및 검증
2. PasswordSetup — 비밀번호 설정 (강도 표시)
3. ProfileInfo — 프로필 정보 (이름, 사진)
4. Completion — 완료 메시지

## 검증 정보

- **검증자**: 홍길동
- **검증 완료**: 2026-02-25 15:00:00
- **검증 항목**:
 - [x] 플로우 연결 — 모든 화면 정상 연결
 - [x] 컴포넌트 렌더링 — 모두 정상 표시
 - [x] 기능 동작 — 입력/버튼 정상
 - [x] 반응형 — 모바일/태블릿/데스크톱 정상

## 테스트

- [x] 모든 테스트 통과
- [x] Dev 서버 렌더링 확인
- [x] 품질 검증 (Strict Mode)

## 참고

- Dev 서버: http://localhost:3000
- 화면 구조: flows/signup-wizard/
```

---

## 상태 저장 (로컬 Fallback)

### 검증 상태
```
.claude/state/validations/flow/
├── signup_20260225_150000.json
└── payment_20260225_153000.json
```

### 보류 중인 공유
```
.claude/state/pending-shares/flow/
└── signup_to_share.json
```

---

## flows/ .gitignore 처리

### main 브랜치
```bash
# flows/는 .gitignore 됨 (로컬 전용)
git check-ignore flows/ # true
```

### flow/{product-name} 브랜치
```bash
# PR 생성 전 자동으로 해제
git update-index --no-skip-worktree flows/

# 결과: flows/의 모든 파일이 PR에 포함
```

---

## 참고 자료

- [플로우 스펙](../spec/flow-spec.md)
- [검증 및 공유 플로우](../spec/validation-flow.md)
- [PR 템플릿](../templates/pr-template.md)
- [컴포넌트 API](../manifests/component-api.md)
- [GitHub 기본 라벨](https://github.com/boydcog/service-flow-template/labels)
