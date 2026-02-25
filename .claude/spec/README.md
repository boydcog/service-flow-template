# Claude Code 명세 문서 가이드

## 개요

이 디렉토리는 Service Flow Template의 모든 명세 문서를 체계적으로 구성합니다.

---

## 읽는 순서 (추천)

### 1단계: 기초 이해 (1-foundation/)
먼저 기초부터 시작하세요.

1. **1-1-permission-model.md** — 권한 모델 (3-tier 시스템)
   - 모든 명세의 기초
   - 어떤 역할이 어떤 작업을 할 수 있는가?

2. **1-2-setup-process.md** — Setup 프로세스 (참고: ../commands/setup.md)
   - 사용자 신원 정보 수집
   - 권한 초기화

---

### 2단계: 핵심 시스템 (2-core-system/)
기초를 이해한 후 핵심 시스템을 학습하세요.

1. **2-1-intent-detection.md** — 의도 자동 감지
   - 사용자 메시지에서 의도 인식
   - 키워드 패턴 매칭

2. **2-2-auto-command-execution.md** — 자동 명령 실행
   - 의도 감지 후 자동 실행
   - 사용자 입력 단계 건너뜀

---

### 3단계: 워크플로우 (3-workflow/)
실제 작업 흐름을 이해하세요.

1. **3-1-validation-flow.md** — 검증 및 공유 플로우
   - 개발 완료 후 사용자 검증
   - PR 생성 및 공유

2. **3-2-flow-standardization.md** — 7단계 표준 플로우
   - 모든 command의 공통 구조
   - AskUserQuestion 템플릿 표준화

---

### 4단계: 감지 시스템 (4-detection/)
고급 기능을 학습하세요.

1. **4-1-global-feedback-detection.md** — 전역 피드백 감지
   - 어디서나 사용자 불만 감지
   - 신뢰도 시스템 (0.6 임계값)

---

### 참고 문서 (references/)

- **setup-validation.md** — Setup 검증 보고서 (참고용)
- **component-spec.md** — 컴포넌트 작성 규칙
- **flow-spec.md** — 플로우 설계 규칙

---

## 의존성 맵

```
1-foundation/
├── 1-1-permission-model.md (기초)
└── 1-2-setup-process.md (기초)
    ↓
2-core-system/
├── 2-1-intent-detection.md (의도 감지)
│   └─ 참조: permission-model.md
├── 2-2-auto-command-execution.md (자동 실행)
│   └─ 참조: intent-detection.md, permission-model.md
    ↓
3-workflow/
├── 3-1-validation-flow.md (검증 플로우)
│   └─ 참조: permission-model.md, auto-command-execution.md
├── 3-2-flow-standardization.md (표준화)
│   └─ 참조: validation-flow.md, permission-model.md
    ↓
4-detection/
└── 4-1-global-feedback-detection.md (피드백 감지)
    └─ 참조: validation-flow.md, permission-model.md
```

---

## 구현 순서

### Phase 1: 기초 구현
1. Permission Validation 로직 (각 command에 추가)
2. Role-based access control

### Phase 2: 자동화 구현
1. Intent Detection 시스템 (auto-dispatcher.sh)
2. Auto-Command Execution 로직
3. Keyword matching 정규식

### Phase 3: 워크플로우 구현
1. Validation Flow 적용 (5-7단계)
2. AskUserQuestion 템플릿 표준화
3. PR 자동 생성

### Phase 4: 감지 시스템 구현
1. Global Feedback Detection
2. Confidence scoring 시스템
3. Issue 공유 플로우

### Phase 5: 테스트
1. Unit 테스트 (각 기능별)
2. Integration 테스트 (워크플로우)
3. E2E 테스트 (전체 플로우)

---

## 각 명세 사용처

| 명세 | 위치 | 참조처 | 용도 |
|------|------|--------|------|
| permission-model.md | 2-core-system | 모든 command | 권한 검증 |
| intent-detection.md | 2-core-system | auto-dispatcher.sh | 의도 감지 |
| auto-command-execution.md | 2-core-system | 모든 command | 자동 실행 |
| validation-flow.md | 3-workflow | designer, flow, create-issue | 검증 플로우 |
| flow-standardization.md | 3-workflow | 모든 command | 구조 표준화 |
| global-feedback-detection.md | 4-detection | 모든 command | 피드백 감지 |

---

## 빠른 참조

**"의도 감지는 어디에?"**
→ `2-core-system/2-1-intent-detection.md`

**"권한 검증은?"**
→ `1-foundation/1-1-permission-model.md`

**"검증 플로우는?"**
→ `3-workflow/3-1-validation-flow.md`

**"피드백 감지는?"**
→ `4-detection/4-1-global-feedback-detection.md`

---

## 문서 업데이트 규칙

- 명세 수정 시 의존하는 다른 문서도 함께 검토
- DEPENDENCIES.md 업데이트
- CHANGELOG.md에 기록

---

**마지막 업데이트**: 2026-02-25
**상태**: Phase 1 (명세 작성 완료) → Phase 2 (구현 예정)
