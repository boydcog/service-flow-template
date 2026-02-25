# /create-issue — 이슈 제보

## 개요

GitHub 이슈를 생성합니다. 버그 리포트, 기능 요청, 질문 등을 제출할 수 있습니다.

**기본 라벨**: bug, enhancement, documentation, question, duplicate, invalid, help wanted, wontfix

---

## Claude 실행 지시

이 명령을 실행할 때 Claude가 따라야 할 단계:

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

# 권한 검증: create-issue는 모든 역할 가능
echo "✅ 권한 확인 완료"
echo "역할: $USER_ROLE | 사용자: $USER_NAME"
echo ""
echo "이 세션에서는 /create-issue를 사용해서 이슈를 제보합니다."
```

### 2단계: 이슈 정보 수집 (AskUserQuestion)

#### 2-1. 이슈 유형 선택
```
이슈 유형을 선택하세요:
- Bug (bug) — 버그/결함
- Enhancement (enhancement) — 새로운 기능 또는 개선사항
- Documentation (documentation) — 문서 개선
- Question (question) — 질문 또는 명확화 필요
```

#### 2-2. 제목 입력 (필수)
```
이슈 제목을 입력하세요:
> Button 컴포넌트에서 hover 상태 스타일 미적용
```

#### 2-3. 상세 내용 입력 (필수)
```
상세 내용을 입력하세요:
> Button 컴포넌트에서 hover 상태 스타일이 적용되지 않습니다.
> 예상: 마우스 오버 시 배경색 변경
> 실제: 배경색이 변하지 않음
```

#### 2-4. 관련 파일/컴포넌트 (선택)
```
관련 파일을 입력하세요 (예: components/web/Button.tsx):
> components/web/Button.tsx
```

#### 2-5. 환경 정보 (선택, 버그인 경우 권장)
```
환경 정보 (OS, 브라우저, Node.js 버전 등):
> macOS, Chrome, Node.js 18
```

### 3단계: 사용자 확인 (AskUserQuestion)

이슈를 GitHub에 공유할까요?

```
이슈 공유 확인:

제목: Button 컴포넌트에서 hover 상태 스타일 미적용
라벨: bug
작성자: 홍길동 (designer)

공유하시겠습니까?
[Yes] GitHub Issue 생성
[No] 로컬에 저장
[Edit] 내용 수정
```

### 4단계: GitHub Issue 생성

#### 4-1. 토큰 확인
```bash
if [ ! -f .gh-token ]; then
 echo " GitHub 토큰을 찾을 수 없습니다"
 # Fallback: 로컬 저장
fi
```

#### 4-2. Issue 생성
```bash
gh issue create \
 --title "$TITLE" \
 --body "$BODY" \
 --label "$LABEL"
```

생성 시 포함 정보:
- 제목
- 상세 내용
- 관련 파일
- 환경 정보
- 작성자 정보
- 검증 여부 (해당하는 경우)

### 5단계: 완료 메시지

#### 성공
```
 GitHub Issue가 생성되었습니다!
 링크: https://github.com/{owner}/{repo}/issues/123

제목: Button 컴포넌트에서 hover 상태 스타일 미적용
라벨: bug
작성자: 홍길동 (designer)
```

#### Fallback (토큰 없음)
```
GitHub 토큰을 찾을 수 없어 로컬에 저장했습니다.

저장 위치: .state/pending-issues/20260225_button-hover-bug.md

나중에 gh auth login 후 다음 명령으로 동기화하세요:
/create-issue:sync-pending
```

---

## 사용 방법

### 1. 명령어 실행
```bash
/create-issue
```

### 2. 단계별 진행

```
1. 이슈 유형 선택
 ├─ Bug
 ├─ Enhancement
 ├─ Documentation
 └─ Question

2. 정보 입력
 ├─ 제목 (필수)
 ├─ 상세 내용 (필수)
 ├─ 관련 파일 (선택)
 └─ 환경 정보 (선택)

3. 공유 확인
 ├─ Yes: GitHub에 생성
 ├─ No: 로컬 저장
 └─ Edit: 내용 수정

4. 완료
 ├─ GitHub 링크 표시
 └─ 또는 로컬 저장 경로 표시
```

---

## 이슈 공유 플로우 (선택)

### 개발/검증 중 불만/피드백 감지

사용자가 불만이나 추가 요청을 표현하면:

```
Claude: 불만/피드백을 감지했습니다.

사용자 피드백: "Button의 색상이 Figma와 다르네요"

이를 이슈로 등록할까요?

[Yes - Bug] 버그로 등록
[Yes - Enhancement] 기능요청으로 등록
[No] 로컬에만 저장
[Edit] 내용 수정
```

결과:
- 선택 → Issue 생성 또는 로컬 저장
- 자동으로 불만 내용 → Issue 본문에 포함

---

## Issue 템플릿

생성된 이슈의 형식:

```markdown
## 설명

Button 컴포넌트에서 hover 상태 스타일이 적용되지 않습니다.

### 문제 상황
어떤 문제가 발생했는지

### 예상 동작
마우스 오버 시 배경색이 변경되어야 합니다.

### 실제 동작
배경색이 변하지 않습니다.

---

## 환경 정보

- OS: macOS
- 브라우저: Chrome
- Node.js: 18.x

---

## 관련 파일

- components/web/Button.tsx

---

## 작성자 정보

- 이름: 홍길동
- 역할: designer
- GitHub: @hong-gildong
- 작성 시간: 2026-02-25 10:30:00
```

---

## GitHub 기본 라벨

| 라벨 | 색상 | 사용 시기 |
|------|------|---------|
| `bug` | #d73a4a | 버그/결함 리포트 |
| `enhancement` | #a2eeef | 새로운 기능 또는 개선사항 |
| `documentation` | #0075ca | 문서 개선 |
| `question` | #d876e3 | 질문 또는 명확화 필요 |
| `duplicate` | #cfd3d7 | 중복 이슈 |
| `invalid` | #e4e669 | 유효하지 않은 요청 |
| `help wanted` | #008672 | 도움이 필요한 작업 |
| `wontfix` | #ffffff | 해결하지 않기로 결정 |

---

## 로컬 저장 구조

### Pending Issues (토큰 없을 때)

```bash
.state/pending-issues/
├── 20260225_button-hover-bug.md
├── 20260225_color-mismatch.md
└── 20260225_size-needed.md
```

**파일 형식**:
```markdown
# Button 컴포넌트에서 hover 상태 스타일 미적용

**Type**: bug
**Created**: 2026-02-25 10:30:00
**Author**: 홍길동
**Role**: designer

## Content

Button 컴포넌트에서 hover 상태 스타일이 적용되지 않습니다.

...
```

### 동기화

```bash
# 모든 pending issues 동기화
/create-issue:sync-pending

# 결과
 5개 이슈가 GitHub에 생성되었습니다.
 링크:
 - https://github.com/.../issues/123
 - https://github.com/.../issues/124
 ...
```

---

## 주의사항

### 피해야 할 것
- 민감한 정보 (비밀번호, API 키) 공유
- 관계없는 이슈 혼합 (하나의 이슈 = 하나의 문제)
- 무례하거나 공격적인 언어 사용

### 권장 사항
- 명확하고 구체적인 제목 사용
- 재현 가능한 단계 제시 (버그인 경우)
- 스크린샷이나 비디오 첨부
- 환경 정보 포함 (OS, 브라우저, Node.js 버전 등)

---

## 예제

### 버그 리포트

```
제목: Input 컴포넌트에서 maxLength 제한이 작동하지 않음
유형: bug

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
유형: enhancement

상세:
현재 모든 텍스트가 한국어로 고정되어 있습니다.
영어, 일본어, 중국어 지원을 추가해주세요.

제안:
- i18n 라이브러리 도입 (next-i18next 등)
- 언어 선택 UI 추가
- 각 언어별 번역 파일 관리
```

### 질문

```
제목: Button 컴포넌트의 disabled 상태는 어떻게 구현하나요?
유형: question

상세:
Button 컴포넌트에서 disabled 상태를 사용하려면
어떻게 해야 하나요?

관련 파일:
- components/web/Button.tsx
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

- [GitHub Issue 생성](https://cli.github.com/manual/gh_issue_create)
- [검증 및 공유 플로우](../spec/validation-flow.md)
- [Issue 템플릿](../templates/issue-template.md)
- [Roles 정의](../manifests/roles.yaml)
