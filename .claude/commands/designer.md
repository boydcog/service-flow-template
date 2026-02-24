# /designer — 컴포넌트 제작·수정

## 개요

Emocog 테마를 기반으로 재사용 가능한 컴포넌트를 만들거나 기존 컴포넌트를 수정합니다.

**권한**: designer 이상 (admin, developer, designer)

---

## Claude 실행 지시

이 명령을 실행할 때 Claude가 따라야 할 단계:

1. 선행 조건 확인:
   - `.user-identity` 파일 존재 여부 확인
   - 없으면 Skill("setup") 먼저 실행
   - 존재하면 role 읽고 권한 검증 (role이 admin/developer/designer만 가능)
   - 권한 없으면: "역할 {role}은 /designer를 사용할 수 없습니다" → 중단

2. 프레임워크 선택 (AskUserQuestion):
   - Web (Next.js, Vite + React, Remix)
   - Native (React Native + Gluestack)

3. 액션 선택 (AskUserQuestion):
   - 새 컴포넌트 생성
   - 기존 컴포넌트 수정
   - 컴포넌트 스펙 업데이트

4. 입력 정보 수집 (각 액션별로 다름):
   - 컴포넌트 이름, 설명, Props 정의, 스타일 선택 등

5. 코드 생성:
   - `.claude/spec/component-spec.md` 참조하여 규칙 준수
   - TypeScript strict 모드 사용
   - Props 인터페이스 명시
   - 접근성(ARIA) 포함

6. 작업 완료 후:
   - 포트 6006 정리 및 Storybook 재시작 (필요 시)
   - PR 생성 지원

---

## 사용 방법

```bash
python3 scripts/designer.py
```

또는 Claude Code에서:
```
/designer
```

---

## 워크플로우

```
1️⃣  사용자 입력
   ├─ 프레임워크 선택 (Web/Native)
   ├─ 액션 선택 (생성/수정)
   └─ 컴포넌트 정보 입력

2️⃣  코드 생성
   ├─ 컴포넌트 파일 생성 (components/web/*.tsx)
   └─ 스토리 파일 생성 (*.stories.tsx)

3️⃣  Storybook 실행
   ├─ npm install (필요 시)
   ├─ npm run storybook
   └─ 브라우저 자동 띄우기 (localhost:6006)

4️⃣  사용자 검증
   ├─ Storybook에서 컴포넌트 상호작용 확인
   └─ Props, 다크 모드, 반응형 등 검증

5️⃣  PR 생성
   ├─ git worktree 자동 생성
   ├─ git add/commit/push
   └─ gh pr create로 자동 PR 생성
```

---

## 단계별 진행

### 1단계: 신원 및 권한 확인

```
✅ 신원: 홍길동 (designer)
✅ 권한: 컴포넌트 작업 가능

다음 단계: 프레임워크 선택
```

**권한 없음 시**:
```
❌ pm은 /designer 명령어를 사용할 수 없습니다.
필요 역할: designer 이상 (admin, developer, designer)
```

### 2단계: 프레임워크 선택

```
🏗️  프레임워크를 선택하세요:
  1. Web (Next.js, Vite + React, Remix)
  2. Native (React Native + Gluestack)

선택:
> 1
```

### 3단계: 액션 선택

```
🎯 액션을 선택하세요:
  1. ✨ 새 컴포넌트 생성
  2. ✏️  기존 컴포넌트 수정
  3. 📚 컴포넌트 스펙 업데이트

선택:
> 1
```

---

## 액션 1: 새 컴포넌트 생성

### 진행 과정

```
📦 새 웹 컴포넌트 생성
========================

1️⃣  컴포넌트 이름 입력:
> Button

2️⃣  컴포넌트 설명 입력:
> 재사용 가능한 버튼 컴포넌트

3️⃣  컴포넌트 유형:
  a) 기본 (Basic) — 단순 컴포넌트
  b) 폼 (Form) — 폼 입력 컴포넌트
  c) 콘테이너 (Container) — 레이아웃 컴포넌트
  d) 고급 (Advanced) — 복합 로직

선택:
> a

4️⃣  Props 정의:
속성 이름 (예: variant): variant
속성 타입 (예: string, boolean): 'primary' | 'secondary' | 'destructive'
필수 여부 (선택: y/n): n
설명: 버튼 스타일 변형
→ 더 추가? (y/n): n

5️⃣  스타일 테마:
  - primary (주색상)
  - secondary (보조색상)
  - destructive (위험)
  - muted (중립)

사용할 색상 (쉼표로 구분):
> primary, secondary

6️⃣  다크 모드:
다크 모드를 지원하시겠습니까? (y/n):
> y

7️⃣  반응형:
반응형 디자인을 포함하시겠습니까? (y/n):
> y

========================
✅ 컴포넌트 생성됨!

📍 위치: components/web/Button.tsx
📊 크기: 150 줄

생성된 코드:
────────────────────
import React from 'react'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'destructive'
  size?: 'sm' | 'md' | 'lg'
  children: React.ReactNode
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  children,
  className = '',
  ...props
}) => {
  const variantStyles = {
    primary: 'bg-primary text-primary-foreground hover:opacity-90',
    secondary: 'bg-secondary text-secondary-foreground hover:opacity-90',
    destructive: 'bg-destructive text-destructive-foreground hover:opacity-90',
  }

  const sizeStyles = {
    sm: 'px-3 py-1 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  }

  return (
    <button
      className={`
        rounded-md font-medium transition-all duration-200
        disabled:opacity-50 disabled:cursor-not-allowed
        dark:opacity-90
        ${variantStyles[variant]}
        ${sizeStyles[size]}
        ${className}
      `}
      {...props}
    >
      {children}
    </button>
  )
}
────────────────────

📝 다음 단계:
  1. 코드 검토 및 필요시 수정
  2. 테스트 작성
  3. PR 생성
```

---

## 액션 2: 기존 컴포넌트 수정

### 진행 과정

```
✏️  기존 웹 컴포넌트 수정
========================

1️⃣  수정할 컴포넌트 선택:

📦 사용 가능한 컴포넌트:
  1. Button.tsx (150 줄)
  2. Card.tsx (120 줄)
  3. Input.tsx (180 줄)
  4. Dialog.tsx (200 줄)

선택 또는 이름 입력:
> Button

2️⃣  현재 코드 표시:
────────────────────
// components/web/Button.tsx의 내용
────────────────────

3️⃣  수정할 부분 설명:
> hover 상태에서 색상 변화를 더 강하게 하고 싶습니다.

4️⃣  수정 사항 적용:
✅ 코드 수정됨

5️⃣  변경 사항 미리보기:

Before:
  hover:opacity-90

After:
  hover:brightness-110 hover:shadow-lg

6️⃣  수정 확인:
수정을 저장하시겠습니까? (y/n):
> y

========================
✅ 컴포넌트 수정됨!
📍 위치: components/web/Button.tsx

📝 다음 단계:
  1. 로컬에서 테스트
  2. 변경 사항이 올바른지 확인
  3. PR 생성
```

---

## 액션 3: 컴포넌트 스펙 업데이트

```
📚 컴포넌트 스펙 업데이트
========================

1️⃣  대상 스펙:
  1. component-spec.md (전체 컴포넌트 규칙)
  2. flow-spec.md (플로우 규칙)
  3. theme.yaml (테마 정의)

선택:
> 1

2️⃣  업데이트 내용:
> 웹 컴포넌트에 ARIA 접근성 예제 추가

3️⃣  문서 수정 및 저장됨!
✅ spec/component-spec.md 업데이트됨

📝 다음 단계:
  PR 생성
```

---

## PR 생성

모든 변경 후:

```
🔄 PR 생성을 시작합니다...

1️⃣  PR 정보:
제목: [designer] 홍길동: Button 컴포넌트 hover 상태 개선
본문: 템플릿 자동 적용 중...

2️⃣  변경 파일:
- components/web/Button.tsx (수정)

3️⃣  PR 옵션:
제목 수정? (y/n):
> n

본문 수정? (y/n):
> n

========================
✅ PR이 생성되었습니다!

📍 PR 링크: https://github.com/{owner}/{repo}/pull/123
📌 상태: Open (리뷰 대기 중)

리뷰 완료 시 자동으로 main에 병합됩니다.
```

---

## 컴포넌트 생성 모범 사례

### 1. 명확한 이름과 설명

```typescript
/**
 * Button 컴포넌트
 *
 * Emocog 테마 기반 재사용 가능한 버튼입니다.
 * variant와 size를 통해 다양한 스타일을 지원합니다.
 *
 * @example
 * <Button variant="primary" size="md">
 *   클릭하세요
 * </Button>
 */
```

### 2. Emocog 테마 사용

```typescript
// ✅ 좋음
className="bg-primary text-primary-foreground dark:bg-primary"

// ❌ 나쁨
className="bg-blue-500 text-white"
```

### 3. 접근성

```typescript
<button
  type="button"
  aria-label="메뉴 열기"
  aria-expanded={isOpen}
>
  {/* ... */}
</button>
```

### 4. 다크 모드 지원

```typescript
className="
  bg-white dark:bg-slate-950
  text-gray-900 dark:text-white
"
```

---

## 주의사항

### ❌ 피해야 할 것

- 커스텀 색상 사용 (Emocog 테마 벗어남)
- ARIA 라벨 누락
- 하드코딩된 값 (CSS 변수 미사용)
- 테스트 없이 제출

### ✅권장 사항

- 템플릿에 따라 구현
- 모든 Props TypeScript 타입 정의
- JSDoc 주석 작성
- 단위 테스트 포함
- 스토리북 스토리 추가 (선택)

---

## 체크리스트

완성 전 확인:

- [ ] 컴포넌트가 Emocog 테마를 사용합니다
- [ ] TypeScript 타입 정의가 완전합니다
- [ ] JSDoc 주석이 작성되었습니다
- [ ] 접근성(ARIA) 요구사항이 충족되었습니다
- [ ] 반응형 디자인이 포함되었습니다 (웹)
- [ ] 다크 모드가 지원됩니다 (웹)
- [ ] 단위 테스트를 작성했습니다
- [ ] PR 템플릿을 사용했습니다

---

## 예제

### 웹 컴포넌트: Card

```typescript
interface CardProps {
  title?: string
  description?: string
  variant?: 'default' | 'elevated'
  children: React.ReactNode
  className?: string
}

export const Card: React.FC<CardProps> = ({
  title,
  description,
  variant = 'default',
  children,
  className = '',
}) => {
  const variantStyles = {
    default: 'border border-border bg-background',
    elevated: 'shadow-lg bg-background',
  }

  return (
    <div
      className={`
        rounded-lg p-6
        ${variantStyles[variant]}
        ${className}
      `}
    >
      {title && <h3 className="text-xl font-bold mb-2">{title}</h3>}
      {description && <p className="text-muted-foreground mb-4">{description}</p>}
      {children}
    </div>
  )
}
```

### 네이티브 컴포넌트: NativeButton

```typescript
import { Button as GluestackButton, Text } from '@gluestack-ui/themed'

export const NativeButton: React.FC<NativeButtonProps> = ({
  variant = 'primary',
  children,
  ...props
}) => {
  const variantColors = {
    primary: '$primary',
    destructive: '$destructive',
  }

  return (
    <GluestackButton bg={variantColors[variant]} {...props}>
      <Text fontWeight="$semibold">{children}</Text>
    </GluestackButton>
  )
}
```

---

## 참고

- [컴포넌트 스펙](../spec/component-spec.md)
- [Emocog 테마](../manifests/theme.yaml)
- [PR 템플릿](../templates/pr-template.md)
- [Tailwind CSS 문서](https://tailwindcss.com)
- [Gluestack 문서](https://gluestack.io)
