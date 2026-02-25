# 명세 문서 의존성 맵

## 의존성 다이어그램

```
┌──────────────────────────────────────────────────────────────────┐
│                  기초 (1-Foundation)                             │
│      1-1-permission-model.md (모든 것의 기초)                    │
└───────────────┬────────────────────────────────────────────────┘
                │
                ├──────────────────────────────────────┐
                │                                      │
                ↓                                      ↓
    ┌───────────────────────────┐    ┌──────────────────────────┐
    │   핵심 시스템              │    │  참고/학습               │
    │ (2-core-system)           │    │ references/setup-valid.md
    └─────────┬─────────────────┘    └──────────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
    ↓                   ↓
┌──────────────────┐ ┌──────────────────────────────┐
│ 2-1-intent-      │ │ 2-2-auto-command-           │
│ detection        │ │ execution                   │
│ (의도 감지)      │ │ (자동 실행)                 │
│ 의존:            │ │ 의존:                       │
│ - permission     │ │ - 2-1-intent-detection     │
│   -model         │ │ - permission-model          │
└────────┬────────┘ └───────┬────────────────────┘
         │                  │
         └────────┬─────────┘
                  │
                  ↓
    ┌─────────────────────────────┐
    │   워크플로우 (3-workflow)    │
    │    위 2개를 조합해서 사용    │
    └─────────────┬───────────────┘
                  │
    ┌─────────────┴─────────────┐
    │                           │
    ↓                           ↓
┌──────────────────────┐ ┌─────────────────────┐
│ 3-1-validation-flow  │ │ 3-2-flow-standard   │
│ (검증 플로우)        │ │ (7단계 표준)        │
│ 의존:                │ │ 의존:               │
│ - auto-execution     │ │ - validation-flow   │
│ - permission-model   │ │ - permission-model  │
└──────────┬───────────┘ └─────────┬──────────┘
           │                       │
           └───────────┬───────────┘
                       │
                       ↓
    ┌────────────────────────────────────┐
    │ 감지 시스템 (4-detection)          │
    │ 4-1-global-feedback-detection     │
    │ (피드백 감지)                      │
    │ 의존:                              │
    │ - validation-flow                  │
    │ - flow-standardization             │
    │ - permission-model                 │
    └────────────────────────────────────┘
```

---

## 문서별 의존성 상세

### 1-foundation/

#### 1-1-permission-model.md
- **역할**: 권한 시스템의 기초
- **의존성**: 없음 (독립적)
- **참조처**:
  - 2-1-intent-detection.md
  - 2-2-auto-command-execution.md
  - 3-1-validation-flow.md
  - 3-2-flow-standardization.md
  - 4-1-global-feedback-detection.md
  - 모든 command (designer, flow, admin, create-issue)

---

### 2-core-system/

#### 2-1-intent-detection.md
- **역할**: 사용자 의도 자동 인식
- **의존성**:
  - permission-model.md (권한 검증 규칙)
- **참조처**:
  - 2-2-auto-command-execution.md
  - auto-dispatcher.sh (구현)
  - intent-detection.test.sh (테스트)

#### 2-2-auto-command-execution.md
- **역할**: 의도 감지 후 자동 실행
- **의존성**:
  - 2-1-intent-detection.md (의도 감지)
  - permission-model.md (권한 검증)
- **참조처**:
  - 모든 command 시작 단계
  - 3-1-validation-flow.md

---

### 3-workflow/

#### 3-1-validation-flow.md
- **역할**: 검증 및 공유 플로우 (7단계 중 5-7단계)
- **의존성**:
  - permission-model.md (권한 정보)
  - 2-2-auto-command-execution.md (자동 실행)
- **참조처**:
  - designer.md (Step 5-7)
  - flow.md (Step 5-7)
  - create-issue.md
  - 3-2-flow-standardization.md
  - 4-1-global-feedback-detection.md

#### 3-2-flow-standardization.md
- **역할**: 모든 command의 7단계 표준 플로우
- **의존성**:
  - 3-1-validation-flow.md (검증 플로우)
  - permission-model.md (권한 정보)
- **참조처**:
  - 모든 command 구조 정의
  - 4-1-global-feedback-detection.md

---

### 4-detection/

#### 4-1-global-feedback-detection.md
- **역할**: 전역 피드백 감지 및 Issue 공유
- **의존성**:
  - 3-1-validation-flow.md (Issue 공유 플로우)
  - 3-2-flow-standardization.md (7단계 구조)
  - permission-model.md (권한 정보)
- **참조처**:
  - 모든 command 마지막 단계 (Step 7)
  - feedback-detection.test.sh (테스트)

---

## 구현 체크리스트

### Phase 1: 기초 (Permission Model)
- [ ] permission-model.md 읽기
- [ ] permission-model.py 구현 (권한 검증 로직)
- [ ] 각 command에 permission-validation.md 추가

### Phase 2: 의도 감지 (Intent Detection)
- [ ] 2-1-intent-detection.md 읽기
- [ ] intent-detection-rules.md 작성 (정규식 패턴)
- [ ] auto-dispatcher.sh 구현
- [ ] intent-detection.test.sh 작성

### Phase 3: 자동 실행 (Auto-Command Execution)
- [ ] 2-2-auto-command-execution.md 읽기
- [ ] 각 command 시작 시 "이 세션에서는..." 추가
- [ ] Skill 자동 호출 로직 구현

### Phase 4: 검증 플로우 (Validation Flow)
- [ ] 3-1-validation-flow.md 읽기
- [ ] designer.md, flow.md에 Step 5-7 구현
- [ ] AskUserQuestion 템플릿 표준화

### Phase 5: 피드백 감지 (Feedback Detection)
- [ ] 4-1-global-feedback-detection.md 읽기
- [ ] feedback-detection.py 구현 (신뢰도 계산)
- [ ] 모든 command에 피드백 감지 로직 추가

### Phase 6: 테스트
- [ ] intent-detection.test.sh 실행
- [ ] permission-validation.test.sh 실행
- [ ] feedback-detection.test.sh 실행
- [ ] e2e.test.sh 실행

---

## 상호 참조 규칙

각 문서에서 다른 문서를 참조할 때:

1. **같은 레벨**: `../sibling.md`
2. **부모 레벨**: `../../README.md`
3. **자식 레벨**: `subdir/child.md`

### 예시:
```markdown
자세한 내용은 [Permission Model](../1-foundation/1-1-permission-model.md)을 참조하세요.
```

---

## 문서 수정 시 확인 사항

문서를 수정할 때마다 다음을 확인하세요:

1. **의존하는 문서 업데이트**
   - 이 문서를 참조하는 다른 문서들이 있나?
   - 그 문서들도 함께 수정이 필요한가?

2. **이 문서가 의존하는 내용 확인**
   - 기초 문서의 내용이 변했으면, 이 문서도 반영해야 한다

3. **CHANGELOG 업데이트**
   - 모든 변경사항을 CHANGELOG.md에 기록

### 예: permission-model.md를 수정할 때
1. 다음 문서들도 검토:
   - 2-1-intent-detection.md
   - 2-2-auto-command-execution.md
   - 3-1-validation-flow.md
   - 모든 command 파일
2. CHANGELOG에 기록

---

## 최종 구조

```
.claude/spec/
├── README.md                    (이 README)
├── DEPENDENCIES.md              (의존성 맵)
├── 1-foundation/
│   ├── 1-1-permission-model.md
│   └── 1-2-setup-process.md (예정)
├── 2-core-system/
│   ├── 2-1-intent-detection.md
│   └── 2-2-auto-command-execution.md
├── 3-workflow/
│   ├── 3-1-validation-flow.md
│   └── 3-2-flow-standardization.md
├── 4-detection/
│   └── 4-1-global-feedback-detection.md
└── references/
    ├── setup-validation.md
    ├── component-spec.md
    └── flow-spec.md
```

---

**마지막 업데이트**: 2026-02-25
**상태**: 의존성 맵 완성, Phase 2 (구현) 준비 완료
