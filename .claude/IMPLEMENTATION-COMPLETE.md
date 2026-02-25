# Service Flow Template — 구현 완료

**2026-02-24 완료**

## 구현된 기능

### 1. 마이그레이션 시스템
- `migrations/v1-to-v2.sh` - 자동 마이그레이션 스크립트
- `startup.sh` - 세션 시작 시 마이그레이션 자동 실행
- `state/_schema_version.txt` - 스키마 버전 관리

### 2. 권한 검증 시스템 (NEW!)
- `hooks/verify-permissions.sh` - 권한 검증 유틸
- `startup.sh` - roles.yaml 자동 로드
- 역할별 권한 정의 (team.yaml, roles.yaml)

### 3. PR 자동 생성
- `hooks/create-pr.sh` - PR 생성 유틸
- `hooks/admin-workflow.sh` - Admin 작업 자동화
- GitHub CLI 통합

### 4. 상태 확인 UI
- `hooks/check-status.sh` - 변경사항 확인 (CLI)
- `/admin-status` 스킬 - GitHub 진입 없이 상태 확인

### 5. 자동 동기화
- git pull (템플릿 + 컴포넌트 라이브러리 동기화)
- 권한 자동 적용
- Admin 변경사항 즉시 반영

---

## 동기화 흐름

### Admin의 변경사항 → 팀 전체 자동 반영

```
Timeline:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Admin Session:
 1. /admin 실행
 2. team.yaml 수정 (홍길동 추가)
 3. roles.yaml 수정 (권한 변경)
 4. /admin-workflow 실행 → PR 생성 → 병합

Designer Session (5분 후):
 1. 세션 시작 → startup.sh 실행
 2. git pull (변경사항 가져옴)
 3. load team.yaml (홍길동 인식)
 4. load roles.yaml (권한 설정)
 5. verify_permissions() (권한 검증)
 6. Intent Detection ("/admin" 가능 여부 판단)
```

---

## 공유 vs 독립

### Git에 추적 (자동 동기화 )
```
.claude/
├── commands/ # Skill 정의
├── hooks/ # 자동화 스크립트
├── manifests/
│ ├── team.yaml # Admin이 관리
│ ├── roles.yaml # Admin이 관리
│ └── theme.yaml # Admin이 관리
├── spec/ # 규칙 정의
└── migrations/ # 마이그레이션

components/
├── web/ui/ # 공유 컴포넌트
└── native/ui/ # 공유 컴포넌트
```

### Git에서 무시 (프로젝트별 독립 )
```
flows/ # 프로젝트별 플로우
projects/ # 프로젝트 코드
.claude/state/ # 로컬 상태
.user-identity # 로컬 설정
.gh-token # 로컬 토큰
```

---

## 검증 결과

모든 테스트 통과:
```
Admin 역할 (6개 스킬) : 6/6 통과
Developer 역할 (6개 스킬) : 6/6 통과
Designer 역할 (6개 스킬) : 6/6 통과 (admin 불가)
PM 역할 (6개 스킬) : 6/6 통과 (admin, designer 불가)

합계: 24/24 (100%)
```

---

## 새로 추가된 파일

```
.claude/
├── ARCHITECTURE.md # 아키텍처 설명
├── IMPLEMENTATION-COMPLETE.md # 이 파일
├── commands/
│ ├── admin.md (개선) # 스킬 정의
│ └── admin-status.md (신규) # 상태 확인 스킬
├── hooks/
│ ├── startup.sh (개선) # 권한 로드 추가
│ ├── admin-workflow.sh # Admin 자동화
│ ├── create-pr.sh # PR 생성
│ ├── check-status.sh # 상태 확인
│ ├── verify-permissions.sh # 권한 검증 ⭐
│ └── test-permissions.sh # 권한 테스트 ⭐
└── migrations/
 └── v1-to-v2.sh # 마이그레이션

.gitignore (개선) # 프로젝트별 무시 규칙 명확화
```

---

## 사용 방법

### Admin이 팀원 추가

```bash
# 1. Admin: team.yaml 수정
/admin
# → "2. 팀원 관리" 선택
# → .claude/manifests/team.yaml 편집

# 2. 자동으로 PR 생성 및 병합

# 3. 다른 팀원 세션 시작 시 자동 적용 
```

### Designer가 컴포넌트 생성

```bash
/designer
# → 컴포넌트 생성 → PR → 병합

# 다른 팀원 세션 시작 시 자동 동기화 
```

### PM이 변경사항 확인 (GitHub 진입 없이)

```bash
/admin-status

# 또는
bash .claude/hooks/check-status.sh --pr # PR 상태만
bash .claude/hooks/check-status.sh --local # 로컬 변경사항만
```

---

## 핵심 특징

### 1. "껍데기만 공유"
- 템플릿 (CLAUDE.md, spec/) 공유
- 규칙 (component-spec.md, roles.yaml) 공유
- 컴포넌트 라이브러리 공유
- 프로젝트 구현 독립

### 2. "Admin 변경 → 팀 전체 자동 반영"
- Admin이 team.yaml 수정 → PR → 병합
- 다른 팀원 세션 시작 → 자동 동기화 
- 권한 자동 적용 

### 3. "각 프로젝트는 독립"
- flows/ (프로젝트별 플로우) - git 무시
- projects/ (프로젝트 코드) - git 무시
- Agent Team 설정 - git 무시

---

## 아키텍처

```
┌─────────────────────────────────────┐
│ Public Template (GitHub) │
│ CLAUDE.md (규칙) │
│ component-spec.md (규칙) │
│ team.yaml (Admin 관리) │
│ roles.yaml (권한 정의) │
│ components/ (라이브러리) │
│ migrations/ (마이그레이션) │
└─────────────────────────────────────┘
 ↓ (git pull)
 ↓ (자동 동기화)
┌─────────────────────────────────────┐
│ 각 팀원의 로컬 환경 │
│ .user-identity (로컬) │
│ .gh-token (로컬) │
│ flows/ (프로젝트별, 무시) │
│ projects/ (프로젝트, 무시) │
│ roles 자동 로드 │
│ 권한 자동 검증 │
└─────────────────────────────────────┘
 ↓ (로컬 작업)
┌─────────────────────────────────────┐
│ 프로젝트별 독립 개발 │
│ - flows/product-a/ (로컬) │
│ - projects/product-a/ (로컬) │
│ - Agent Team 설정 (로컬) │
│ → 다른 프로젝트 영향 없음 │
└─────────────────────────────────────┘
 ↓ (push)
┌─────────────────────────────────────┐
│ GitHub (PR 리뷰 & 병합) │
│ 프로젝트 코드는 git 무시 │
│ 템플릿만 공유 │
└─────────────────────────────────────┘
```

---

## 테스트 방법

### 권한 검증 테스트 실행

```bash
bash .claude/hooks/test-permissions.sh

# 결과:
# 모든 테스트 통과!
# 통과: 24 / 24 (100%)
```

### 권한 수동 검증

```bash
# Admin 역할이 /admin 사용 가능?
bash .claude/hooks/verify-permissions.sh admin admin
# 권한 확인: /admin 사용 가능 (역할: admin)

# Designer 역할이 /admin 사용 가능?
bash .claude/hooks/verify-permissions.sh admin designer
# 권한 없음 (필요 역할: admin developer, 현재 역할: designer)
```

---

## 체크리스트

구현 완료:
- [x] 마이그레이션 시스템
- [x] 권한 검증 시스템
- [x] PR 자동 생성
- [x] 상태 확인 UI
- [x] Admin 자동 적용
- [x] 프로젝트 독립성
- [x] 전체 테스트 (24/24 통과)

---

## 결론

이제 **완전한 템플릿 시스템**이 완성되었습니다:

1. Admin의 변경사항 → 팀 전체 자동 적용
2. Designer의 컴포넌트 → 팀 전체 자동 동기화
3. 각 프로젝트는 독립적으로 개발
4. 모든 권한 자동 검증
5. GitHub 진입 없이 상태 확인

**"껍데기는 공유, 구현은 독립, Admin 변경은 자동 반영"**

---

최종 수정: 2026-02-24
구현 상태: 완료
테스트: 24/24 통과
