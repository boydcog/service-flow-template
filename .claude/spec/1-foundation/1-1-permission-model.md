# 권한 모델 (Permission Model)

## 개요

사용자 역할별로 할 수 있는 작업을 정의합니다.

---

## 권한 원칙

### 1. 명확한 제약: Admin만
```
Admin 기능은 엄격한 권한 제약이 있습니다:
- designer: admin 못함 (거절)
- pm: admin 못함 (거절)
```

### 2. 유연한 접근: 나머지
```
Designer, Flow, Create-Issue, Setup은
모든 역할이 시도할 수 있습니다.

그러나 각 역할의 "주요 작업"이 있습니다:
- admin: 관리 업무
- developer: 관리 + 개발 지원
- designer: 디자인 + 컴포넌트
- pm: 기획 + 플로우 + 이슈

→ 다른 작업을 하고 싶으면 "이건 보통 [역할]이 하는데,
 그래도 진행할까?" 정도로 안내만 함
```

---

## 권한 매트릭스 (수정됨)

| Intent | admin | developer | designer | pm | guest |
|--------|-------|-----------|----------|------|-------|
| **setup** | | | | | |
| **designer** | | | | | |
| **flow** | | | | | |
| **create-issue** | | | | | |
| **admin** | | | | | |

**범례**:
- = 완전 권한 (거절 없음)
- = 가능하지만 안내 (확인 후 진행)
- = 거절 (권한 없음)

---

## 권한 종류

### 1 완전 권한 ()
```
거절 없음. 바로 진행.

예:
사용자 (designer): "컴포넌트 만들어줄 수 있어?"
Claude: "이 세션에서는 /designer 명령을 사용해서
 컴포넌트를 만들겠습니다."
[자동 실행]
```

### 2 안내 후 진행 ()
```
"이건 보통 [역할]이 하는데, 그래도 할까?" 정도로 안내 후 진행.

예:
사용자 (pm): "컴포넌트 만들어줄 수 있어?"
Claude: "컴포넌트 제작은 보통 designer가 하는데,
 pm이셔도 진행하시겠습니까?"
[Yes] [No - 다른 작업 추천]
```

### 3 명확한 거절 ()
```
권한 없음. 거절하고 안내.

예:
사용자 (designer): "팀원 추가해줄 수 있어?"
Claude: "죄송합니다. Admin 기능은
 admin/developer 역할만 사용 가능합니다.

현재 역할 [designer]이 할 수 있는 작업:
- /designer — 컴포넌트 제작
- /flow — 플로우 설계
- /create-issue — 이슈 제보"
```

---

## 역할별 기본 작업 (가이드)

### Admin / Developer
```
주요 작업:
- /admin → 팀원 관리, 스펙 관리, 테마 관리
- /designer → 컴포넌트 제작 (기술 리뷰)
- /flow → 플로우 설계 검토
- /create-issue → 이슈 관리

권한:
 admin (완전 권한)
 designer (완전 권한)
 flow (완전 권한)
 create-issue (완전 권한)
```

### Designer
```
주요 작업:
- /designer → 컴포넌트 제작/수정

가능한 작업:
- /flow → 플로우 설계 (디자인 관점)
- /create-issue → 이슈 제보

권한:
 designer (완전 권한)
 flow (완전 권한)
 create-issue (완전 권한)
 admin (안내 후 거절 - "admin이 할 일입니다")
```

### PM
```
주요 작업:
- /flow → 플로우 설계/기획
- /create-issue → 이슈 제보 (기능 요청)

가능한 작업:
- /designer → 컴포넌트 제작 (필요시)
- /create-issue → 이슈 제보

권한:
 flow (완전 권한)
 create-issue (완전 권한)
 designer (안내 후 진행 - "보통 designer가 하는데...")
 admin (거절 - "관리자만 가능")
```

### Guest
```
가능한 작업:
- /create-issue → 이슈 제보만 가능
- /setup → 초기 설정

권한:
 create-issue (제한적)
 setup (초기 설정만)
 designer (거절)
 flow (거절)
 admin (거절)
```

---

## 실행 흐름 (권한 검증)

### 케이스 1: 완전 권한 ()

```
사용자 (developer): "컴포넌트 만들어줄 수 있어?"

Claude:
이 세션에서는 /designer 명령을 사용해서
컴포넌트를 만들겠습니다.

[자동 실행]
───────────────────
프레임워크를 선택해주세요:
...
```

### 케이스 2: 안내 후 진행 ()

```
사용자 (pm): "컴포넌트 만들어줄 수 있어?"

Claude:
컴포넌트 제작은 보통 designer가 담당하는 작업입니다.

그래도 진행하시겠습니까?

[Yes] 계속 진행
[No] 다른 작업 추천
```

**Yes 선택**:
```
이 세션에서는 /designer 명령을 사용해서
컴포넌트를 만들겠습니다.

[자동 실행]
───────────────────
프레임워크를 선택해주세요:
...
```

**No 선택**:
```
현재 역할 [pm]이 주로 하는 작업:
- /flow — 서비스 플로우 설계
- /create-issue — 이슈 제보 (기능 요청)

이 중 어떤 작업을 시작할까요?
```

### 케이스 3: 명확한 거절 ()

```
사용자 (designer): "팀원 추가해줄 수 있어?"

Claude:
죄송합니다. Admin 기능 (/admin)은
admin/developer 역할만 사용 가능합니다.

필요한 권한: admin 또는 developer
현재 역할: designer

현재 역할 [designer]이 할 수 있는 작업:
- /designer — 컴포넌트 제작/수정
- /flow — 서비스 플로우 설계
- /create-issue — 이슈 제보

다른 작업을 도와드릴까요?
```

---

## 의도별 권한 정책

### Designer Intent

```python
if intent == "designer":
 if role in ["admin", "developer", "designer"]:
 # 완전 권한
 print("이 세션에서는 /designer 명령을 사용해서...")
 execute_command("designer")
 elif role == "pm":
 # 안내 후 진행
 if ask_confirmation("컴포넌트 제작은 designer 작업인데, 계속할까?"):
 execute_command("designer")
 else:
 show_recommended_actions("pm")
 else: # guest
 # 거절
 print_permission_denied("designer", role)
```

### Flow Intent

```python
if intent == "flow":
 if role in ["admin", "developer", "designer", "pm"]:
 # 완전 권한 (모든 역할 가능)
 print("이 세션에서는 /flow 명령을 사용해서...")
 execute_command("flow")
 else: # guest
 # 거절
 print_permission_denied("flow", role)
```

### Create-Issue Intent

```python
if intent == "create_issue":
 if role in ["admin", "developer", "designer", "pm"]:
 # 완전 권한
 print("이 세션에서는 /create-issue 명령을 사용해서...")
 execute_command("create_issue")
 else: # guest
 # 거절
 print_permission_denied("create_issue", role)
```

### Admin Intent

```python
if intent == "admin":
 if role in ["admin", "developer"]:
 # 완전 권한
 print("이 세션에서는 /admin 명령을 사용해서...")
 execute_command("admin")
 else: # designer, pm, guest
 # 명확한 거절
 print_permission_denied("admin", role)
```

### Setup Intent

```python
if intent == "setup":
 # 모든 역할 가능
 print("이 세션에서는 /setup 명령을 사용해서...")
 execute_command("setup")
```

---

## 안내 메시지 (권한별)

### 완전 권한 ()

```
이 세션에서는 /designer 명령을 사용해서
Emocog 테마 기반 재사용 가능한 컴포넌트를
만들겠습니다.

[자동 실행]
───────────────────────
프레임워크를 선택해주세요:
...
```

### 안내 후 진행 ()

```
컴포넌트 제작은 보통 designer가 담당하는 작업입니다.

pm이셔도 진행하시겠습니까?

[Yes] 계속 진행
[No] 다른 작업 추천
```

### 명확한 거절 ()

```
죄송합니다. Admin 기능 (/admin)은
admin/developer 역할만 사용 가능합니다.

필요한 권한: admin 또는 developer

현재 역할 [designer]이 할 수 있는 작업:
- /designer — 컴포넌트 제작/수정
- /flow — 플로우 설계
- /create-issue — 이슈 제보

다른 작업을 도와드릴까요?
```

---

## 예제 시나리오

### 시나리오 1: Designer가 Flow 요청 ( 완전 권한)

```
사용자 (designer): "온보딩 플로우 설계해줄 수 있어?"

Claude:
이 세션에서는 /flow 명령을 사용해서
서비스 플로우를 설계하겠습니다.

[자동 실행]
───────────────────────
제품명을 입력하세요: user-onboarding
```

### 시나리오 2: PM이 Component 요청 ( 안내 후 진행)

```
사용자 (pm): "체크박스 컴포넌트 만들어줄 수 있어?"

Claude:
컴포넌트 제작은 보통 designer가 담당하는 작업입니다.

pm이셔도 진행하시겠습니까?

[Yes] 계속 진행
[No] 다른 작업 추천

# Yes 선택 시
이 세션에서는 /designer 명령을 사용해서
체크박스 컴포넌트를 만들겠습니다.

[자동 실행]
───────────────────────
프레임워크를 선택해주세요:

# No 선택 시
현재 역할 [pm]이 주로 하는 작업:
- /flow — 플로우 설계
- /create-issue — 이슈 제보

어떤 작업을 시작할까요?
```

### 시나리오 3: Designer가 Admin 요청 ( 거절)

```
사용자 (designer): "팀원 추가해줄 수 있어?"

Claude:
죄송합니다. Admin 기능 (/admin)은
admin/developer 역할만 사용 가능합니다.

필요한 권한: admin 또는 developer
현재 역할: designer

현재 역할 [designer]이 할 수 있는 작업:
- /designer — 컴포넌트 제작/수정
- /flow — 플로우 설계
- /create-issue — 이슈 제보

다른 작업을 도와드릴까요?
```

### 시나리오 4: PM이 Admin 요청 ( 거절)

```
사용자 (pm): "테마 업데이트해줄 수 있어?"

Claude:
죄송합니다. Admin 기능 (/admin)은
admin/developer 역할만 사용 가능합니다.

필요한 권한: admin 또는 developer
현재 역할: pm

현재 역할 [pm]이 할 수 있는 작업:
- /flow — 플로우 설계
- /create-issue — 이슈 제보

다른 작업을 도와드릴까요?
```

---

## 정리

### 3가지 권한 정책

| 정책 | 대상 | 처리 |
|------|------|------|
| ** 완전 권한** | 역할이 해당 작업을 주로 하는 경우 | 바로 실행 |
| ** 안내 후 진행** | 역할이 다르지만 필요시 할 수 있는 경우 | 확인 후 실행 또는 안내 |
| ** 거절** | Admin 같이 명확한 제약이 있는 경우 | 거절 후 권한 안내 |

### 핵심 원칙

1. **Admin만 엄격함** - designer/pm은 admin 못함
2. **나머지는 유연함** - 다른 역할도 시도 가능하되 안내
3. **사용자 중심** - 거절보다는 안내와 대안 제시

---

## 참고

- [Auto Command Execution](./auto-command-execution.md)
- [Intent Detection](./intent-detection.md)
- [CLAUDE.md - 권한](../../../CLAUDE.md#완료-기준)
