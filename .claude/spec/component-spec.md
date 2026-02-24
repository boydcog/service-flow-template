# 컴포넌트 생성 규칙

## 개요

Emocog 테마를 기반으로 재사용 가능한 컴포넌트를 만드는 가이드입니다.

---

## 컴포넌트 명명 규칙

- **PascalCase**: `Button`, `CardHeader`, `FormInput`
- **접두사 없음**: 충분히 명확한 이름 사용
- **파일명**: `Button.tsx` (컴포넌트명과 동일)

---

## 웹 컴포넌트 (React + TypeScript + Tailwind)

### 파일 위치
```
components/web/{ComponentName}.tsx
```

### 기본 구조

```typescript
import React from 'react'

interface {ComponentName}Props {
  // Props 정의
  children?: React.ReactNode
  className?: string
  [key: string]: any
}

/**
 * {ComponentName}
 *
 * {짧은 설명}
 *
 * @example
 * <{ComponentName} prop1="value">Content</{ComponentName}>
 */
export const {ComponentName}: React.FC<{ComponentName}Props> = ({
  children,
  className = '',
  ...props
}) => {
  return (
    <div className={`emocog-component ${className}`} {...props}>
      {children}
    </div>
  )
}
```

### Emocog 테마 사용

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

#### 반응형 설정
```typescript
<div className="
  px-4 sm:px-6 md:px-8 lg:px-10
  text-sm md:text-base lg:text-lg
">
  반응형 컴포넌트
</div>
```

#### 다크 모드
```typescript
<div className="
  bg-white dark:bg-slate-950
  text-gray-900 dark:text-white
">
  다크 모드 지원
</div>
```

### 예제: Button 컴포넌트

```typescript
import React from 'react'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'destructive' | 'muted'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
  children: React.ReactNode
}

const variantStyles = {
  primary: 'bg-primary text-primary-foreground hover:opacity-90',
  secondary: 'bg-secondary text-secondary-foreground hover:opacity-90',
  destructive: 'bg-destructive text-destructive-foreground hover:opacity-90',
  muted: 'bg-muted text-muted-foreground hover:opacity-80',
}

const sizeStyles = {
  sm: 'px-3 py-1 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-6 py-3 text-lg',
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  children,
  className = '',
  disabled,
  ...props
}) => {
  return (
    <button
      className={`
        rounded-md font-medium transition-all duration-200
        disabled:opacity-50 disabled:cursor-not-allowed
        ${variantStyles[variant]}
        ${sizeStyles[size]}
        ${className}
      `}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? '로딩 중...' : children}
    </button>
  )
}
```

---

## 네이티브 컴포넌트 (React Native + Gluestack)

### 파일 위치
```
components/native/{ComponentName}.tsx
```

### 기본 구조

```typescript
import React from 'react'
import { styled } from '@gluestack-ui/styled-components'
import { Text, View } from 'react-native'

interface {ComponentName}Props {
  // Props 정의
  children?: React.ReactNode
  [key: string]: any
}

/**
 * {ComponentName}
 *
 * {짧은 설명}
 */
export const {ComponentName}: React.FC<{ComponentName}Props> = ({
  children,
  ...props
}) => {
  return (
    <View sx={{ /* gluestack styles */ }}>
      {children}
    </View>
  )
}
```

### Gluestack 테마 사용

```typescript
import { Button, Text, VStack } from '@gluestack-ui/themed'

export const NativeButton = () => {
  return (
    <VStack space="md">
      <Button bg="$primary" action="primary">
        <Text>Primary</Text>
      </Button>
      <Button bg="$destructive" action="negative">
        <Text>Destructive</Text>
      </Button>
    </VStack>
  )
}
```

---

## Props 정의

### 필수 Props vs 선택 Props

```typescript
interface ComponentProps {
  // 필수
  id: string
  title: string

  // 선택 (기본값)
  variant?: 'primary' | 'secondary'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean

  // 이벤트 핸들러
  onClick?: (event: React.MouseEvent) => void
  onChange?: (value: any) => void

  // 스타일
  className?: string
  style?: React.CSSProperties
}
```

---

## 스타일 가이드

### Tailwind CSS (웹)

**권장**: 인라인 클래스 사용
```typescript
<div className="flex items-center justify-between gap-4 px-4 py-2">
  {/* ... */}
</div>
```

**피할 것**: 하드코딩 된 색상
```typescript
// ❌ 나쁨
<div style={{ color: '#2b65ff' }}>Bad</div>

// ✅ 좋음
<div className="text-primary">Good</div>
```

### CSS 변수 (폴백)

```css
/* components/theme/tokens.css */
:root {
  --emocog-primary: oklch(0.488 0.243 264.376);
  --emocog-primary-foreground: oklch(0.985 0.001 106.423);
}

@media (prefers-color-scheme: dark) {
  :root {
    --emocog-primary: #2b65ff;
    --emocog-primary-foreground: #ffffff;
  }
}
```

---

## 문서화

### JSDoc 주석

```typescript
/**
 * 버튼 컴포넌트
 *
 * Emocog 테마 기반 재사용 가능한 버튼입니다.
 *
 * @param {ButtonProps} props - 버튼 프로퍼티
 * @param {'primary' | 'secondary' | 'destructive'} props.variant - 버튼 스타일 변형
 * @param {'sm' | 'md' | 'lg'} props.size - 버튼 크기
 * @param {boolean} props.disabled - 비활성화 여부
 * @param {React.ReactNode} props.children - 버튼 내용
 *
 * @example
 * <Button variant="primary" size="md">
 *   클릭하세요
 * </Button>
 *
 * @example
 * <Button variant="destructive" disabled>
 *   삭제 (비활성화)
 * </Button>
 */
```

---

## 접근성 (A11y)

### ARIA 속성

```typescript
<button
  type="button"
  aria-label="메뉴 열기"
  aria-expanded={isOpen}
  aria-controls="menu-list"
>
  <Menu size={24} />
</button>
```

### 키보드 네비게이션

```typescript
const [focusedIndex, setFocusedIndex] = React.useState(0)

const handleKeyDown = (e: React.KeyboardEvent) => {
  if (e.key === 'ArrowDown') {
    setFocusedIndex((prev) => (prev + 1) % items.length)
  } else if (e.key === 'ArrowUp') {
    setFocusedIndex((prev) => (prev - 1 + items.length) % items.length)
  }
}
```

### 색상 대비

- **최소 4.5:1** (일반 텍스트)
- **최소 3:1** (큰 텍스트, UI 컴포넌트)

Emocog 테마는 WCAG 2.1 AA 이상 준수합니다.

---

## 테스트

### 웹 컴포넌트 테스트 예제

```typescript
import { render, screen } from '@testing-library/react'
import { Button } from './Button'

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('handles click events', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click</Button>)
    screen.getByText('Click').click()
    expect(handleClick).toHaveBeenCalled()
  })

  it('applies variant styles', () => {
    const { container } = render(<Button variant="destructive">Delete</Button>)
    expect(container.querySelector('button')).toHaveClass('bg-destructive')
  })
})
```

---

## 체크리스트

- [ ] 컴포넌트 명명 규칙 준수 (PascalCase)
- [ ] Props TypeScript 인터페이스 정의
- [ ] Emocog 테마 색상 사용
- [ ] 다크 모드 지원 (웹)
- [ ] 반응형 디자인 (웹)
- [ ] JSDoc 주석 작성
- [ ] ARIA 라벨 추가 (필요 시)
- [ ] 단위 테스트 작성
- [ ] 스토리북 스토리 추가 (선택)
- [ ] PR 생성

---

## 참고

- [Tailwind CSS 문서](https://tailwindcss.com)
- [React TypeScript 가이드](https://react-typescript-cheatsheet.netlify.app)
- [Gluestack 문서](https://gluestack.io)
- [WCAG 2.1 가이드](https://www.w3.org/WAI/WCAG21/quickref/)
- [Emocog 테마](../manifests/theme.yaml)
