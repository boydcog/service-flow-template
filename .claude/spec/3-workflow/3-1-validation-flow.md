# 검증 및 공유 플로우 가이드

## 개요

모든 개발 산출물(컴포넌트, 플로우)은 사용자 검증 → 공유 확인 → PR 생성의 3단계 프로세스를 거칩니다.

---

## 1. 기본 라벨 정책

**GitHub 기본 라벨만 사용** (자동 매핑 제거):

| 라벨 | 사용 시기 |
|------|---------|
| `bug` | 버그/결함 리포트 |
| `enhancement` | 새로운 기능 또는 개선사항 |
| `documentation` | 문서 개선 |
| `question` | 질문 또는 명확화 필요 |
| `duplicate` | 중복 이슈 |
| `invalid` | 유효하지 않은 요청 |
| `help wanted` | 도움이 필요한 작업 |
| `wontfix` | 해결하지 않기로 결정 |

**적용 규칙**:
- 사용자가 이슈/PR 유형을 선택 → 해당 라벨 자동 할당
- 추가 라벨은 GitHub에서 수동 할당

---

## 2. 기능 개발 후 검증 플로우

### 단계 1: 개발 완료
```
Claude: 컴포넌트/플로우 개발 완료
├── 코드 생성
├── 테스트 작성
├── Storybook (Web만)
└── Strict Mode 검증 통과
```

### 단계 2: 사용자 검증 요청
```
Claude가 사용자에게 물어보기:

┌─────────────────────────────────┐
│ 개발이 완료되었습니다. │
│ │
│ 이제 검증 단계입니다. │
│ │
│ 1. Storybook에서 렌더링 확인 │
│ (예: http://localhost:6006) │
│ │
│ 2. 다음을 확인해주세요: │
│ - 시각적 일치성 │
│ - 기능 정상 동작 │
│ - 접근성 (키보드 탭) │
│ - 반응형 (모바일/데스크톱) │
│ │
│ 검증이 완료되셨나요? │
│ [O] 완료 - 모두 정상 │
│ [X] 미완료 - 수정 필요 │
│ [?] 질문 있음 │
└─────────────────────────────────┘
```

### 단계 3: 검증 결과 처리

#### 3-1. 검증 완료 
```
Claude: 검증 감사합니다!

다음 단계: 개발자에게 공유

PR을 생성하여 개발자에게 공유할까요?
[Yes] PR 생성 → 개발자 리뷰 대기
[No] 로컬 브랜치에 저장만 (나중에 공유)
[Edit] 수정 후 재검증
```

#### 3-2. 미완료 (수정 필요)
```
Claude: 어떤 부분을 수정할까요?

사용자 입력: "Button의 hover 상태가 안보임"

Claude:
1. 문제 분석
2. 수정 사항 반영
3. Storybook 재시작
4. 재검증 요청
```

#### 3-3. 질문
```
Claude: 어떤 부분이 궁금하신가요?

사용자가 설명 → Claude가 답변 → 재검증 요청
```

---

## 3. PR 생성 전 공유 확인

### 플로우
```
Claude:

┌──────────────────────────────────┐
│ 개발자 공유 확인 │
│ │
│ 다음 PR을 생성할 준비가 │
│ 되었습니다: │
│ │
│ 제목: │
│ [designer] 박나현: Button │
│ │
│ 담당: 개발자 리뷰 (main 브랜치) │
│ │
│ 공유하시겠습니까? │
│ [Yes] PR 생성 & 알림 │
│ [No] 로컬에만 보관 │
│ [Edit] PR 제목/설명 수정 │
└──────────────────────────────────┘
```

### PR 생성 시 정보
```
PR 제목: [designer] 박나현: Button 컴포넌트
PR 본문:
- 변경사항
- 테스트 결과
- 검증 완료 여부
- 검증자: 사용자명
- 검증 일시: YYYY-MM-DD HH:MM:SS
```

---

## 4. 이슈 공유 플로우

### 단계 1: 사용자 불만/피드백 감지
```
개발 중 또는 완료 후:

Claude: 혹시 불만이나 추가 요청이 있으신가요?

사용자: "Button의 색상이 Figma와 다르네요"
사용자: "미디엄 사이즈가 필요해요"
사용자: "버그: 클릭 안됨"
```

### 단계 2: 이슈로 공유할지 확인
```
Claude가 사용자 피드백을 감지하면:

┌──────────────────────────────────┐
│ 이슈로 등록하시겠습니까? │
│ │
│ 제목: │
│ "Button 컴포넌트: 색상 불일치" │
│ │
│ 유형: │
│ [O] enhancement — 개선요청 │
│ [ ] bug — 버그 │
│ [ ] question — 질문 │
│ │
│ 등록하시겠습니까? │
│ [Yes] GitHub Issue 생성 │
│ [No] 로컬에 저장 │
│ [Edit] 내용 수정 │
└──────────────────────────────────┘
```

### 단계 3: Issue 생성
```
생성된 Issue:
- 제목: "Button 컴포넌트: 색상 불일치"
- 라벨: enhancement (선택한 유형)
- 내용: 사용자 피드백 + 맥락 정보
- 작성자: {사용자명}
- 링크: https://github.com/...../issues/123
```

### 단계 4: Fallback (토큰 없을 때)
```
.state/pending-issues/
├── 20260225_button-color-mismatch.md
└── 20260225_medium-size-needed.md

사용자에게 안내:
"로컬에 저장되었습니다.
gh auth login 후 동기화하세요:
/create-issue:sync-pending"
```

---

## 5. 코드 구현 가이드

### Claude 명령어 변경사항

#### `/designer` 워크플로우
```
1. 컴포넌트 개발
2. Storybook 실행
3. 사용자 검증 요청 (AskUserQuestion)
4. 검증 결과 처리
 ├── 완료 → 공유 확인 (AskUserQuestion)
 ├── 미완료 → 수정 → 재검증
 └── 질문 → 답변 → 재검증
5. PR 생성 또는 로컬 저장
6. 불만/피드백 감지 → Issue 공유 확인
```

#### `/flow` 워크플로우
```
1. 플로우 설계
2. Dev 서버 실행
3. 사용자 검증 요청 (AskUserQuestion)
4. [동일] 검증 결과 처리
5. [동일] PR 생성 또는 로컬 저장
6. [동일] 불만/피드백 감지 → Issue 공유 확인
```

#### `/create-issue` 워크플로우
```
1. 이슈 정보 수집
2. 기본 라벨 선택 (bug/enhancement/documentation/question)
3. 사용자 확인 (공유할지)
4. Issue 생성 또는 로컬 저장
```

### AskUserQuestion 템플릿

#### 검증 요청
```json
{
 "question": "검증이 완료되셨나요?",
 "header": "QA Check",
 "options": [
 {
 "label": "완료 - 모두 정상",
 "description": "시각적 일치, 기능 정상, 접근성 확인됨"
 },
 {
 "label": "미완료 - 수정 필요",
 "description": "문제가 있어서 수정이 필요합니다"
 },
 {
 "label": "질문 있음",
 "description": "확인할 사항이 있습니다"
 }
 ],
 "multiSelect": false
}
```

#### 공유 확인
```json
{
 "question": "개발자에게 공유하시겠습니까?",
 "header": "Share to Developer",
 "options": [
 {
 "label": "PR 생성",
 "description": "GitHub에 PR을 생성하여 개발자 리뷰 요청"
 },
 {
 "label": "로컬 저장",
 "description": "로컬 브랜치에만 저장 (나중에 수동 공유)"
 },
 {
 "label": "수정 후 재검증",
 "description": "코드를 수정한 후 다시 검증"
 }
 ],
 "multiSelect": false
}
```

#### Issue 공유 확인
```json
{
 "question": "이슈로 등록하시겠습니까?",
 "header": "Create Issue",
 "options": [
 {
 "label": "Issue 생성 - Bug",
 "description": "버그 리포트로 등록합니다"
 },
 {
 "label": "Issue 생성 - Enhancement",
 "description": "기능 개선요청으로 등록합니다"
 },
 {
 "label": "Issue 생성 - Question",
 "description": "질문으로 등록합니다"
 },
 {
 "label": "로컬 저장",
 "description": "로컬에만 저장합니다"
 }
 ],
 "multiSelect": false
}
```

---

## 6. 상태 저장 (로컬 Fallback)

### 검증 상태
```
.claude/state/validations/
├── designer/
│ ├── 20260225_button_validation.json
│ └── 20260225_input_validation.json
└── flow/
 └── 20260225_signup_validation.json
```

**파일 내용**:
```json
{
 "id": "button_20260225_143000",
 "type": "designer",
 "component": "Button",
 "status": "validation_passed",
 "validation_date": "2026-02-25T14:30:00Z",
 "validator": "사용자명",
 "notes": "모든 상태 정상, 색상 일치",
 "pr_created": false,
 "issues_created": []
}
```

### 보류 중인 공유
```
.claude/state/pending-shares/
├── designer/
│ └── button_to_share.json
└── flow/
 └── signup_to_share.json
```

**파일 내용**:
```json
{
 "id": "button_20260225_143000",
 "type": "designer",
 "branch": "component/button",
 "title": "[designer] 박나현: Button 컴포넌트",
 "body": "...",
 "ready_to_share": true,
 "share_date": "2026-02-25T14:35:00Z",
 "shared": false
}
```

---

## 7. 참고 자료

- GitHub 기본 라벨: `gh label list`
- Issue 템플릿: `.claude/templates/issue-template.md`
- PR 템플릿: `.claude/templates/pr-template.md`
- 컴포넌트 스펙: `.claude/spec/component-spec.md`
- 플로우 스펙: `.claude/spec/flow-spec.md`
