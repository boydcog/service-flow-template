# Service Flow Template — 전사 배포 Claude Code 템플릿

## 코드 작성 규칙

- 이모지 사용 금지 — 코드, 문서, 주석, 응답 모두에서

---

## 자동 의도 감지 (Intent Detection)

명시적인 `/command` 없이도 사용자 요청을 분석해 적절한 Skill을 자동 실행합니다.

### 선행 조건 확인

모든 요청 처리 전, `.user-identity` 파일 존재 여부 확인:
- 없으면 → Skill("setup") 먼저 실행

### 요청 패턴 → 자동 실행

| 요청 패턴 | 자동 실행 | 권한 |
|----------|-----------|------|
| "컴포넌트 만들어줘", "버튼 추가", "UI 수정", "스토리 만들어줘", "카드 만들어", "입력창 만들기" | Skill("designer") | designer+ |
| "플로우 만들어줘", "화면 설계", "서비스 기획", "앱 만들어줘", "페이지 만들어줘", "온보딩 만들어" | Skill("flow") | 모든 역할 |
| "이슈 등록", "버그 제보", "피드백 남길게", "신고할게", "문제 보고" | Skill("create-issue") | 모든 역할 |
| "팀원 추가", "테마 수정", "스펙 업데이트", "권한 변경", "템플릿 관리" | Skill("admin") | admin/developer만 |
| 신원 파일 없음 또는 "설정해줘", "처음 설정", "초기화", "계정 만들기" | Skill("setup") | 모든 역할 |

**권한 없는 역할이 요청 시**: 역할과 필요 권한을 안내하고 중단합니다.

---

## GitHub 토큰 검증 규칙 (필수)

**모든 GitHub 작업 전에 반드시 실행**:

### 1단계: `.gh-token` 파일 확인
```bash
if [ ! -f .gh-token ]; then
  # 토큰 파일 없음
  echo "❌ .gh-token 파일이 없습니다."
  echo "템플릿 관리자에게 문의하세요:"
  grep -A 5 "^admins:" .claude/manifests/admins.yaml | grep -E "name|github|email"
  exit 1
fi
```

### 2단계: 토큰 유효성 검증
```bash
GH_TOKEN=$(cat .gh-token)
if [ -z "$GH_TOKEN" ]; then
  echo "❌ .gh-token이 비어있습니다."
  echo "템플릿 관리자에게 문의하세요"
  exit 1
fi

# API 호출로 검증
if ! curl -s -H "Authorization: token $GH_TOKEN" https://api.github.com/user > /dev/null 2>&1; then
  echo "❌ 토큰이 유효하지 않습니다."
  echo "템플릿 관리자에게 문의하세요"
  exit 1
fi
```

### 3단계: 토큰으로 인증 후 git 작업
```bash
GH_TOKEN=$(cat .gh-token)
git remote set-url origin "https://${GH_TOKEN}@github.com/boydcog/service-flow-template.git"
git push -u origin main
# 이후 URL에서 토큰 제거 (보안)
git remote set-url origin "https://github.com/boydcog/service-flow-template.git"
```

### 관리자 정보
`.gh-token` 없거나 토큰이 유효하지 않으면 아래 관리자에게 문의:
- **이름**: 보이드
- **GitHub**: boydcog
- **역할**: maintainer

---

## 프로젝트 개요

이 레포지토리는 회사 전체가 공유하는 **Claude Code 템플릿**입니다. 세 가지 역할이 협업하여 공통 컴포넌트 라이브러리와 서비스 플로우를 구축합니다:

- **Admin/Developer**: 템플릿과 컴포넌트 스펙 관리 (`/admin`)
- **Designer**: Emocog 테마 기반 컴포넌트 제작·수정 (`/designer`)
- **PM**: 완성된 컴포넌트로 서비스 플로우 바이브코딩 (`/flow`)

**GitHub가 Single Source of Truth(SSoT)이며, 매 세션 시작 시 자동으로 동기화됩니다.**

---

## 빠른 시작

### 1단계: 신원 설정
```bash
/setup
```
- 이름, 역할(admin/developer/designer/pm), GitHub 정보 입력
- GH Access Token 저장

### 2단계: 역할별 작업
- **Designer**: `/designer` → 컴포넌트 생성/수정
- **PM**: `/flow` → 서비스 플로우 생성
- **Admin**: `/admin` → 템플릿 관리

### 3단계: 공유
- PR 자동 생성 → 리뷰 → 메인 브랜치 병합

---

## 명령어 가이드

### `/setup` — 초기 설정 (모든 역할)
최초 세션에서 한 번만 실행합니다.

**입력**:
- 사용자 이름
- 역할 선택 (admin/developer/designer/pm)
- GitHub 사용자명
- GH Access Token

**생성 파일**:
- `.user-identity` (로컬, git에서 skip)
- `.gh-token` (로컬, git에서 skip)

---

### `/admin` — 템플릿 관리 (admin/developer만)
템플릿 규칙, 팀 관리, 테마 업데이트를 담당합니다.

**선택 사항**:
1. 컴포넌트 스펙 수정 → `spec/component-spec.md`
2. 역할 및 권한 수정 → `manifests/roles.yaml`
3. 팀원 추가 → `manifests/team.yaml`
4. Emocog 테마 업데이트 → `manifests/theme.yaml`

**프로세스**:
- git worktree 생성 (메인 브랜치 보호)
- 파일 수정
- CHANGELOG 업데이트
- PR 자동 생성

---

### `/designer` — 컴포넌트 제작·수정 (designer)
Emocog 테마를 기반으로 컴포넌트를 만들거나 수정합니다.

**프레임워크 선택**:
- **Web**: Next.js (App Router/Pages), Vite + React, Remix
- **Native**: React Native (Gluestack)

**액션**:
1. 새 컴포넌트 생성
2. 기존 컴포넌트 수정
3. 컴포넌트 스펙 업데이트

**생성 위치**:
- Web: `components/web/{component-name}.tsx`
- Native: `components/native/{component-name}.tsx`

**PR 제목 형식**:
```
[designer] {사용자명}: {컴포넌트명}
```

---

### `/flow` — 서비스 플로우 생성 (모든 역할)
기존 컴포넌트를 활용하여 서비스 플로우를 설계합니다.

**프로세스**:
1. 제품명 입력 → `flow/{product-name}` 브랜치 자동 생성
2. 기능 설명 자유 입력 (바이브코딩)
3. 관련 컴포넌트 자동 탐색
4. 화면 설계 → 네비게이션 → 데이터 플로우
5. `flows/{product-name}/` 아래 저장

**공유 방법**:
```bash
# (자동 실행, 또는 수동)
git update-index --no-skip-worktree flows/
```
→ PR 생성 → 메인 브랜치로 병합

**주의**: main 브랜치에서 `flows/`는 `.gitignore`되어 있습니다. 공유 시 자동으로 해제됩니다.

---

### `/create-issue` — 이슈 제보 (모든 역할)
버그 리포트, 기능 요청, 피드백을 GitHub 이슈로 생성합니다.

**입력**:
- 제목
- 내용

**자동 처리**:
- 키워드 기반 라벨 자동 추가 (bug/enhancement/feedback)
- `gh issue create` 실행
- GH_TOKEN 없으면 로컬 `.state/pending-issues/` 저장

---

## 디렉토리 구조

```
service-flow-template/
├── .claude/
│   ├── commands/
│   │   ├── setup.md              # /setup 명령어 구현
│   │   ├── admin.md              # /admin 명령어 구현
│   │   ├── designer.md           # /designer 명령어 구현
│   │   ├── flow.md               # /flow 명령어 구현
│   │   └── create-issue.md       # /create-issue 명령어 구현
│   ├── manifests/
│   │   ├── roles.yaml            # 역할별 권한 정의
│   │   ├── team.yaml             # 팀원 명단 (admin 관리)
│   │   └── theme.yaml            # Emocog 테마 레퍼런스
│   ├── spec/
│   │   ├── component-spec.md     # 컴포넌트 생성 규칙 (프레임워크별)
│   │   └── flow-spec.md          # 서비스 플로우 컨벤션
│   ├── templates/
│   │   ├── pr-template.md        # PR 본문 템플릿
│   │   └── issue-template.md     # 이슈 본문 템플릿
│   ├── hooks/
│   │   ├── startup.sh            # 세션 시작 훅 (git sync + 신원 로드)
│   │   └── startup.ps1           # Windows 동등 구현
│   └── settings.json             # Claude 권한 + 훅 + env 설정
├── components/
│   ├── web/                      # Next.js / Vite / Remix 컴포넌트
│   ├── native/                   # React Native (Gluestack) 컴포넌트
│   └── theme/
│       ├── tokens.css            # Emocog CSS 변수
│       └── gluestack-theme.ts    # Gluestack 토큰 매핑
├── flows/                        # main에서는 gitignored
│   └── .gitkeep
├── .gitignore
└── CLAUDE.md                     # 이 파일
```

---

## 브랜치 전략

| 브랜치 | 내용 | `flows/` 추적 |
|--------|------|--------|
| `main` | 템플릿 + 컴포넌트 라이브러리 | ❌ gitignored |
| `flow/{product-name}` | 제품별 서비스 플로우 | ✅ 추적됨 |

**워크플로우**:
1. PM이 `/flow {product-name}` 실행
2. `flow/{product-name}` 브랜치 자동 생성 (main에서 분기)
3. 로컬에서 바이브코딩 및 테스트
4. 완료 후 PR 생성 (자동 또는 `/share-flow` 명령)
5. 리뷰 후 main으로 병합

---

## 사용자 신원 파일 (`.user-identity`)

```
name: 홍길동
role: designer
github: hong-gildong
```

**주의**: 이 파일은 `.gitignore` + `git skip-worktree`로 보호됩니다. 로컬 환경에만 유지되며 git에 커밋되지 않습니다.

---

## 세션 시작 자동화

매 세션 시작 시 `.claude/hooks/startup.sh`가 자동 실행되어:

1. ✅ 사용자 신원 로드
2. ✅ GH 토큰 로드
3. ✅ 로컬 파일 보호 (git skip-worktree)
4. ✅ Git 동기화 (pull --rebase)
5. ✅ 상태 리포트 출력

```
=== Service Flow Template — Session Start ===
✅ 안녕하세요, 홍길동 (designer)!

📦 웹 컴포넌트: 12개
📱 네이티브 컴포넌트: 5개
🌿 브랜치: main

명령어: /setup  /admin  /designer  /flow  /create-issue
```

---

## ✅ 품질 검증 규칙 (Strict Mode)

**모든 산출물은 품질 검증을 "무조건" 통과해야만 완료로 인정됩니다.**

### 핵심 원칙
- Storybook과 PM이 생성한 모든 산출물 = 검증 필수
- 검증 기준 = TypeScript strict + ESLint strict + Prettier formatting + 100% Test Pass
- 검증 실패 = PR 생성 불가

### 검증 단계 (4가지 Strict 기준)

#### 1단계: Format (Prettier - Auto-fix)
```bash
npm run format
```
**Strict 규칙**:
- 라인 너비: 100
- 탭 너비: 2
- 세미콜론: 필수
- 트레일링 콤마: all
- 포맷 미준수 시 자동 수정

#### 2단계: Lint (ESLint - Error 레벨)
```bash
npm run lint
```
**Strict 규칙**:
- `react/prop-types: "error"` (warn → error)
- `@typescript-eslint/no-unused-vars: "error"`
- `@typescript-eslint/no-any: "error"`
- `react-hooks/rules-of-hooks: "error"`
- `react-hooks/exhaustive-deps: "error"`
- **경고(warn) 없음** → 경고도 실패로 처리

#### 3단계: Type Check (TypeScript - Strict)
```bash
npm run type-check
```
**Strict 설정** (이미 활성화):
- `"strict": true` ✅
- `"noUnusedLocals": true` ✅
- `"noUnusedParameters": true` ✅
- `"noFallthroughCasesInSwitch": true` ✅

#### 4단계: Test (Unit + Integration)
```bash
npm run test
```
**Strict 규칙**:
- 통과율: 100%
- 비동기 처리 테스트 필수
- 에러 핸들링 테스트 필수

### 검증 명령어

#### 전체 검증 (최종)
```bash
npm run verify
```
Format + Lint + Type-check + Test + Playwright 스크린샷 (1-2분)

#### 빠른 검증 (개발 중)
```bash
npm run verify:fast
```
Format + Lint + Type-check + Test (15초)

### 자동화 설정

**`.claude/hooks/post-designer.sh`** — 컴포넌트 생성 후
- 자동으로 품질 검증 실행
- 검증 실패 시 PR 생성 불가
- 검증 성공 시만 PR 생성 가능

**`.claude/hooks/post-flow.sh`** — 플로우 생성 후
- 자동으로 품질 검증 실행
- 검증 실패 시 PR 생성 불가
- 검증 성공 시만 PR 생성 가능

### Claude 코드 생성 기준 (Strict Mode)

**모든 Claude 생성 코드는 다음 기준으로 작성**:

1. **TypeScript Strict 모드** 준수
   - 모든 타입 명시적 지정
   - `any` 타입 금지
   - 반환 타입 필수 작성

2. **Props 인터페이스** 정의
   ```typescript
   export interface MyComponentProps extends React.HTMLAttributes<HTMLDivElement> {
     variant?: "default" | "outlined"
     size?: "sm" | "md" | "lg"
   }
   ```

3. **에러 핸들링** 필수
   - try-catch로 예외 처리
   - 사용자 피드백 메시지 포함

4. **테스트 케이스** 포함
   - 기본 렌더링 테스트
   - Props 변화 테스트
   - 에러 상황 테스트

5. **JSDoc 주석** (공개 API)
   ```typescript
   /**
    * 사용자 입력을 받는 폼 컴포넌트
    * @param props - 컴포넌트 props
    * @returns 렌더링된 폼 요소
    */
   ```

6. **Prettier 포맷** 사전 적용
   - 라인 너비 100
   - 세미콜론 필수
   - 트레일링 콤마

### Storybook 스토리 작성 규칙

모든 Web 컴포넌트는 Storybook 스토리를 포함해야 합니다:

```bash
components/web/ui/my-component.tsx
components/web/ui/my-component.stories.tsx  ← 필수!
```

스토리 파일 템플릿:
```typescript
import type { Meta, StoryObj } from '@storybook/react'
import { MyComponent } from './my-component'

const meta = {
  title: 'Web/MyComponent',
  component: MyComponent,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'outlined'],
    },
  },
} satisfies Meta<typeof MyComponent>

export default meta
type Story = StoryObj<typeof meta>

/**
 * 기본 상태
 */
export const Default: Story = {
  args: {
    children: 'Default',
  },
}

/**
 * Outlined 변형
 */
export const Outlined: Story = {
  args: {
    variant: 'outlined',
    children: 'Outlined',
  },
}
```

### 검증 실패 예시

```
⚠️  품질 검증 실패 (Strict Mode)

[Format]      ✅ 코드 포맷 정상

[Lint]        ❌ 1 error
  - Line 45: react/prop-types: prop 'variant' is missing

[Type-check]  ❌ 2 errors
  - Line 78: Type 'string' is not assignable to type 'never'
  - Line 92: Object is possibly 'undefined'

[Test]        ✅ 모든 테스트 통과

❌ 린트와 타입 에러를 먼저 해결하세요.
수동 수정 또는 npm run lint -- --fix 실행 후 재검증하세요.

PR 생성 불가.
```

### 검증 성공 예시

```
========================================
✅ 품질 검증 완료 (Strict Mode 통과)
========================================

📊 검증 결과:
  [Format]      ✅ 코드 포맷 정상
  [Lint]        ✅ 에러 0개
  [Type-check]  ✅ 타입 검증 통과
  [Test]        ✅ 모든 테스트 통과

🎉 완료! PR 생성 가능합니다.
```

---

## Emocog 테마

프로젝트 전체 디자인은 **Emocog 테마**를 기반으로 합니다.

**참고**:
- 색상 정의: `.claude/manifests/theme.yaml`
- CSS 변수: `components/theme/tokens.css`
- Gluestack 토큰: `components/theme/gluestack-theme.ts`

디자이너가 새 컴포넌트 생성 시:
- Web: Tailwind CSS + theme 변수 사용
- Native: Gluestack 토큰 참조

---

## Web-Native 컴포넌트 동기화

**핵심 원칙**: Web과 Native 컴포넌트는 동일한 Props API를 제공하되, 스타일링 구현만 다릅니다.

### 디렉토리 구조
```
components/
├── web/ui/
│   ├── button.tsx          # Web: shadcn/ui + Tailwind
│   ├── input.tsx
│   ├── card.tsx
│   └── ...
├── native/ui/
│   ├── Button.tsx          # Native: PascalCase + Gluestack
│   ├── Input.tsx
│   ├── Card.tsx
│   └── ...
└── theme/
    ├── tokens.css          # Web CSS 변수 (Tailwind v4)
    └── gluestack-theme.ts  # Native Gluestack 토큰
```

### 명명 규칙
- **Web**: 소문자 파일명 (예: `button.tsx`)
- **Native**: PascalCase 파일명 (예: `Button.tsx`)

### Props API 동기화
모든 컴포넌트는 동일한 Props 인터페이스를 제공해야 합니다:

```typescript
// Web ✅
export interface ButtonProps extends React.ComponentPropsWithoutRef<"button"> {
  variant?: "default" | "destructive" | "outline" | "secondary" | "ghost" | "link"
  size?: "default" | "sm" | "lg" | "icon"
}

// Native ✅ (동일한 Props)
export interface ButtonProps extends React.ComponentPropsWithoutRef<typeof GluestackButton> {
  variant?: "default" | "destructive" | "outline" | "secondary" | "ghost" | "link"
  size?: "default" | "sm" | "lg" | "icon"
}
```

### 테마 동기화
Web 컴포넌트 변경 시:
1. `components/theme/tokens.css` 업데이트 (CSS 변수)
2. `components/theme/gluestack-theme.ts` 동시 업데이트 (Gluestack 토큰)
3. 두 파일의 색상/크기/레이아웃이 1:1 매핑되어야 함

### 동기화 확인
매 세션 시작 시 자동으로 실행되며, 다음을 검증합니다:

```bash
# 수동 실행
./.claude/hooks/check-sync.sh
```

**확인 항목**:
- Web 컴포넌트마다 Native 짝 컴포넌트 존재
- 파일명 일관성 (web: lowercase, native: PascalCase)
- 총 컴포넌트 개수 일치

### 컴포넌트 추가 절차

#### 1단계: Web 컴포넌트 작성
```typescript
// components/web/ui/mycomponent.tsx
export interface MyComponentProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "outlined"
  size?: "sm" | "md" | "lg"
}

export const MyComponent = forwardRef<HTMLDivElement, MyComponentProps>(
  ({ variant = "default", size = "md", ...props }, ref) => {
    // Web 구현 (Tailwind CSS)
  }
)
```

#### 2단계: Native 컴포넌트 작성 (동일한 Props)
```typescript
// components/native/ui/MyComponent.tsx
export interface MyComponentProps extends React.ComponentPropsWithoutRef<typeof GluestackBox> {
  variant?: "default" | "outlined"
  size?: "sm" | "md" | "lg"
}

export const MyComponent = forwardRef<typeof GluestackBox, MyComponentProps>(
  ({ variant = "default", size = "md", ...props }, ref) => {
    // Native 구현 (Gluestack)
  }
)
```

#### 3단계: 테마 토큰 검증
- Web: `tokens.css`에서 색상/크기 사용 확인
- Native: `gluestack-theme.ts`에서 동일 값으로 정의 확인

#### 4단계: 동기화 검증
```bash
./.claude/hooks/check-sync.sh
```

---

## 완료 기준

- [ ] 모든 필수 명령어 구현 (`/setup`, `/designer`, `/flow`, etc.)
- [ ] `.user-identity` + `.gh-token` 로컬 보호 작동
- [ ] git 자동 동기화 확인
- [ ] 각 역할별 권한 검증 (designer는 `/admin` 거부, pm은 `/designer` 거부 등)
- [ ] 컴포넌트 및 플로우 PR 생성 작동
- [ ] 메인 브랜치 보호 (force-push 방지, 코드 리뷰 필수 등)

---

## 추가 리소스

- [GitHub CLI 문서](https://cli.github.com)
- [Figma Code Connect](https://www.figma.com/developers/code-connect)
- [Emocog Theme (tweakcn)](https://tweakcn.com/themes/cmlyp83mj000004kt9m73dbqt?p=custom)
- [Next.js 문서](https://nextjs.org/docs)
- [React Native (Gluestack)](https://gluestack.io)
