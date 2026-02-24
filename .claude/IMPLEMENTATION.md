# Service Flow Template — 지속가능성 개선사항

이 문서는 2026-02-24에 적용된 **Phase 1-3 개선사항**을 설명합니다.

---

## 개요

템플릿의 지속가능성을 위해 다음 5가지 부족했던 부분을 구현했습니다:

1. ✅ **마이그레이션 시스템** (상태 관리)
2. ✅ **Startup 자동화** (세션 시작 시 마이그레이션 자동 실행)
3. ✅ **PR 자동 생성** (변경사항 공유)
4. ✅ **상태 확인 UI** (변경사항 적용 확인)
5. ✅ **Admin 워크플로우** (명령어 통합의 첫 단계)

---

## 📁 새로 추가된 파일

```
.claude/
├── migrations/
│   └── v1-to-v2.sh              ✅ 마이그레이션 스크립트
├── hooks/
│   ├── startup.sh               🔄 개선 (마이그레이션 자동 실행)
│   ├── create-pr.sh             ✅ PR 자동 생성
│   ├── check-status.sh          ✅ 변경사항 확인 UI
│   └── admin-workflow.sh        ✅ Admin 워크플로우
└── IMPLEMENTATION.md            ✅ 이 파일
```

---

## 🔄 Phase 1: 마이그레이션 시스템

### 목적
- **상태 파일 보호**: `.user-identity`, `.gh-token` gitignore 관리
- **로컬 구조 표준화**: 매번 세션 시작 시 일관된 구조 유지
- **자동 마이그레이션**: gitignore 파일 구조 변경 시 자동 대응

### 핵심 파일

#### `.claude/state/_schema_version.txt`
```
v1  ← 현재 버전
```

#### `.claude/migrations/_target_version.txt`
```
v1  ← 목표 버전 (v1과 동일하면 마이그레이션 불필요)
```

#### `.claude/migrations/v1-to-v2.sh`
마이그레이션 스크립트. 다음을 자동 처리:
1. `.user-identity` git skip-worktree 적용
2. `.gh-token` 파일 보호 (권한 설정)
3. `flows/` 디렉토리 초기화
4. `.claude/state/` 정리

### 사용 방법

#### 자동 실행 (권장)
```bash
# 세션 시작 시 자동으로 실행됨
# startup.sh가 마이그레이션 감지 → 자동 실행
```

#### 수동 실행
```bash
bash .claude/migrations/v1-to-v2.sh
```

### 마이그레이션 추가 (v2 → v3)
```bash
# 1. 새 마이그레이션 스크립트 생성
cat > .claude/migrations/v2-to-v3.sh <<EOF
#!/bin/bash
# v2 to v3 마이그레이션
...
EOF

# 2. 목표 버전 업데이트
echo "v3" > .claude/migrations/_target_version.txt

# 3. 다음 세션 시작 시 자동 실행됨
```

---

## ⚙️ Phase 2: Startup 자동화

### 개선사항

기존:
```bash
# 마이그레이션을 감지하지만 실행하지 않음
WARN MIGRATION_NEEDED: v1 → v2
```

개선 후:
```bash
# 마이그레이션을 감지하고 자동 실행
🔄 마이그레이션 감지: v1 → v2
마이그레이션 실행 중...
✅ 마이그레이션 완료
```

### 동작 흐름

```
세션 시작
  ↓
1. 사용자 신원 로드
2. GH 토큰 로드
3. 로컬 파일 보호 (git skip-worktree)
4. Git pull
5. **마이그레이션 감지**
   → 필요하면 자동 실행
6. 컴포넌트 동기화
7. 상태 리포트
```

### 로그 확인
```bash
# 마이그레이션 로그
cat .claude/state/logs/migrations.log

# 출력:
# [2026-02-24 16:55:32] Migration v1→v2 completed
```

---

## 📤 Phase 2+3: PR 자동 생성 & 상태 확인

### 사용 시나리오

#### 시나리오 1: Admin이 팀원 추가 후 PR 생성

```bash
# 1. 템플릿 관리 작업 완료 (파일 수정 등)

# 2. Admin 워크플로우 실행
bash .claude/hooks/admin-workflow.sh \
    "팀원 추가" \
    "홍길동 (designer) 추가" \
    "보이드"

# 출력:
# 🌿 브랜치 생성: admin/1708741600
# 📝 CHANGELOG 업데이트 중...
# ✓ CHANGELOG 업데이트됨
# 📤 변경사항 커밋 중...
# 📝 PR 생성 중: [admin] 보이드: 팀원 추가
# ✅ PR 생성 완료!
# 📍 PR URL: https://github.com/anthropics/service-flow-template/pull/123
```

#### 시나리오 2: 현재 상태 확인

```bash
# 변경사항 적용 상태 확인
bash .claude/hooks/check-status.sh

# 또는 특정 항목만 확인
bash .claude/hooks/check-status.sh --pr       # PR 상태만
bash .claude/hooks/check-status.sh --branch   # 브랜치 상태만
bash .claude/hooks/check-status.sh --local    # 로컬 변경사항만
```

### 파일 상세

#### `.claude/hooks/create-pr.sh`
PR 자동 생성 유틸리티

```bash
# 사용법
bash .claude/hooks/create-pr.sh <branch> <title> [description]

# 예
bash .claude/hooks/create-pr.sh \
    "component/button" \
    "[designer] 박나현: Button 컴포넌트" \
    "새로운 버튼 컴포넌트 추가..."
```

기능:
- ✅ 브랜치 검증
- ✅ GH_TOKEN 로드
- ✅ git push 자동
- ✅ PR 생성
- ✅ PR 링크 표시
- ✅ PR 상태 확인

#### `.claude/hooks/check-status.sh`
변경사항 적용 상태 확인 UI

```bash
# 모든 상태 확인
bash .claude/hooks/check-status.sh

# 출력 예:
# ========================================
# Service Flow Template — 상태 확인
# ========================================
#
# 💾 로컬 변경사항
#
# 최근 커밋:
#   3f7a8c2 admin: 팀원 추가
#   b4d5e1f admin: 테마 업데이트
#   c6f9g2h [designer] 버튼 컴포넌트
#
# 변경 통계:
#  manifests/team.yaml | 2 ++
#  1 file changed, 2 insertions(+)
#
# 🌿 브랜치 상태
#
# 현재 브랜치: admin/1708741600
# 📤 로컬 커밋 (미푸시): 1개
# ✅ main 브랜치와 동기화됨
#
# 📊 PR 상태 확인
#
# PR #123: [admin] 보이드: 팀원 추가 [OPEN]
#
# ✅ 최근 병합된 PR
#
# PR #122: [designer] 박나현: Button 컴포넌트 (병합: 2026-02-24)
#
# 🔄 마이그레이션 상태
#
# 현재 스키마: v1
# 목표 스키마: v1
# ✅ 스키마가 최신 버전입니다
```

#### `.claude/hooks/admin-workflow.sh`
Admin 작업 자동화 (브랜치 생성 → 커밋 → PR 생성)

```bash
bash .claude/hooks/admin-workflow.sh <action> <description> [user]

# 예
bash .claude/hooks/admin-workflow.sh \
    "팀원 추가" \
    "홍길동 (designer) 추가" \
    "보이드"
```

기능:
- ✅ 브랜치 자동 생성
- ✅ CHANGELOG 업데이트
- ✅ 파일 커밋
- ✅ PR 자동 생성
- ✅ 액션 로그 기록

---

## 🎯 사용 흐름 (Admin 예시)

### Before (이전)
```
1. 파일 수정 (직접 main 브랜치)
2. git add / commit / push (수동)
3. GitHub에서 PR 생성 (수동)
4. 병합 확인 (GitHub 진입)
5. 로컬 pull (수동)
```

❌ **문제**:
- GitHub 직접 진입 필요
- 변경사항 적용 여부 확인 어려움
- 반복 작업 수동

### After (개선)
```
1. 파일 수정
2. bash .claude/hooks/admin-workflow.sh "설명" "작성자"
3. bash .claude/hooks/check-status.sh  # 상태 확인
4. 세션 시작 시 자동으로 최신 상태 동기화
```

✅ **이점**:
- GitHub 직접 진입 불필요
- CLI에서 상태 확인 가능
- 자동화된 워크플로우
- 매 세션 시작 시 자동 적용

---

## 🚀 다음 단계 (Phase 4)

### 아직 구현되지 않은 부분

1. **Designer 명령어 실행 자동화**
   - `/designer` 명령 후 자동 PR 생성
   - Storybook 자동 검증

2. **Flow 명령어 실행 자동화**
   - `/flow` 명령 후 자동 PR 생성
   - Dev 서버 자동 검증

3. **명령어 자동 감지 (Intent Detection)**
   - 사용자 요청 분석 → 적절한 스킬 자동 실행
   - CLAUDE.md의 "요청 패턴 → 자동 실행" 구현

### 추가 마이그레이션 (v1 → v2 → v3)

나중에 파일 구조 변경 시:
```bash
# v2 → v3 마이그레이션 추가
cat > .claude/migrations/v2-to-v3.sh <<EOF
#!/bin/bash
# 새로운 구조로 업데이트
EOF

echo "v3" > .claude/migrations/_target_version.txt
```

---

## 📋 체크리스트

설정 확인:

- [ ] `.claude/migrations/v1-to-v2.sh` 실행 가능 (755)
- [ ] `.claude/hooks/startup.sh` 마이그레이션 부분 개선됨
- [ ] `.claude/hooks/create-pr.sh` 실행 가능
- [ ] `.claude/hooks/check-status.sh` 실행 가능
- [ ] `.claude/hooks/admin-workflow.sh` 실행 가능
- [ ] `GH_TOKEN` 설정됨
- [ ] `.user-identity` 파일 보호됨
- [ ] 첫 실행 시 마이그레이션 자동 실행됨

---

## 🔗 관련 파일

- `.claude/CLAUDE.md` — 주 설정 파일 (프로젝트 지시사항)
- `.claude/manifests/` — 역할, 팀, 테마 정의
- `.claude/state/` — 런타임 상태 파일
- `CHANGELOG.md` — 변경 이력

---

## 💡 팁

### 디버깅

```bash
# 마이그레이션 로그 보기
tail -f .claude/state/logs/migrations.log

# PR 이력 보기
cat .claude/state/logs/pr-history.log

# Admin 액션 이력 보기
cat .claude/state/logs/admin-actions.log
```

### 수동 마이그레이션 강제 실행

```bash
# 현재 버전을 이전 버전으로 변경
echo "v1" > .claude/state/_schema_version.txt

# 다음 명령어로 마이그레이션 강제 실행
bash .claude/migrations/v1-to-v2.sh
```

---

## ❓ FAQ

### Q: PR 생성 시 "GitHub 토큰을 찾을 수 없습니다" 오류

**A**: `.gh-token` 파일이 없거나 비어있습니다.
```bash
# /setup 명령으로 설정하거나
echo "your-github-token" > .claude/.gh-token
chmod 600 .claude/.gh-token
```

### Q: 마이그레이션이 자동으로 실행되지 않음

**A**: `.claude/migrations/_target_version.txt`의 버전을 확인하세요.
```bash
# 현재 버전
cat .claude/state/_schema_version.txt

# 목표 버전
cat .claude/migrations/_target_version.txt

# 다르면 마이그레이션이 필요합니다
```

### Q: Admin 워크플로우로 여러 파일을 수정했는데 일부만 커밋됨

**A**: `admin-workflow.sh`는 `git add -A`로 모든 변경사항을 커밋합니다. 선택적 커밋이 필요하면 수동으로 진행하세요:
```bash
# 수동 진행
git add manifests/team.yaml
git commit -m "admin: 팀원 추가"
bash .claude/hooks/create-pr.sh admin/xxxxx "[admin] 보이드: 팀원 추가"
```

---

## 📞 문제 해결

모든 스크립트는 `set -euo pipefail`으로 설정되어 있어 에러 발생 시 즉시 중단됩니다.

문제 시:
1. 스크립트 로그 확인
2. `.claude/state/logs/` 로그 파일 확인
3. `git status` 확인
4. 수동으로 각 단계 실행

---

마지막 수정: 2026-02-24
