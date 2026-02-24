# /designer -- 컴포넌트 제작/수정/확장

## 개요

Emocog 테마를 기반으로 재사용 가능한 컴포넌트를 만들거나, 기존 컴포넌트를 수정/확장합니다.

**권한**: designer 이상 (admin, developer, designer)

---

## Claude 실행 지시

이 명령을 실행할 때 Claude가 따라야 할 단계:

1. 선행 조건 확인:
   - `.user-identity` 파일 존재 여부 확인
   - 없으면 Skill("setup") 먼저 실행
   - 존재하면 role 읽고 권한 검증 (role이 admin/developer/designer만 가능)
   - 권한 없으면: "역할 {role}은 /designer를 사용할 수 없습니다" -> 중단

2. 프레임워크 선택 (AskUserQuestion):
   - Web (Next.js, Vite + React, Remix)
   - Native (React Native + Gluestack)

3. 컴포넌트 탐색 및 목록 표시:
   - `scan_existing_components(framework)` 호출
   - 현재 등록된 컴포넌트 수와 목록 출력
   - 각 컴포넌트의 스토리 파일 존재 여부 표시

4. 3-way 액션 선택 (AskUserQuestion):
   - 1. 새 컴포넌트 생성 (create)
   - 2. 기존 컴포넌트 확장 (extend) -- 스토리/변형 추가
   - 3. 기존 컴포넌트 수정 (modify) -- 코드 직접 수정

5. 액션별 처리:

   **create (새 컴포넌트 생성)**:
   - 이름 입력 시 덮어쓰기 방지 검사 (동일 이름 파일 존재 확인)
   - 존재하면 경고 후 사용자 확인 요청 (y/n)
   - n 선택 시 "확장" 또는 "수정" 안내 후 중단
   - 컴포넌트 정보 수집 (이름, 설명, 유형)
   - 코드 생성 (`.claude/spec/component-spec.md` 참조)

   **extend (기존 컴포넌트 확장)**:
   - `find_similar_components(query)` 로 부분 일치 검색
   - `show_component_api(path)` 로 Props 인터페이스만 표시
   - 확장 옵션 선택: 스토리 추가 / 변형 추가
   - 스토리 추가 시 export 이름 충돌 검사

   **modify (기존 컴포넌트 수정)**:
   - `find_similar_components(query)` 로 컴포넌트 검색
   - `read_component_content(path)` 로 전체 코드 표시
   - `write_component_content(path, new, original)` 로 diff 확인 후 저장
   - 사용자가 n 선택 시 원본 유지

6. 검증 (verify_designer):
   - `verify_designer.run_all(component_name)` 실행
   - 검증 항목: 컴포넌트 파일, 스토리 파일, Default 스토리, Props 정의, any 타입 금지
   - 실패 시 최대 3회 재시도
   - 재시도 실패 시 PR 생성 불가

7. Storybook 실행:
   - 포트 6006 정리 및 재시작
   - 브라우저 자동 띄우기

8. PR 생성:
   - 검증 통과 + 사용자 확인 후에만 가능

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
1. 사용자 입력
   +-- 프레임워크 선택 (Web/Native)
   +-- 컴포넌트 목록 표시 (scan_existing_components)
   +-- 3-way 액션 선택 (생성/확장/수정)

2. 액션 처리
   +-- [생성] 덮어쓰기 방지 -> 코드/스토리 생성
   +-- [확장] 검색(find_similar_components) -> API 확인 -> 스토리/변형 추가
   +-- [수정] 검색 -> 코드 표시 -> diff 확인 후 저장

3. 검증 (Strict Mode)
   +-- verify_designer.run_all() 실행
   +-- 컴포넌트/스토리/Default/Props/any 타입 검사
   +-- 실패 시 최대 3회 재시도

4. Storybook 실행
   +-- 포트 6006 정리
   +-- npm run storybook
   +-- 브라우저 자동 띄우기 (localhost:6006)

5. 사용자 검증
   +-- Storybook에서 컴포넌트 상호작용 확인
   +-- Props, 다크 모드, 반응형 등 검증

6. PR 생성
   +-- git checkout -b component/{name}
   +-- git add/commit/push
   +-- gh pr create로 자동 PR 생성
```

---

## 컴포넌트 탐색 절차

### scan_existing_components(framework)

`components/{framework}/ui/*.tsx` 전체를 스캔하여 컴포넌트 목록 반환:

```
[INFO] 현재 WEB 컴포넌트: 25개

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

### find_similar_components(query, framework)

부분 일치 검색 (case-insensitive, 하이픈/언더스코어 무시):

| 검색어 | 결과 |
|--------|------|
| "btn" | button |
| "card" | card, stat-card, pricing-card |
| "input" | input |
| "tab" | table, tabs |
| "select" | select |

### show_component_api(path)

전체 코드 대신 Props interface만 추출:

```
--- Props Interface ---
export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

--- Exports ---
export { Button, buttonVariants }
```

---

## 덮어쓰기 방지 절차

새 컴포넌트 생성 시 동일 이름 파일이 이미 존재하면:

```
[WARNING] 'button.tsx' 파일이 이미 존재합니다: components/web/ui/button.tsx
기존 컴포넌트를 덮어쓰면 코드가 손실됩니다.
덮어쓰시겠습니까? (y/n):
> n

[CANCEL] 생성이 취소되었습니다.
[TIP] '기존 컴포넌트 확장' 또는 '기존 컴포넌트 수정'을 사용해보세요.
```

---

## 단계별 진행

### 1단계: 신원 및 권한 확인

```
[OK] 신원: 홍길동 (designer)
[OK] 권한: 컴포넌트 작업 가능
```

**권한 없음 시**:
```
[ERROR] pm은 /designer 명령어를 사용할 수 없습니다.
필요 역할: designer 이상 (admin, developer, designer)
```

### 2단계: 프레임워크 선택

```
프레임워크를 선택하세요:
  1. Web (Next.js, Vite + React, Remix)
  2. Native (React Native + Gluestack)

선택:
> 1
```

### 3단계: 3-way 액션 선택

```
[INFO] 현재 WEB 컴포넌트: 25개

액션을 선택하세요:
  1. 새 컴포넌트 생성
  2. 기존 컴포넌트 확장 (스토리/변형 추가)
  3. 기존 컴포넌트 수정 (코드 변경)

선택 (1/2/3):
> 2
```

---

## 액션 1: 새 컴포넌트 생성

### 진행 과정

```
컴포넌트 정보 입력
========================================

컴포넌트 이름 (예: button, stat-card): dropdown-menu
설명 (예: 클릭 가능한 버튼): 드롭다운 메뉴 컴포넌트

컴포넌트 유형:
  a) Basic (단순)
  b) Form (폼)
  c) Container (레이아웃)
선택 (a/b/c): a

[OK] 컴포넌트 생성됨!
  컴포넌트: components/web/ui/dropdown-menu.tsx
  스토리: components/web/ui/dropdown-menu.stories.tsx
```

---

## 액션 2: 기존 컴포넌트 확장

### 스토리 추가

```
컴포넌트 이름 또는 검색어 입력: btn

[FOUND] button (components/web/ui/button.tsx)
--- Props Interface ---
export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

'button' 컴포넌트를 선택하시겠습니까? (y/n): y

'button' 확장 옵션:
  1. 새 스토리(Story) 추가
  2. 새 변형(Variant) 추가 (컴포넌트 코드 + 스토리)

선택 (1/2): 1

새 스토리 이름 (예: WithIcon, Loading): Loading
스토리 설명 (선택): 로딩 상태의 버튼
args (JSON, 예: {"children": "텍스트"}): {"children": "Loading...", "disabled": true}

--- 추가될 스토리 ---
/**
 * 로딩 상태의 버튼
 */
export const Loading: Story = {
  args: {
    children: 'Loading...',
    disabled: true,
  },
}
--- end ---

스토리를 추가하시겠습니까? (y/n): y
[OK] 스토리 추가됨: components/web/ui/button.stories.tsx
```

---

## 액션 3: 기존 컴포넌트 수정

### 진행 과정

```
컴포넌트 이름 또는 검색어 입력: card

[FOUND] 3개의 일치 항목:
  1. card [story]
  2. pricing-card [story]
  3. stat-card [story]

번호 선택 (1-3): 1

[SELECTED] card
--- Props Interface ---
(card.tsx에서 추출된 Props)

--- 현재 코드 (card.tsx) ---
// 전체 코드 표시
--- end ---

[INFO] 수정할 내용을 설명해주세요.
수정 사항: CardHeader의 패딩을 p-4로 변경

--- 변경 사항 ---
  - className={cn("flex flex-col space-y-1.5 p-6", className)}
  + className={cn("flex flex-col space-y-1.5 p-4", className)}
--- end diff ---

변경 사항을 저장하시겠습니까? (y/n):
> y
[OK] 저장됨: components/web/ui/card.tsx
```

---

## 검증 (Strict Mode)

모든 액션 완료 후 `verify_designer.run_all()` 자동 실행:

```
================================================
  검증 시작 (Strict Mode)
================================================

  [PASS]  컴포넌트 파일: components/web/ui/button.tsx
  [PASS]  스토리 파일: components/web/ui/button.stories.tsx
  [PASS]  Default 스토리: export const Default 확인됨
  [PASS]  Props 정의: interface ButtonProps
  [PASS]  any 타입 금지: any 타입 사용 없음
  [PASS]  Storybook 실행: Storybook 실행 중 (포트 6006)

================================================
  검증 완료 (Strict Mode 통과)
================================================

  모든 검증 항목 통과. PR 생성 가능합니다.
```

검증 실패 시:
```
  [FAIL]  Props 정의: Props interface 없음

================================================
  검증 실패 (Strict Mode)
================================================

  재시도 기회: 2회 남음
  파일을 수정한 후 Enter를 눌러 재검증하세요.
  (취소: q 입력)
```

---

## PR 생성

검증 통과 + 사용자 Storybook 확인 후:

```
PR 생성 중...

[OK] PR이 생성되었습니다!
  PR 링크: https://github.com/{owner}/{repo}/pull/123
```

PR 제목 형식:
```
[designer] {사용자명}: {컴포넌트명} 컴포넌트
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
// 좋음
className="bg-primary text-primary-foreground dark:bg-primary"

// 나쁨
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

### 피해야 할 것

- 커스텀 색상 사용 (Emocog 테마 벗어남)
- ARIA 라벨 누락
- 하드코딩된 값 (CSS 변수 미사용)
- 테스트 없이 제출
- 기존 컴포넌트 무단 덮어쓰기

### 권장 사항

- 템플릿에 따라 구현
- 모든 Props TypeScript 타입 정의
- JSDoc 주석 작성
- 단위 테스트 포함
- 스토리북 스토리 추가 (필수)
- 수정 전 반드시 검색으로 기존 컴포넌트 확인

---

## 체크리스트

완성 전 확인:

- [ ] 컴포넌트가 Emocog 테마를 사용합니다
- [ ] TypeScript 타입 정의가 완전합니다
- [ ] JSDoc 주석이 작성되었습니다
- [ ] 접근성(ARIA) 요구사항이 충족되었습니다
- [ ] 반응형 디자인이 포함되었습니다 (웹)
- [ ] 다크 모드가 지원됩니다 (웹)
- [ ] Storybook 스토리가 포함되었습니다
- [ ] Default 스토리가 존재합니다
- [ ] any 타입이 사용되지 않았습니다
- [ ] verify_designer 검증을 통과했습니다
- [ ] PR 템플릿을 사용했습니다

---

## 스크립트 API 참조

### scan_existing_components(framework: str) -> List[Dict]

components/{framework}/ui/*.tsx 전체 스캔. stories 파일 제외.

반환: `[{"name": "button", "path": Path, "has_story": True}, ...]`

### find_similar_components(query: str, framework: str) -> List[Dict]

부분 일치 검색 (case-insensitive, 하이픈/언더스코어 무시).

### show_component_api(component_path: Path) -> str

Props interface만 추출하여 반환 (전체 코드 대신).

### read_component_content(path: Path) -> str

파일 전체 내용 반환.

### write_component_content(path: Path, new: str, original: str) -> bool

diff 출력 후 사용자 확인을 거쳐 저장. n 선택 시 원본 유지.

### extend_component_stories(story_path: Path, new_story: str) -> bool

stories 파일 끝에 새 Story 추가. export 이름 충돌 검사 포함.

### verify_component_quality(name: str, framework: str) -> Dict

간이 검증. 반환: `{"passed": bool, "checks": [...]}`

---

## 참고

- [컴포넌트 스펙](../spec/component-spec.md)
- [Emocog 테마](../manifests/theme.yaml)
- [PR 템플릿](../templates/pr-template.md)
- [Tailwind CSS 문서](https://tailwindcss.com)
- [Gluestack 문서](https://gluestack.io)
