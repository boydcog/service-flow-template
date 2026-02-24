# Changelog

모든 주목할 만한 변경 사항이 이 파일에 문서화됩니다.

형식은 [Keep a Changelog](https://keepachangelog.com/)를 기반으로 합니다.
버전은 [Semantic Versioning](https://semver.org/)을 따릅니다.

---

## [Unreleased]

### Added
- ✨ **상태 추적 시스템** (State Management)
  - `.claude/state/` 디렉토리: 활성 플로우, 메타데이터 추적
  - `.claude/migrations/` 디렉토리: 스키마 버전 관리
  - `_active_flow.txt`: 현재 작업 플로우 추적
  - `_schema_version.txt`: 현재 템플릿 버전 (v1)

- 🔧 **startup.sh 고도화** (320줄 → orchestration_test 패턴 적용)
  - 의존성 감지 (git, gh CLI, brew)
  - git 초기화 + remote 설정 (HTTPS/SSH 폴백)
  - worktree 자동 정리 (잔여 worktree 정리)
  - git pull 재시도 로직 (stash+rebase+pop)
  - 마이그레이션 감지 (스키마 버전 비교)
  - 활성 플로우 복구 (마지막 플로우 상태 로드)
  - 상세한 상태 리포트 (의존성, 프로젝트 상태)

- 📋 **manifests 확장**
  - `admins.yaml`: 관리자 권한 관리 (orchestration_test 패턴)
  - `flow-defaults.yaml`: 플로우 기본값 정의

- 🔐 **admin.py 강화**
  - `admins.yaml` 기반 권한 검증
  - `verify_admin_access()` 함수 추가
  - `load_admins()` 함수 추가

- 📊 **flow.py 상태 추적**
  - `save_active_flow()`: 활성 플로우 저장
  - `load_active_flow()`: 활성 플로우 로드
  - `save_flow_metadata()`: 플로우 메타데이터 저장
  - `load_flow_metadata()`: 플로우 메타데이터 로드
  - 플로우 생성 시 자동 메타데이터 저장

- ⚙️ **settings.json 개선**
  - `bypassPermissions` 모드 활성화 (신뢰 기반 권한)
  - `EnterPlanMode`, `ExitPlanMode` 권한 추가
  - `mcp__*` 와일드카드로 MCP 서버 자유 접근

### Changed
- 🔄 **git pull 재시도 로직**: stash+rebase+pop 패턴 적용
- 📁 **.gitignore 확장**: `.claude/state/`, `.claude/migrations/` 추가

### Improved
- 🚀 **세션 시작 안정성**: 네트워크 장애 복구력 향상
- 🎯 **상태 추적 명확성**: 활성 플로우, 메타데이터로 진행상황 추적
- 🔒 **권한 관리**: admins.yaml 기반 역할 기반 접근 제어 (RBAC)

---

## [v1.0.0] - 2026-02-24

초기 릴리스

### Added
- ✨ Service Flow Template 초기 구조
- 📦 Web/Native 컴포넌트 동기화
- 🎨 Emocog 테마 시스템
- 👥 역할 기반 워크플로우 (admin, designer, pm)
- 🔄 컴포넌트 자동 동기화

---

