# 의도 자동 감지 (Intent Detection) 시스템

## 개요

사용자가 명시적인 `/command`를 입력하지 않아도, 사용자의 의도를 분석하여 자동으로 적절한 명령을 실행하는 시스템입니다.

---

## 1. 의도 감지 규칙

### 1-1. Designer 의도 감지
**Skill 호출**: `Skill("designer")`
**권한**: designer+ (admin, developer, designer)

**감지 키워드** (정규식 매칭, 대소문자 무시):

```
컴포넌트 관련:
- "컴포넌트 (만들어|추가|수정|만들|만들어줘)"
- "(버튼|카드|입력|선택|폼|다이얼로그|모달) (만들어|추가|수정)"
- "UI (컴포넌트)? (만들어|추가|수정)"
- "(스토리|스토리북) (만들어|추가|작성)"
- "(타입스크립트|ts)? 컴포넌트"
- "재사용 가능한 컴포넌트"

디자인 시스템:
- "디자인 시스템 (컴포넌트|UI)"
- "Emocog 테마 (컴포넌트|적용)"
- "(색상|레이아웃|아이콘) 컴포넌트"

웹/네이티브:
- "(웹|web) 컴포넌트"
- "(네이티브|native|리액트 네이티브) 컴포넌트"
- "다중 플랫폼 UI"
```

**거절 조건** (권한 없음):
```
사용자 역할이 pm 또는 guest인 경우:
 "죄송합니다. [역할]은 /designer를 사용할 수 없습니다.
필요한 권한: designer 이상 (admin, developer, designer)"
```

---

### 1-2. Flow 의도 감지
**Skill 호출**: `Skill("flow")`
**권한**: 모든 역할 (admin, developer, designer, pm)

**감지 키워드** (정규식 매칭, 대소문자 무시):

```
플로우 설계:
- "플로우 (만들어|설계|디자인|구성)"
- "(화면|페이지) (설계|만들어|디자인)"
- "(서비스|앱|웹) (플로우|흐름|설계)"
- "(사용자|고객) (흐름|플로우|여정)"

온보딩/가입:
- "온보딩 (플로우|설계|만들어)"
- "(회원가입|가입|로그인) (플로우|설계|화면)"
- "인증 (플로우|흐름)"

결제/구매:
- "(결제|구매|체크아웃) (플로우|설계)"
- "결제 화면"

대시보드/기타:
- "(대시보드|홈화면|메인화면) (만들어|설계)"
- "(상품|프로필|설정) 페이지"
- "서비스 (디자인|기획|구축)"
- "화면 네비게이션"

바이브코딩:
- "대충 (만들어|설계|구성)"
- "이런 식으로 (플로우|화면|페이지)"
- "약간 이런 (느낌|느낌의 플로우)"
```

---

### 1-3. Create-Issue 의도 감지
**Skill 호출**: `Skill("create-issue")`
**권한**: 모든 역할 (admin, developer, designer, pm)

**감지 키워드** (정규식 매칭, 대소문자 무시):

```
버그 리포트:
- "(버그|bug) (제보|리포트|신고|있|발견)"
- "(문제|에러|오류) (있|발생|발견)"
- "동작 (안|안 해|안됨|안 됨)"
- "(안 보|안보임|안 보임|표시 안)"
- "깨진|깨짐"

기능 요청:
- "(기능|피처) (추가|요청|원|필요)"
- "(~)? (만들어|추가|지원)해주세요"
- "지원 (해|해줘)"
- "(개선|개선사항|개선하면) (좋을|좋겠)"

피드백:
- "(피드백|의견|건의) (있|있음|말)"
- "다시 생각해보니"
- "더 나으면"
- "향후에는"

문서/질문:
- "(문서|가이드|도움말) (추가|개선|필요)"
- "(어떻게|어디서|뭐로) (하|해)"
- "사용법"
```

---

### 1-4. Admin 의도 감지
**Skill 호출**: `Skill("admin")`
**권한**: admin/developer만

**감지 키워드** (정규식 매칭, 대소문자 무시):

```
팀원 관리:
- "(팀원|멤버|사용자) (추가|초대|등록|관리)"
- "권한 (변경|수정|관리)"

템플릿/스펙:
- "(컴포넌트|플로우) 스펙 (수정|업데이트|변경)"
- "(규칙|규정|규격) (추가|수정|변경)"
- "템플릿 (관리|수정|업데이트)"

테마/디자인:
- "테마 (수정|업데이트|변경)"
- "Emocog (테마|색상|토큰) (수정|업데이트)"
- "디자인 토큰 (수정|업데이트)"

전체 관리:
- "프로젝트 설정"
- "(전체|일괄) (설정|관리|구성)"
```

**거절 조건** (권한 없음):
```
사용자 역할이 designer 또는 pm인 경우:
 "죄송합니다. [역할]은 /admin을 사용할 수 없습니다.
필요한 권한: admin/developer"
```

---

### 1-5. Setup 의도 감지
**Skill 호출**: `Skill("setup")`
**권한**: 모든 역할

**감지 조건** (우선순위 높음):

```
1. `.user-identity` 파일 없음 (매 세션 시작 시 자동 확인)
 → 자동으로 /setup 실행

2. 사용자가 명시적으로 요청:
 - "설정해줘"
 - "처음 설정"
 - "초기화"
 - "계정 만들기"
 - "신원 설정"
 - "(이름|역할|github) 등록"
```

**자동 트리거**:
```bash
# 세션 시작 시 자동 확인
if [ ! -f .user-identity ]; then
 # 자동으로 /setup 실행
 echo "초기 설정이 필요합니다. /setup을 실행해주세요."
fi
```

---

## 2. 플로우 일관성 구조

모든 command는 다음의 **표준화된 플로우**를 따릅니다:

### 표준 플로우 (7단계)

```
1. 선행 조건 확인
 ├─ .user-identity 확인 (없으면 /setup)
 └─ 권한 검증 (권한 없으면 거절 메시지 + 중단)

2. 정보 수집 (AskUserQuestion)
 ├─ 필수 정보 (예: 컴포넌트명, 플로우명 등)
 └─ 선택 정보 (예: 설명, 환경 정보 등)

3. 상태 준비
 ├─ Git 작업 (브랜치 생성, pull 등)
 └─ 디렉토리 구조 확인

4. 작업 수행
 ├─ 코드 생성 / 설계 / 이슈 생성
 └─ 검증

5. 사용자 검증 요청 (AskUserQuestion)
 ├─ Storybook/Dev 서버 / 이슈 정보 확인
 ├─ 완료 / 미완료 / 질문 선택
 └─ 결과에 따라 처리

6. 공유 확인 (AskUserQuestion)
 ├─ PR 생성 / 로컬 저장 / 수정 선택
 └─ PR 생성 시 라벨: enhancement (기본)

7. 불만/피드백 감지 (AskUserQuestion)
 ├─ 버그/개선/질문 Issue 생성 여부 확인
 └─ Issue 생성 또는 로컬 저장
```

### 단계별 AskUserQuestion 형식

#### 2-1. 정보 수집 (단계 2)
```json
{
 "questions": [
 {
 "question": "컴포넌트명을 입력하세요",
 "header": "Component Name",
 "options": [
 {"label": "새 컴포넌트", "description": "새로 만들기"},
 {"label": "기존 컴포넌트", "description": "수정 또는 확장"}
 ],
 "multiSelect": false
 }
 ]
}
```

#### 2-2. 검증 요청 (단계 5)
```json
{
 "questions": [
 {
 "question": "검증이 완료되셨나요?",
 "header": "QA Check",
 "options": [
 {"label": "완료 - 모두 정상", "description": "모든 항목 확인됨"},
 {"label": "미완료 - 수정 필요", "description": "문제점 있음"},
 {"label": "질문 있음", "description": "확인할 사항 있음"}
 ],
 "multiSelect": false
 }
 ]
}
```

#### 2-3. 공유 확인 (단계 6)
```json
{
 "questions": [
 {
 "question": "개발자에게 공유하시겠습니까?",
 "header": "Share to Developer",
 "options": [
 {"label": "PR 생성", "description": "GitHub에 PR 생성"},
 {"label": "로컬 저장", "description": "로컬에만 저장"},
 {"label": "수정 후 재검증", "description": "코드 수정 후 다시"}
 ],
 "multiSelect": false
 }
 ]
}
```

#### 2-4. Issue 공유 (단계 7)
```json
{
 "questions": [
 {
 "question": "이슈로 등록하시겠습니까?",
 "header": "Create Issue",
 "options": [
 {"label": "Issue 생성 - Bug", "description": "버그로 등록"},
 {"label": "Issue 생성 - Enhancement", "description": "개선요청으로 등록"},
 {"label": "로컬 저장", "description": "로컬에만 저장"}
 ],
 "multiSelect": false
 }
 ]
}
```

---

## 3. 의도 감지 구현 알고리즘

### 3-1. 감지 순서 (우선순위)

```python
def detect_intent(user_input, user_role, user_identity_exists):
 # 1. Setup 우선 (신원 파일 없음)
 if not user_identity_exists:
 return "setup"

 # 2. Intent 키워드 매칭
 if match_designer_keywords(user_input):
 if check_permission(user_role, "designer"):
 return "designer"
 else:
 return "permission_denied"

 if match_flow_keywords(user_input):
 if check_permission(user_role, "flow"):
 return "flow"
 else:
 return None # flow는 모든 역할 가능

 if match_create_issue_keywords(user_input):
 return "create_issue" # 모든 역할 가능

 if match_admin_keywords(user_input):
 if check_permission(user_role, "admin"):
 return "admin"
 else:
 return "permission_denied"

 # 3. 매칭 실패 시 None 반환 (명시적 명령 요청)
 return None
```

### 3-2. 키워드 매칭 구현

```python
def match_designer_keywords(user_input):
 patterns = [
 r"컴포넌트\s*(만들|추가|수정|만들어)",
 r"(버튼|카드|입력|선택)\s*(만들|추가|수정)",
 r"UI\s*(만들|추가|수정)",
 r"스토리\s*(만들|추가|작성)",
 r"디자인\s*시스템",
 r"웹\s*컴포넌트",
 r"네이티브\s*컴포넌트",
 ]
 return any(re.search(pattern, user_input, re.IGNORECASE) for pattern in patterns)

def match_flow_keywords(user_input):
 patterns = [
 r"플로우\s*(만들|설계|구성)",
 r"(화면|페이지)\s*(설계|만들|디자인)",
 r"온보딩\s*(만들|설계)",
 r"(결제|구매)\s*플로우",
 r"대시보드\s*(만들|설계)",
 r"대충\s*(만들|설계)",
 ]
 return any(re.search(pattern, user_input, re.IGNORECASE) for pattern in patterns)

def match_create_issue_keywords(user_input):
 patterns = [
 r"(버그|에러|문제)\s*(제보|있|발견)",
 r"동작\s*안",
 r"(기능|피처)\s*(추가|요청|필요)",
 r"피드백",
 r"문서\s*추가",
 ]
 return any(re.search(pattern, user_input, re.IGNORECASE) for pattern in patterns)

def match_admin_keywords(user_input):
 patterns = [
 r"(팀원|멤버)\s*추가",
 r"권한\s*변경",
 r"(스펙|규칙)\s*(수정|변경)",
 r"테마\s*수정",
 r"템플릿\s*관리",
 ]
 return any(re.search(pattern, user_input, re.IGNORECASE) for pattern in patterns)
```

---

## 4. 실행 흐름 (Claude Code)

### 4-1. 세션 시작 시
```
1. .user-identity 확인
 ├─ 없음 → /setup 자동 실행
 └─ 있음 → 계속 진행

2. 사용자 입력 대기
```

### 4-2. 사용자 입력 분석
```
사용자 입력 예: "버튼 컴포넌트 만들어줘"

1. 의도 감지
 → match_designer_keywords() 매칭 성공
 → 반환값: "designer"

2. 권한 검증
 → user_role = "designer"
 → permission 확인: 통과

3. Skill 실행
 → Skill("designer") 호출

4. 사용자는 /designer 명령을 사용하지 않음 (자동 실행됨)
```

### 4-3. 의도 감지 실패 시
```
사용자 입력 예: "뭐 할 수 있어?"

1. 의도 감지 → None (매칭 실패)

2. Claude 응답
 → 명시적 명령 제안:
 - /designer — 컴포넌트 제작/수정
 - /flow — 플로우 설계
 - /create-issue — 이슈 제보
 - /admin — 템플릿 관리
 - /setup — 초기 설정
```

---

## 5. 권한 매트릭스

| Intent | admin | developer | designer | pm | guest |
|--------|-------|-----------|----------|-----|-------|
| setup | | | | | |
| designer | | | | | |
| flow | | | | | |
| create-issue | | | | | |
| admin | | | | | |

**거절 메시지 형식**:
```
 권한 없음

죄송합니다. 역할 [{role}]은 [{command}]을 사용할 수 없습니다.

필요한 권한: {required_role}

담당자에게 문의하세요:
- 이름: 보이드
- GitHub: boydcog
- 역할: maintainer
```

---

## 6. 예제

### 예제 1: Designer 의도 감지
```
사용자: "버튼 컴포넌트 만들어줘"
↓
Claude: 의도 감지 → "designer"
Claude: 권한 검증 → designer 권한
Claude: Skill("designer") 자동 실행
↓
[/designer 명령 없음 - 자동으로 시작됨]
사용자: 프레임워크 선택 요청받음
...
```

### 예제 2: Flow 의도 감지
```
사용자: "회원가입 플로우 만들어줘"
↓
Claude: 의도 감지 → "flow"
Claude: 권한 검증 → 모든 역할 가능 (pm도 가능)
Claude: Skill("flow") 자동 실행
↓
[/flow 명령 없음 - 자동으로 시작됨]
사용자: 제품명 입력 요청받음
...
```

### 예제 3: Create-Issue 의도 감지
```
사용자: "Button 컴포넌트에서 버그가 있어요. 클릭이 안 되네요."
↓
Claude: 의도 감지 → "create-issue"
Claude: 불만 감지 + Issue 공유 플로우
Claude: Skill("create-issue") 자동 실행
↓
[/create-issue 명령 없음 - 자동으로 시작됨]
사용자: Issue 유형 선택 요청받음 (bug/enhancement/...)
...
```

### 예제 4: 권한 거절
```
사용자 (pm): "컴포넌트 만들어줘"
↓
Claude: 의도 감지 → "designer"
Claude: 권한 검증 → pm 역할 불가능
Claude: 거절 메시지 출력
↓
 죄송합니다. 역할 [pm]은 /designer를 사용할 수 없습니다.
필요한 권한: designer 이상 (admin, developer, designer)
```

### 예제 5: Setup 자동 트리거
```
세션 시작
↓
Claude: .user-identity 파일 확인 → 없음
Claude: Skill("setup") 자동 실행
↓
[사용자 입력 없이도 setup 시작]
사용자: 이름 입력 요청받음
...
```

---

## 7. 구현 체크리스트

- [ ] Intent detection 알고리즘 구현
- [ ] 키워드 매칭 패턴 정의
- [ ] 권한 검증 로직 구현
- [ ] AskUserQuestion 템플릿 표준화
- [ ] 모든 command 플로우 통일
- [ ] 오류 메시지 표준화
- [ ] 테스트 (다양한 의도 감지 시나리오)

---

## 참고

- [CLAUDE.md - 자동 의도 감지](../../../CLAUDE.md#자동-의도-감지-intent-detection)
- [Validation Flow](./validation-flow.md)
- [Command: Designer](../commands/designer.md)
- [Command: Flow](../commands/flow.md)
- [Command: Create-Issue](../commands/create-issue.md)
- [Command: Admin](../commands/admin.md)
