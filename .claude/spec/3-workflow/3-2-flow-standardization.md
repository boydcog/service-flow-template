# Command 플로우 표준화 (Flow Standardization)

## 개요

모든 command (`/designer`, `/flow`, `/create-issue`, `/admin`)는 다음의 **7단계 표준 플로우**를 따릅니다. 이를 통해 모든 세션과 사용자가 일관된 경험을 얻습니다.

---

## 표준 7단계 플로우

```
1 선행 조건 확인
 ↓
2 정보 수집 (AskUserQuestion)
 ↓
3 상태 준비 (Git, 디렉토리 등)
 ↓
4 작업 수행 (코드 생성, 설계, 이슈 생성)
 ↓
5 사용자 검증 요청 (AskUserQuestion)
 ↓
6 공유 확인 (AskUserQuestion)
 ↓
7 불만/피드백 감지 및 Issue 공유 (AskUserQuestion)
```

---

## 각 단계별 상세 명세

### 1단계: 선행 조건 확인

**공통 작업**:
```
 .user-identity 파일 확인
 └─ 없으면 Skill("setup") 실행

 권한 검증
 └─ 사용자 역할 확인 후 접근 권한 검증
 └─ 권한 없으면 거절 메시지 + 중단

 Git 상태 확인 (필요 시)
 └─ git pull --rebase origin main
```

**Command별 추가 작업**:

| Command | 추가 작업 |
|---------|---------|
| designer | Framework 선택 준비 |
| flow | Product name 선택 준비 |
| create-issue | 이슈 유형 선택 준비 |
| admin | 액션 선택 준비 |

---

### 2단계: 정보 수집 (AskUserQuestion)

**구조**:
```json
{
 "questions": [
 {
 "question": "명확한 질문",
 "header": "짧은 카테고리 (12자 이하)",
 "options": [
 {
 "label": "옵션 1",
 "description": "설명 (50자 이내)"
 }
 ],
 "multiSelect": false
 }
 ]
}
```

**Command별 구체적 질문**:

#### designer
```
Q1: 프레임워크 선택
Options:
- Web (Next.js / Vite / Remix)
- Native (React Native + Gluestack)

Q2: 액션 선택 (이전 작업 완료 후)
Options:
- 새 컴포넌트 생성
- 기존 컴포넌트 확장 (스토리/변형 추가)
- 기존 컴포넌트 수정

Q3: 컴포넌트 정보
- 이름 (필수)
- 설명 (필수)
```

#### flow
```
Q1: 제품명 선택
Options:
- user-onboarding
- payment-flow
- product-dashboard
- 또는 새로 입력

Q2: 기능 설명 (자유 형식, 바이브코딩)
- "사용자 회원가입 플로우"
- "1. 이메일 입력 2. 비밀번호 설정 3. 완료"
```

#### create-issue
```
Q1: 이슈 유형 선택
Options:
- Bug (버그/결함)
- Enhancement (새로운 기능/개선)
- Documentation (문서 개선)
- Question (질문)

Q2: 이슈 제목 (필수)
Q3: 상세 내용 (필수)
Q4: 관련 파일 (선택)
```

#### admin
```
Q1: 액션 선택
Options:
- 컴포넌트 스펙 수정
- 역할 및 권한 수정
- 팀원 추가
- Emocog 테마 업데이트

Q2: 설명 (필수)
Q3: 담당자 (선택, 기본: 현재 사용자)
```

---

### 3단계: 상태 준비 (Git, 디렉토리 등)

**공통 작업**:
```bash
# Git 작업
git checkout -b {branch-name} # 필요 시
git pull --rebase origin main

# 디렉토리 확인
ls -la {target-directory} # 대상 디렉토리 존재 확인
```

**Command별 구체적 작업**:

| Command | Branch | 디렉토리 | 파일 구조 |
|---------|--------|--------|---------|
| designer | `component/{name}` | `components/{web\|native}/ui/` | `.tsx` + `.stories.tsx` |
| flow | `flow/{product-name}` | `flows/{product-name}/` | `screens/*.tsx` + `page.tsx` |
| create-issue | N/A | N/A | N/A |
| admin | `admin/{action}` | `.claude/` | CHANGELOG + 파일 |

---

### 4단계: 작업 수행

**Designer**: 코드 생성
```
1. 컴포넌트 코드 생성 (TypeScript strict)
2. Props 인터페이스 정의
3. Storybook 스토리 파일 생성 (Web만)
4. 테스트 파일 생성
5. 검증 (Strict Mode)
```

**Flow**: 화면 설계 및 구현
```
1. 기능 설명에서 화면 추출
2. 컴포넌트 추천 (자동 매칭)
3. 각 화면별 컴포넌트 조립 (TSX)
4. 메인 플로우 페이지 생성 (page.tsx)
5. 네비게이션 연결
6. 검증 (Strict Mode)
```

**Create-Issue**: 이슈 생성
```
1. 이슈 템플릿 생성 (issue-template.md 참조)
2. 라벨 선택 (기본 라벨만)
3. GitHub Issue 생성 또는 로컬 저장
4. Fallback: 토큰 없으면 .state/pending-issues 저장
```

**Admin**: 변경사항 적용
```
1. 해당 파일 수정 (spec, manifest, etc.)
2. CHANGELOG 업데이트
3. 변경사항 커밋
4. PR 생성
```

---

### 5단계: 사용자 검증 요청 (AskUserQuestion)

**구조** (모든 command 동일):
```json
{
 "question": "검증이 완료되셨나요?",
 "header": "QA Check",
 "options": [
 {
 "label": "완료 - 모두 정상",
 "description": "모든 항목이 정상입니다"
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

**검증 내용** (Command별):

| Command | 검증 항목 |
|---------|---------|
| designer | Storybook에서 시각적/기능/접근성/반응형 확인 |
| flow | Dev 서버에서 플로우 연결/렌더링/기능/반응형 확인 |
| create-issue | 이슈 정보 (제목/내용/관련 파일) 확인 |
| admin | 변경사항 내용 및 영향도 확인 |

**검증 결과 처리**:

#### 완료 
```
다음 단계: 6단계 (공유 확인)로 진행
```

#### 미완료 
```
1. 사용자 입력: 수정할 부분 설명
2. Claude: 코드/설계 수정
3. Storybook/Dev 서버 재시작
4. 재검증 요청 (5단계 반복)
```

#### 질문 
```
1. 사용자 질문 입력
2. Claude: 질문 답변
3. 추가 검증 필요 여부 확인
4. 필요시 재검증 (5단계 반복)
```

---

### 6단계: 공유 확인 (AskUserQuestion)

**구조** (모든 command 동일):
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

**각 선택에 따른 처리**:

#### PR 생성 선택
```
1. Git 작업
 git add .
 git commit -m "[{role}] {user}: {description}"

2. PR 생성
 gh pr create --title "[{role}] {user}: {title}"
 --body "{body}"
 --base main
 --head {branch}

3. 라벨 자동 할당
 라벨: enhancement (기본)

4. PR 정보 출력
 PR URL, 상태 등
```

#### 로컬 저장 선택
```
1. 브랜치 유지 (푸시 안함)
2. 상태 저장
 .claude/state/pending-shares/{role}/{name}.json
3. 사용자 안내
 "로컬에 저장되었습니다. 나중에 공유하려면
 bash .claude/hooks/create-pr.sh {branch} {title}"
```

#### 수정 후 재검증 선택
```
1. 사용자에게 코드 수정 권장
2. 수정 후 다시 5단계로 이동
 (검증 요청 반복)
```

---

### 7단계: 불만/피드백 감지 및 Issue 공유 (선택)

**불만/피드백 감지 시점**:
- 개발 중 또는 완료 후
- 사용자가 부정적 의견 표현 시

**감지 패턴**:
```
"색상이 다르네요"
"필요해요"
"버그가 있어요"
"안 보임"
"너무 작음"
"개선되면 좋겠"
```

**Issue 공유 확인 (AskUserQuestion)**:
```json
{
 "question": "불만/피드백을 감지했습니다. Issue로 등록하시겠습니까?",
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
 "label": "로컬 저장",
 "description": "로컬에만 저장합니다"
 }
 ],
 "multiSelect": false
}
```

**선택에 따른 처리**:

#### Issue 생성 선택 (Bug/Enhancement)
```
1. Issue 제목 자동 생성
 "[컴포넌트명]: [사용자 피드백]"

2. Issue 생성
 gh issue create --title "{title}"
 --body "{body}"
 --label "{bug|enhancement}"

3. Issue 정보 출력
 Issue URL, 라벨 등
```

#### 로컬 저장 선택
```
1. 상태 저장
 .claude/state/pending-issues/{type}/{name}.json

2. 사용자 안내
 "로컬에 저장되었습니다. 나중에 동기화하려면
 gh auth login 후 /create-issue:sync-pending"
```

---

## 모든 Command 플로우 비교

| 단계 | designer | flow | create-issue | admin |
|------|----------|------|--------------|-------|
| 1 선행 조건 | .user-identity + 권한 | .user-identity + 권한 | .user-identity + 권한 | .user-identity + 권한 |
| 2 정보 수집 | Framework → 액션 → 정보 | 제품명 → 기능 설명 | 유형 → 제목 → 내용 | 액션 → 설명 → 담당자 |
| 3 상태 준비 | branch: component/{name} | branch: flow/{name} | N/A | branch: admin/{action} |
| 4 작업 수행 | 컴포넌트 코드 생성 | 화면 설계 및 구현 | Issue 생성 | 파일 수정 |
| 5 검증 요청 | Storybook 확인 | Dev 서버 확인 | 이슈 정보 확인 | 변경사항 확인 |
| 6 공유 확인 | PR/로컬/수정 | PR/로컬/수정 | GitHub/로컬 | PR/로컬 |
| 7 Issue 공유 | Bug/Enhancement/로컬 | Bug/Enhancement/로컬 | (이미 이슈) | 선택사항 |

---

## AskUserQuestion 통합 템플릿

### 검증 확인 (5단계 - 모든 command)
```json
{
 "questions": [
 {
 "question": "검증이 완료되셨나요?",
 "header": "QA Check",
 "options": [
 {"label": "완료 - 모두 정상", "description": "..."},
 {"label": "미완료 - 수정 필요", "description": "..."},
 {"label": "질문 있음", "description": "..."}
 ],
 "multiSelect": false
 }
 ]
}
```

### 공유 확인 (6단계 - designer, flow, admin)
```json
{
 "questions": [
 {
 "question": "개발자에게 공유하시겠습니까?",
 "header": "Share to Developer",
 "options": [
 {"label": "PR 생성", "description": "GitHub PR 생성"},
 {"label": "로컬 저장", "description": "로컬 저장"},
 {"label": "수정 후 재검증", "description": "수정 후 재검증"}
 ],
 "multiSelect": false
 }
 ]
}
```

### Issue 공유 (7단계 - 모든 command)
```json
{
 "questions": [
 {
 "question": "Issue로 등록하시겠습니까?",
 "header": "Create Issue",
 "options": [
 {"label": "Issue 생성 - Bug", "description": "버그로 등록"},
 {"label": "Issue 생성 - Enhancement", "description": "개선요청 등록"},
 {"label": "로컬 저장", "description": "로컬 저장"}
 ],
 "multiSelect": false
 }
 ]
}
```

---

## 구현 체크리스트

**각 Command가 다음을 준수해야 함**:

- [ ] 1단계: .user-identity + 권한 검증 포함
- [ ] 2단계: AskUserQuestion 사용 (필수 정보 수집)
- [ ] 3단계: Git 브랜치 생성 (필요 시)
- [ ] 4단계: 작업 수행 + 검증 (Strict Mode)
- [ ] 5단계: 사용자 검증 요청 (AskUserQuestion)
- [ ] 6단계: 공유 확인 (AskUserQuestion, create-issue는 선택)
- [ ] 7단계: 불만/피드백 감지 + Issue 공유 (선택)

**Fallback**:
- [ ] GitHub 토큰 없을 때 로컬 저장 처리
- [ ] PR/Issue 생성 실패 시 로컬 저장 처리
- [ ] 모든 오류 메시지 일관성 있게 포맷팅

---

## 참고

- [Intent Detection](./intent-detection.md)
- [Validation Flow](./validation-flow.md)
- [Command: Designer](../commands/designer.md)
- [Command: Flow](../commands/flow.md)
- [Command: Create-Issue](../commands/create-issue.md)
- [Command: Admin](../commands/admin.md)
