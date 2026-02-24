# /create-issue — 이슈 제보

## 개요

GitHub 이슈를 생성합니다. 버그 리포트, 기능 요청, 피드백 등을 제출할 수 있습니다.

---

## Claude 실행 지시

이 명령을 실행할 때 Claude가 따라야 할 단계:

1. 선행 조건 확인:
   - `.user-identity` 파일 존재 여부 확인
   - 없으면 Skill("setup") 먼저 실행

2. 이슈 정보 수집 (AskUserQuestion):
   - 이슈 유형: bug / enhancement / feedback / other
   - 제목 (필수)
   - 상세 내용 (필수)
   - 관련 파일/컴포넌트 (선택)
   - 환경 정보 (선택)

3. 자동 라벨 추가:
   - 키워드 매핑 (하단의 "자동 라벨 매핑" 테이블 참조)
   - 제목과 내용에서 키워드 추출 → 라벨 할당

4. GitHub 이슈 생성:
   - `.gh-token` 파일 확인
   - GH_TOKEN 환경변수 설정
   - `gh issue create` 명령어 실행 (제목, 본문, 라벨 포함)

5. 토큰 없을 때 Fallback:
   - `.state/pending-issues/` 디렉토리 생성
   - 이슈 정보를 마크다운 파일로 저장
   - `{YYYYMMDD}_{issue-slug}.md` 형식
   - 사용자에게 "나중에 `gh auth login` 후 동기화 가능" 안내

6. 완료 메시지:
   - 성공: GitHub 이슈 링크 표시
   - 실패/Fallback: 저장 경로 표시

---

## 사용 방법

```bash
/create-issue
```

---

## 단계별 진행

### 1단계: 신원 확인

```
✅ 신원 로드됨: 홍길동 (designer)
```

### 2단계: 이슈 유형 선택

```
📌 이슈 유형을 선택하세요:
  1. 🐛 버그 (Bug) — 버그 리포트
  2. ✨ 기능 (Enhancement) — 기능 요청
  3. 💬 피드백 (Feedback) — 의견 및 제안
  4. ❓ 기타 (Other) — 기타 사항

선택:
> 1
```

### 3단계: 제목 입력

```
📝 이슈 제목을 입력하세요:
> Button 컴포넌트에서 hover 상태 스타일 미적용
```

### 4단계: 상세 내용 입력

```
📄 상세 내용을 입력하세요 (여러 줄 가능, Ctrl+D로 종료):
> Button 컴포넌트에서 hover 상태 스타일이 적용되지 않습니다.
> 예상: 마우스 오버 시 배경색 변경
> 실제: 배경색이 변하지 않음
> 환경: macOS, Chrome, Node.js 18
```

### 5단계: 관련 파일/컴포넌트 입력 (선택)

```
📁 관련 파일을 입력하세요 (예: components/web/Button.tsx):
> components/web/Button.tsx
```

### 6단계: 라벨 자동 추가

```
🏷️  자동으로 라벨이 추가됩니다:
  - bug
  - component
  - web
  - design-system
```

### 7단계: 이슈 생성 확인

```
✅ GitHub 이슈가 생성되었습니다!
🔗 링크: https://github.com/{owner}/{repo}/issues/123

제목: Button 컴포넌트에서 hover 상태 스타일 미적용
작성자: 홍길동 (designer)
```

---

## 이슈 템플릿

생성된 이슈의 형식:

```markdown
## 📝 이슈 제목

---

## 📝 설명

<!-- 이슈에 대한 자세한 설명 -->

### 문제 상황 (버그인 경우)
<!-- 어떤 문제가 발생했는지 -->

### 예상 동작
<!-- 원래 어떻게 작동해야 하는지 -->

### 실제 동작
<!-- 실제로는 어떻게 작동하는지 -->

---

## 🔧 환경 정보

- OS: macOS
- 브라우저: Chrome
- Node.js: 18.x

---

## 📌 관련 파일

- components/web/Button.tsx

---

## 작성자 정보

- **이름**: 홍길동
- **역할**: designer
- **GitHub**: @hong-gildong
- **작성 시간**: 2024-02-24 10:30:00
```

---

## 자동 라벨 매핑

키워드에 따라 자동으로 라벨이 추가됩니다:

| 키워드 | 라벨 |
|--------|------|
| `button`, `card`, `form`, 등 | `component` |
| `web`, `next.js`, `react` | `web` |
| `native`, `react native`, `gluestack` | `native` |
| `theme`, `color`, `emocog` | `design-system` |
| `flow`, `screen`, `navigation` | `feature` |
| `bug`, `error`, `crash` | `bug` |
| `enhancement`, `improve`, `add` | `enhancement` |
| `docs`, `readme`, `guide` | `documentation` |
| `performance`, `optimize`, `speed` | `performance` |
| `access`, `a11y`, `aria`, `wcag` | `accessibility` |

**예제**:
```
제목: Button 컴포넌트의 hover 상태 버그
→ 자동 라벨: bug, component, web, design-system

제목: 다크 모드 지원 추가
→ 자동 라벨: enhancement, web, design-system
```

---

## GitHub 토큰 없을 때

GH_TOKEN이 없거나 유효하지 않으면 이슈가 로컬에 저장됩니다:

```bash
.state/pending-issues/
├── 20240224_button-hover-bug.md
└── 20240224_dark-mode-request.md
```

나중에 토큰이 설정되면:

```bash
/create-issue:sync-pending
```

로컬 이슈를 GitHub에 동기화할 수 있습니다.

---

## 주의사항

### ❌ 피해야 할 것

- 민감한 정보 (비밀번호, API 키) 공유
- 관계없는 이슈 혼합 (하나의 이슈 = 하나의 문제)
- 무례하거나 공격적인 언어 사용

### ✅권장 사항

- 명확하고 구체적인 제목 사용
- 재현 가능한 단계 제시 (버그인 경우)
- 스크린샷이나 비디오 첨부
- 환경 정보 포함 (OS, 브라우저, Node.js 버전 등)

---

## 예제

### 버그 리포트

```
제목: Input 컴포넌트에서 maxLength 제한이 작동하지 않음

상세:
Input 컴포넌트에 maxLength={10}을 설정했는데도
10자를 초과하여 입력할 수 있습니다.

환경:
- OS: macOS
- 브라우저: Safari
- 컴포넌트: components/web/Input.tsx
```

### 기능 요청

```
제목: 다국어 지원 추가

상세:
현재 모든 텍스트가 한국어로 고정되어 있습니다.
영어, 일본어, 중국어 지원을 추가해주세요.

제안:
- i18n 라이브러리 도입 (next-i18next 등)
- 언어 선택 UI 추가
- 각 언어별 번역 파일 관리
```

### 피드백

```
제목: 버튼 컴포넌트의 border-radius가 Emocog 테마와 맞지 않음

상세:
Button 컴포넌트의 border-radius가 Emocog 테마의 md 값과 다릅니다.
테마 정의: 1.3rem
현재 구현: 0.5rem

제안:
theme.yaml의 값으로 통일하면 일관성이 개선될 것 같습니다.
```

---

## 다음 단계

이슈 생성 후:

1. **리뷰 대기**: admin/developer가 이슈를 검토합니다
2. **담당자 할당**: 필요 시 담당자가 할당됩니다
3. **작업 시작**: 할당된 사람이 문제를 해결합니다
4. **PR 생성**: 수정 사항을 PR로 제출합니다
5. **병합**: 리뷰 후 main 브랜치에 병합됩니다

---

## 참고

- [이슈 템플릿](../templates/issue-template.md)
- [GitHub CLI 이슈 생성](https://cli.github.com/manual/gh_issue_create)
- [Roles 정의](../manifests/roles.yaml)
