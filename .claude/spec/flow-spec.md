# 서비스 플로우 컨벤션

## 개요

디자이너가 만든 컴포넌트를 조합하여 완전한 서비스 플로우를 설계하고 구현하는 가이드입니다.

---

## 플로우 구조

```
flow/{product-name}/
├── page.tsx              # 진입점 (또는 index.tsx)
├── layout.tsx            # 공통 레이아웃
├── contexts/
│   ├── FlowContext.tsx   # 글로벌 상태 (선택)
│   └── theme.ts          # 테마 설정
├── hooks/
│   ├── useNavigation.ts  # 화면 전환 로직
│   └── useFormState.ts   # 폼 상태 관리 (필요 시)
├── types/
│   └── index.ts          # 플로우 타입 정의
├── screens/
│   ├── Screen1.tsx
│   ├── Screen2.tsx
│   └── ...
├── components/
│   └── FlowStep.tsx      # 플로우 특화 컴포넌트 (필요 시)
└── README.md             # 플로우 설명
```

---

## 기본 구조

### 1. Root Layout

```typescript
// flow/{product-name}/layout.tsx
import React from 'react'

export const metadata = {
  title: '{Product Name}',
  description: 'Service flow for {product-name}',
}

interface LayoutProps {
  children: React.ReactNode
}

export default function Layout({ children }: LayoutProps) {
  return (
    <html lang="ko">
      <body className="bg-background text-foreground">
        {/* 네비게이션, 헤더 등 */}
        {children}
      </body>
    </html>
  )
}
```

### 2. Flow Context (선택)

```typescript
// flow/{product-name}/contexts/FlowContext.tsx
import React, { createContext, useContext, useState } from 'react'

interface FlowState {
  currentStep: number
  formData: Record<string, any>
  navigateTo: (step: number) => void
  updateFormData: (data: Partial<typeof formData>) => void
}

const FlowContext = createContext<FlowState | undefined>(undefined)

export const FlowProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [currentStep, setCurrentStep] = useState(0)
  const [formData, setFormData] = useState({})

  return (
    <FlowContext.Provider
      value={{
        currentStep,
        formData,
        navigateTo: setCurrentStep,
        updateFormData: (data) =>
          setFormData((prev) => ({ ...prev, ...data })),
      }}
    >
      {children}
    </FlowContext.Provider>
  )
}

export const useFlow = () => {
  const context = useContext(FlowContext)
  if (!context) {
    throw new Error('useFlow must be used within FlowProvider')
  }
  return context
}
```

### 3. Type Definitions

```typescript
// flow/{product-name}/types/index.ts
export interface User {
  id: string
  name: string
  email: string
}

export interface FlowStep {
  id: number
  title: string
  description: string
  component: React.ComponentType
}

export enum FlowStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  ERROR = 'error',
}
```

### 4. Main Page

```typescript
// flow/{product-name}/page.tsx
'use client'

import React, { useState } from 'react'
import { FlowProvider, useFlow } from './contexts/FlowContext'
import Screen1 from './screens/Screen1'
import Screen2 from './screens/Screen2'
import Screen3 from './screens/Screen3'

const screens = [
  { id: 0, component: Screen1, title: 'Step 1' },
  { id: 1, component: Screen2, title: 'Step 2' },
  { id: 2, component: Screen3, title: 'Step 3' },
]

export default function FlowPage() {
  return (
    <FlowProvider>
      <FlowContainer />
    </FlowProvider>
  )
}

function FlowContainer() {
  const { currentStep } = useFlow()
  const screenData = screens[currentStep]

  if (!screenData) {
    return <div>Flow completed!</div>
  }

  const CurrentScreen = screenData.component

  return (
    <div className="w-full h-screen flex flex-col">
      <header className="bg-primary text-primary-foreground py-4">
        <h1 className="text-2xl font-bold px-4">{screenData.title}</h1>
        <p className="text-sm px-4">Step {currentStep + 1} of {screens.length}</p>
      </header>
      <main className="flex-1 overflow-auto">
        <CurrentScreen />
      </main>
    </div>
  )
}
```

---

## 화면 설계 원칙

### 1. 단일 책임 원칙 (Single Responsibility)

각 화면은 하나의 작업에 집중합니다.

```typescript
// ✅ 좋음: 사용자 정보만 수집
// flow/{product-name}/screens/UserInfoScreen.tsx
export default function UserInfoScreen() {
  const { updateFormData } = useFlow()

  return (
    <form onSubmit={(e) => {
      e.preventDefault()
      // 데이터 저장
      updateFormData({ name, email })
    }}>
      {/* 폼 필드 */}
    </form>
  )
}

// ❌ 나쁨: 너무 많은 책임
export default function UserInfoScreen() {
  // 사용자 입력, 검증, API 호출, 결과 표시 모두 포함
}
```

### 2. 선형 네비게이션

기본적으로 이전/다음 버튼으로 진행됩니다.

```typescript
function ScreenFooter() {
  const { currentStep, navigateTo } = useFlow()
  const totalSteps = 5

  return (
    <div className="flex justify-between gap-4 p-4 bg-muted">
      <button
        onClick={() => navigateTo(currentStep - 1)}
        disabled={currentStep === 0}
      >
        이전
      </button>
      <span className="text-sm text-muted-foreground">
        {currentStep + 1} / {totalSteps}
      </span>
      <button
        onClick={() => navigateTo(currentStep + 1)}
        disabled={currentStep === totalSteps - 1}
      >
        다음
      </button>
    </div>
  )
}
```

### 3. 조건부 화면

필요 시 조건부 분기를 구현합니다.

```typescript
// flow/{product-name}/page.tsx
function getScreens(formData: any) {
  const baseScreens = [Screen1, Screen2]

  // 사용자가 "프리미엄"을 선택한 경우
  if (formData.planType === 'premium') {
    baseScreens.push(PremiumConfigScreen)
  }

  baseScreens.push(ConfirmationScreen)
  return baseScreens
}
```

---

## 데이터 플로우

### 1. 단방향 데이터 흐름 (Unidirectional)

```
User Input
    ↓
updateFormData()
    ↓
Context State
    ↓
Render UI
    ↓
User sees updates
```

### 2. API 호출 패턴

```typescript
// flow/{product-name}/screens/SubmitScreen.tsx
import { useEffect, useState } from 'react'
import { useFlow } from '../contexts/FlowContext'

export default function SubmitScreen() {
  const { formData } = useFlow()
  const [status, setStatus] = useState('idle')
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async () => {
    try {
      setStatus('loading')
      const response = await fetch('/api/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })

      if (!response.ok) {
        throw new Error('Submission failed')
      }

      setStatus('success')
    } catch (err) {
      setError(err.message)
      setStatus('error')
    }
  }

  return (
    <div>
      {status === 'loading' && <p>제출 중...</p>}
      {status === 'error' && <p className="text-destructive">{error}</p>}
      {status === 'success' && <p className="text-primary">완료!</p>}
      <button onClick={handleSubmit} disabled={status === 'loading'}>
        제출하기
      </button>
    </div>
  )
}
```

---

## 네비게이션 패턴

### 1. 선형 플로우 (Wizard)

```typescript
const steps = [
  { id: 0, name: 'Step 1', component: Step1 },
  { id: 1, name: 'Step 2', component: Step2 },
  { id: 2, name: 'Summary', component: Summary },
]

function navigateTo(step: number) {
  if (step >= 0 && step < steps.length) {
    setCurrentStep(step)
  }
}
```

### 2. 탭 네비게이션

```typescript
interface TabConfig {
  id: string
  label: string
  component: React.ComponentType
}

const tabs: TabConfig[] = [
  { id: 'info', label: '정보', component: InfoTab },
  { id: 'settings', label: '설정', component: SettingsTab },
  { id: 'preview', label: '미리보기', component: PreviewTab },
]

export default function TabbedFlow() {
  const [activeTab, setActiveTab] = useState('info')
  const activeTabData = tabs.find((t) => t.id === activeTab)!

  return (
    <div>
      <div className="flex gap-2 border-b">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`px-4 py-2 ${activeTab === tab.id ? 'border-b-2 border-primary' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <div className="p-4">
        <activeTabData.component />
      </div>
    </div>
  )
}
```

### 3. 모달 플로우

```typescript
interface ModalConfig {
  isOpen: boolean
  title: string
  content: React.ReactNode
  onClose: () => void
}

export default function ModalFlow() {
  const [modals, setModals] = useState<Record<string, ModalConfig>>({})

  const openModal = (id: string, config: ModalConfig) => {
    setModals((prev) => ({ ...prev, [id]: { ...config, isOpen: true } }))
  }

  const closeModal = (id: string) => {
    setModals((prev) => ({
      ...prev,
      [id]: { ...prev[id], isOpen: false },
    }))
  }

  return (
    <div>
      {/* UI */}
      {Object.entries(modals).map(([id, modal]) => (
        modal.isOpen && (
          <Dialog key={id} onClose={() => closeModal(id)}>
            <h2>{modal.title}</h2>
            {modal.content}
          </Dialog>
        )
      ))}
    </div>
  )
}
```

---

## 브라우저 내 데이터 저장

### 1. LocalStorage (간단한 데이터)

```typescript
const useLocalStorage = (key: string, initialValue: any) => {
  const [value, setValue] = useState(() => {
    try {
      const stored = localStorage.getItem(key)
      return stored ? JSON.parse(stored) : initialValue
    } catch {
      return initialValue
    }
  })

  const setStoredValue = (newValue: any) => {
    setValue(newValue)
    localStorage.setItem(key, JSON.stringify(newValue))
  }

  return [value, setStoredValue]
}
```

### 2. SessionStorage (한 세션 내)

```typescript
const [sessionData, setSessionData] = useSessionStorage('flowData', {})
```

---

## 에러 처리

```typescript
// flow/{product-name}/screens/ErrorBoundary.tsx
import React from 'react'

interface Props {
  children: React.ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends React.Component<Props, State> {
  state: State = { hasError: false, error: null }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error('Flow error:', error, info)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-4 bg-destructive text-destructive-foreground rounded-md">
          <h2 className="font-bold">오류가 발생했습니다</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => this.setState({ hasError: false })}>
            다시 시도
          </button>
        </div>
      )
    }

    return this.props.children
  }
}
```

---

## 테스트

```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import FlowPage from './page'

describe('Service Flow', () => {
  it('renders initial screen', () => {
    render(<FlowPage />)
    expect(screen.getByText(/Step 1/i)).toBeInTheDocument()
  })

  it('navigates to next screen', () => {
    render(<FlowPage />)
    fireEvent.click(screen.getByText('다음'))
    expect(screen.getByText(/Step 2/i)).toBeInTheDocument()
  })

  it('disables previous button on first screen', () => {
    render(<FlowPage />)
    expect(screen.getByText('이전')).toBeDisabled()
  })
})
```

---

## 체크리스트

- [ ] 플로우 구조 (screens/, contexts/ 등) 생성
- [ ] FlowProvider와 useFlow 구현
- [ ] 타입 정의 (types/index.ts)
- [ ] 각 화면 컴포넌트 생성
- [ ] 네비게이션 로직 구현
- [ ] 폼 데이터 검증
- [ ] API 호출 처리
- [ ] 에러 핸들링
- [ ] 반응형 디자인
- [ ] 접근성 (ARIA 라벨 등)
- [ ] README.md 작성
- [ ] 단위 테스트
- [ ] E2E 테스트 (선택)

---

## 참고

- [Next.js App Router](https://nextjs.org/docs/app)
- [React Context API](https://react.dev/reference/react/useContext)
- [Form Handling Best Practices](https://react.dev/reference/react-dom/components/form)
- [Component Spec](./component-spec.md)
