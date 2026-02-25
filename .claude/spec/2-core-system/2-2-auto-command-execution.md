# 자동 명령 실행 시스템 (Auto Command Execution)

## 개요

사용자가 명령을 입력하지 않아도, Claude가 사용자의 의도를 감지하여 **자동으로 해당 명령을 실행**합니다.

---

## 문제점 (기존 방식)

```
 이전 방식:

사용자: "컴포넌트 만들어줄 수 있어?"
Claude: "네, /designer 명령을 사용하세요"
사용자: (사용자가 명령 입력해야 함)
/designer
Claude: [시작]
```

**문제**:
- 사용자가 여전히 명령을 입력해야 함
- 명령어를 알아야 함
- 직관적이지 않음

---

## 올바른 방식 (자동 실행)

```
 올바른 방식:

사용자: "컴포넌트 만들어줄 수 있어?"
↓
Claude: 의도 감지 → "designer"
↓
Claude: "이 세션에서는 /designer 명령을 사용해서
디자인 작업을 처리할게요"
↓
Claude: (자동으로 /designer 실행 - 사용자 입력 없음)
↓
Claude: [프레임워크 선택 요청]
```

**장점**:
- 사용자는 명령을 입력하지 않음
- 명령어를 알 필요 없음
- 직관적 경험
- 자동으로 시작됨

---

## 구현 원리

### 단계 1: 의도 감지 및 안내

```python
def handle_user_input(user_message):
 """
 1단계: 의도 감지
 """
 feedback = detect_feedback(user_message)
 intent = detect_intent(user_message)

 if intent == "designer":
 # Claude의 응답
 print("이 세션에서는 /designer 명령을 사용해서")
 print("디자인 작업을 처리할게요.")
 print("")

 # 단계 2로 자동 진행 (사용자 입력 없음)
 execute_command("designer")
```

### 단계 2: 자동 실행

```python
def execute_command(command_name):
 """
 2단계: 명령 자동 실행
 """
 if command_name == "designer":
 return Skill("designer") # 자동 실행
 elif command_name == "flow":
 return Skill("flow")
 elif command_name == "create-issue":
 return Skill("create-issue")
 elif command_name == "admin":
 return Skill("admin")
 elif command_name == "setup":
 return Skill("setup")
```

---

## 실행 흐름 (상세)

### 흐름도

```
사용자 입력
 ↓
1 의도 감지
 ├─ intent = detect_intent(user_input)
 ├─ feedback = detect_feedback(user_input)
 └─ confidence 계산
 ↓
2 의도 판정
 ├─ designer? → Yes
 ├─ flow? → Yes
 ├─ create-issue? → Yes
 ├─ admin? → Yes
 ├─ setup? → Yes
 └─ 없음 → 일반 대화로 진행
 ↓
3 권한 검증
 ├─ 사용자 역할 확인
 └─ 권한 있음? → Yes
 ↓
4 안내 메시지 출력
 "이 세션에서는 /[command] 명령을 사용해서
 [작업]을 처리할게요"
 ↓
5 자동 명령 실행
 Skill("[command]")
 (사용자 입력 없음 - 자동 진행)
 ↓
6 명령 실행 시작
 [프레임워크 선택] 또는 [정보 수집] 등
```

---

## 예제 시나리오

### 예제 1: Designer 의도 자동 인식

```
사용자: "버튼 컴포넌트 만들어줄 수 있어?"

Claude:
이 세션에서는 /designer 명령을 사용해서
디자인 작업을 처리할게요.

[자동 실행 - 사용자 명령 입력 없음]

프레임워크를 선택해주세요:

[Web] Next.js, Vite, Remix
[Native] React Native + Gluestack
```

### 예제 2: Flow 의도 자동 인식

```
사용자: "회원가입 플로우를 만들어야 하는데 도와줄래?"

Claude:
이 세션에서는 /flow 명령을 사용해서
서비스 플로우 설계를 처리할게요.

[자동 실행 - 사용자 명령 입력 없음]

제품명을 입력하세요:

예:
- user-onboarding
- payment-flow
- product-dashboard

또는 새로운 이름:
```

### 예제 3: Create-Issue 의도 자동 인식

```
사용자: "Button 컴포넌트에서 버그가 있어요.
클릭이 안 되네요."

Claude:
이 세션에서는 /create-issue 명령을 사용해서
이슈 제보를 처리할게요.

[자동 실행 - 사용자 명령 입력 없음]

이슈 유형을 선택해주세요:

[Bug] 버그 리포트
[Enhancement] 기능 요청
[Documentation] 문서 개선
[Question] 질문
```

### 예제 4: Admin 의도 자동 인식

```
사용자: "팀원을 추가해야 하는데, 어떻게 해?"

Claude:
이 세션에서는 /admin 명령을 사용해서
템플릿 관리를 처리할게요.

[자동 실행 - 사용자 명령 입력 없음]

어떤 작업을 진행하시겠습니까?

[컴포넌트 스펙 수정] 스펙 가이드 업데이트
[역할 및 권한 수정] 역할별 권한 변경
[팀원 추가] 새 팀원 등록
[Emocog 테마 업데이트] 디자인 토큰 업데이트
```

### 예제 5: 권한 거절

```
사용자 (pm): "컴포넌트 만들어줄 수 있어?"

Claude:
이 세션에서는 /designer 명령을 사용해야 하는데,
죄송합니다. 역할 [pm]은 /designer를 사용할 수 없습니다.

필요한 권한: designer 이상 (admin, developer, designer)

현재 역할 [pm]이 할 수 있는 작업:
- /flow — 서비스 플로우 설계
- /create-issue — 이슈 제보
- /setup — 신원 설정 변경

다른 작업을 도와드릴까요?
```

### 예제 6: 권한 확인 후 자동 실행 (admin/developer)

```
사용자 (admin): "팀원을 추가해야 해"

Claude:
이 세션에서는 /admin 명령을 사용해서
템플릿 관리를 처리할게요.

[자동 실행 - 사용자 명령 입력 없음]

어떤 작업을 진행하시겠습니까?
...
```

---

## 안내 메시지 포맷 (표준화)

### 디자인

```
이 세션에서는 /designer 명령을 사용해서
[작업 설명]을 처리할게요.

[자동 실행 시작]
─────────────────────

[실제 작업 시작 메시지]
```

### Flow

```
이 세션에서는 /flow 명령을 사용해서
서비스 플로우 설계를 처리할게요.

[자동 실행 시작]
─────────────────────

[실제 작업 시작 메시지]
```

### Create-Issue

```
이 세션에서는 /create-issue 명령을 사용해서
이슈 제보를 처리할게요.

[자동 실행 시작]
─────────────────────

[실제 작업 시작 메시지]
```

### Admin

```
이 세션에서는 /admin 명령을 사용해서
템플릿 관리를 처리할게요.

[자동 실행 시작]
─────────────────────

[실제 작업 시작 메시지]
```

---

## 권한 검증 및 거절

### 검증 순서

```python
def validate_and_execute(intent, user_role):
 """
 1. 권한 검증
 2. 안내 메시지 출력
 3. 자동 실행
 """

 # 1단계: 권한 검증
 if not has_permission(intent, user_role):
 # 거절 메시지 출력
 print_permission_denied(intent, user_role)
 return

 # 2단계: 안내 메시지 출력
 print_guidance_message(intent)

 # 3단계: 자동 실행
 execute_command(intent)
```

### 권한 거절 메시지

```
 권한 없음

이 세션에서는 /[command] 명령이 필요한데,
죄송합니다. 역할 [{role}]은 /[command]를 사용할 수 없습니다.

필요한 권한: {required_roles}

현재 역할 [{role}]이 할 수 있는 작업:
- /command1 — 설명
- /command2 — 설명
- /command3 — 설명

다른 작업을 도와드릴까요?

관리자 정보:
- 이름: 보이드
- GitHub: boydcog
```

---

## 의도별 안내 메시지 (구체적)

### Designer

```
이 세션에서는 /designer 명령을 사용해서
Emocog 테마 기반 재사용 가능한 컴포넌트를
만들거나 수정하겠습니다.

[자동 실행 시작]
─────────────────────

프레임워크를 선택해주세요:

[Web] Next.js, Vite, Remix
[Native] React Native + Gluestack
```

### Flow

```
이 세션에서는 /flow 명령을 사용해서
서비스 플로우를 설계하겠습니다.

완성된 컴포넌트를 활용하여 화면을 만들고
네비게이션을 연결합니다.

[자동 실행 시작]
─────────────────────

제품명을 입력하세요:

예: user-onboarding, payment-flow, product-dashboard
또는 새로운 이름을 자유롭게 입력하세요.
```

### Create-Issue

```
이 세션에서는 /create-issue 명령을 사용해서
GitHub에 이슈를 제보하겠습니다.

버그, 기능 요청, 피드백 등을 등록할 수 있습니다.

[자동 실행 시작]
─────────────────────

이슈 유형을 선택해주세요:

[Bug] 버그 리포트
[Enhancement] 기능 요청
[Documentation] 문서 개선
[Question] 질문
```

### Admin

```
이 세션에서는 /admin 명령을 사용해서
템플릿과 프로젝트 설정을 관리하겠습니다.

스펙, 역할, 팀원, 테마 등을 수정할 수 있습니다.

[자동 실행 시작]
─────────────────────

어떤 작업을 진행하시겠습니까?

[컴포넌트 스펙 수정] 스펙 가이드 업데이트
[역할 및 권한 수정] 역할별 권한 변경
[팀원 추가] 새 팀원 등록
[Emocog 테마 업데이트] 디자인 토큰 업데이트
```

### Setup

```
이 세션에서는 /setup 명령을 사용해서
초기 설정을 진행하겠습니다.

이름, 역할, GitHub 정보를 등록합니다.

[자동 실행 시작]
─────────────────────

사용자 이름을 입력해주세요:
```

---

## 일반 대화 (의도 감지 안 됨)

```
사용자: "뭐 할 수 있어?"

Claude:
다양한 작업을 도와드릴 수 있습니다:

1. /designer — 컴포넌트 제작/수정/확장
 예: "컴포넌트 만들어줘", "버튼 추가"

2. /flow — 서비스 플로우 설계
 예: "플로우 만들어줘", "온보딩 설계해"

3. /create-issue — 이슈 제보
 예: "버그 있어", "기능 추가해줘"

4. /admin — 템플릿 관리
 예: "팀원 추가", "테마 수정"

5. /setup — 초기 설정
 예: "설정해줘", "계정 만들어"

어떤 작업을 시작할까요?
```

---

## 구현 체크리스트

- [ ] 의도 감지 → 명령 매핑
- [ ] 권한 검증 로직
- [ ] 안내 메시지 (5가지)
- [ ] 자동 실행 (Skill 호출)
- [ ] 권한 거절 메시지
- [ ] 일반 대화 폴백

---

## 사용자 경험 비교

### 이전 (명령 입력 필요)
```
사용자: "컴포넌트 만들어줄 수 있어?"
Claude: "네, /designer 명령을 사용하세요"
사용자: (명령 입력)
/designer
Claude: [시작]
```

### 현재 (자동 실행)
```
사용자: "컴포넌트 만들어줄 수 있어?"
Claude: "이 세션에서는 /designer 명령을 사용해서
 디자인 작업을 처리할게요"
Claude: [자동 실행 - 사용자 입력 없음]
Claude: [시작]
```

**개선점**:
- 사용자가 명령을 입력하지 않음
- 직관적이고 자연스러운 흐름
- 빠른 시작

---

## 참고

- [Intent Detection](./intent-detection.md)
- [Flow Standardization](./flow-standardization.md)
- [Global Feedback Detection](./global-feedback-detection.md)
