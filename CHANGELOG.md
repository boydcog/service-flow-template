# Changelog

모든 주목할 만한 변경 사항이 이 파일에 문서화됩니다.

형식은 [Keep a Changelog](https://keepachangelog.com/)를 기반으로 합니다.
버전은 [Semantic Versioning](https://semver.org/)을 따릅니다.

---

## [Unreleased]

### Added
- **명세 문서 구조화 및 최적화** (2026-02-25)
  - `.claude/spec/` 디렉토리 재구조화 (4개 카테고리)
    - `1-foundation/`: 기초 명세 (permission-model)
    - `2-core-system/`: 핵심 시스템 (intent-detection, auto-command-execution)
    - `3-workflow/`: 워크플로우 (validation-flow, flow-standardization)
    - `4-detection/`: 감지 시스템 (global-feedback-detection)
    - `references/`: 참고 문서 (component-spec, flow-spec, setup-validation)
  - `spec/README.md`: 명세 네비게이션 및 읽기 순서 가이드
  - `spec/DEPENDENCIES.md`: 문서 간 의존성 맵

- **명세 문서 7개 추가** (규격 정의)
  - `intent-detection.md`: 사용자 의도 자동 감지 시스템 (키워드 패턴)
  - `auto-command-execution.md`: 의도 감지 후 자동 명령 실행
  - `permission-model.md`: 3-tier 권한 모델 (완전/안내/거절)
  - `validation-flow.md`: 7단계 검증 및 공유 플로우
  - `flow-standardization.md`: 모든 command의 표준 플로우
  - `global-feedback-detection.md`: 전역 피드백 감지 (신뢰도 시스템)
  - `setup-validation.md`: Setup 프로세스 검증 보고서 (80% 완료)

- **이모지 완전 제거** (CLAUDE.md 정책 준수)
  - 총 508개 이모지 제거 (2단계 처리)
  - 25개 markdown 파일에서 제거
  - 변형 선택자 및 결합 문자까지 정리

- **Phase 2: 구현 완료** (2026-02-25)

  **Phase 2-1: Permission Validation (권한 검증)**
  - `.claude/commands/_common/permission-validation.md`: 권한 검증 가이드 (3단계 프로세스)
  - 모든 command에 표준화된 권한 검증 추가:
    - `designer.md`: admin/developer/designer만 가능
    - `flow.md`: 모든 역할 가능
    - `create-issue.md`: 모든 역할 가능
    - `admin.md`: admin/developer만 가능
    - `setup.md`: 모든 역할 가능
  - 표준화된 권한 메시지 (✅/❌) 적용

  **Phase 2-2: Intent Detection System (의도 자동 감지)**
  - `.claude/hooks/auto-dispatcher.sh`: 의도 감지 엔진 구현
  - 키워드 기반 정규식 패턴 매칭 (2-1-intent-detection.md 기준)
  - 4가지 의도 감지: designer, flow, create-issue, admin
  - 명시적 /command 감지 (우선순위 최상)
  - 권한 기반 거절 메시지

  **Phase 2-3: Auto-Command Execution (자동 실행)**
  - 모든 command에 "이 세션에서는..." 안내 메시지 추가
  - 사용자 입력 없이 명령 자동 실행 준비
  - 직관적 사용자 경험 제공

  **Phase 2-4: Validation Flow (검증 및 공유 플로우)**
  - 모든 command에 7단계 표준 워크플로우 구현
    - Step 1: 선행 조건 확인
    - Step 2: 정보 수집
    - Step 3: 상태 준비
    - Step 4: 작업 수행
    - Step 5: 사용자 검증 요청
    - Step 6: 공유 확인 (PR/로컬 저장)
    - Step 7: 불만/피드백 감지 및 Issue 공유
  - AskUserQuestion 템플릿 표준화
  - PR 자동 생성 및 라벨 매핑

  **Phase 2-5: Global Feedback Detection (전역 피드백 감지)**
  - `.claude/hooks/feedback-detection.sh`: 피드백 감지 시스템
  - 5가지 피드백 유형 감지:
    - 명확한 버그 (confidence: 0.9)
    - 기능 요청 (confidence: 0.8)
    - 개선 제안 (confidence: 0.7)
    - 부정적 의견 (confidence: 0.6)
    - 명시적 피드백 (confidence: 0.5)
  - 신뢰도 기반 Issue 공유 (0.5+ 임계값)
  - 모든 상황에서 감지 (command 실행 중, 일반 대화, 아무 명령도 없을 때)

- **Phase 3: 테스트 완료** (2026-02-25)

  **Phase 3-1: Unit Tests**
  - `.claude/tests/unit-tests.sh`: 단위 테스트
    - Intent detection 테스트 (auto-dispatcher.sh)
    - Permission validation 테스트
    - Feedback detection 테스트 (feedback-detection.sh)
  - 테스트 항목: 5개 이상

  **Phase 3-2: Integration Tests**
  - `.claude/tests/integration-tests.sh`: 통합 테스트
    - 7-step workflow 검증 (Step 1-7)
    - 권한 검증 흐름 테스트
    - Auto-execution 메시지 확인
    - 모든 command 파일 검증
  - 테스트 항목: 15개 이상

  **Phase 3-3: E2E Tests**
  - `.claude/tests/e2e-tests.sh`: 엔드-투-엔드 테스트
    - Designer flow 완전 워크플로우
    - Flow design 워크플로우
    - Bug report 워크플로우
    - Admin task 워크플로우
    - Permission denial 시나리오
    - 다중 피드백 유형 감지 (5가지)
  - 테스트 항목: 20개 이상

### Changed
- **파일 구조 최적화**
  - `.claude/spec/` 다층화 (읽기 순서 명확)
  - `.claude/commands/_common/` 추가 (공통 패턴 모음)
  - `.claude/tests/` 추가 (테스트 파일 위치)

- **PR 템플릿 업데이트**
  - 자동 라벨 매핑 제거
  - 기본 라벨만 사용 (bug, enhancement, documentation, question, etc.)
  - 검증 정보 섹션 추가 (validator, completion date, verification items)

- **Issue 템플릿 업데이트**
  - 자동 라벨 선택 섹션 제거
  - 기본 라벨 정책 적용

- **상태 추적 시스템** (State Management)
 - `.claude/state/` 디렉토리: 활성 플로우, 메타데이터 추적
 - `.claude/migrations/` 디렉토리: 스키마 버전 관리
 - `_active_flow.txt`: 현재 작업 플로우 추적
 - `_schema_version.txt`: 현재 템플릿 버전 (v1)

- **startup.sh 고도화** (320줄 → orchestration_test 패턴 적용)
 - 의존성 감지 (git, gh CLI, brew)
 - git 초기화 + remote 설정 (HTTPS/SSH 폴백)
 - worktree 자동 정리 (잔여 worktree 정리)
 - git pull 재시도 로직 (stash+rebase+pop)
 - 마이그레이션 감지 (스키마 버전 비교)
 - 활성 플로우 복구 (마지막 플로우 상태 로드)
 - 상세한 상태 리포트 (의존성, 프로젝트 상태)

- **manifests 확장**
 - `admins.yaml`: 관리자 권한 관리 (orchestration_test 패턴)
 - `flow-defaults.yaml`: 플로우 기본값 정의

- **admin.py 강화**
 - `admins.yaml` 기반 권한 검증
 - `verify_admin_access()` 함수 추가
 - `load_admins()` 함수 추가

- **flow.py 상태 추적**
 - `save_active_flow()`: 활성 플로우 저장
 - `load_active_flow()`: 활성 플로우 로드
 - `save_flow_metadata()`: 플로우 메타데이터 저장
 - `load_flow_metadata()`: 플로우 메타데이터 로드
 - 플로우 생성 시 자동 메타데이터 저장

- **settings.json 개선**
 - `bypassPermissions` 모드 활성화 (신뢰 기반 권한)
 - `EnterPlanMode`, `ExitPlanMode` 권한 추가
 - `mcp__*` 와일드카드로 MCP 서버 자유 접근

### Changed
- **git pull 재시도 로직**: stash+rebase+pop 패턴 적용
- **.gitignore 확장**: `.claude/state/`, `.claude/migrations/` 추가

### Improved
- **세션 시작 안정성**: 네트워크 장애 복구력 향상
- **상태 추적 명확성**: 활성 플로우, 메타데이터로 진행상황 추적
- **권한 관리**: admins.yaml 기반 역할 기반 접근 제어 (RBAC)

---

## [v1.0.0] - 2026-02-24

초기 릴리스

### Added
- Service Flow Template 초기 구조
- Web/Native 컴포넌트 동기화
- Emocog 테마 시스템
- 역할 기반 워크플로우 (admin, designer, pm)
- 컴포넌트 자동 동기화

---

