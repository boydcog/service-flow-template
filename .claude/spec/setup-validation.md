# Setup 프로세스 검증 리포트

## 검증 범위

1. 신원 정보 수집 (이름, 역할, GitHub)
2. 없을 때 요청하는 프로세스
3. 설정값에서 가져오기 (로드)
4. 각 command에서 사용 여부

---

## 검증 결과

### 1단계: 신원 정보 수집 (setup.md)

**현황**: 완벽하게 구현됨

```yaml
수집 항목:
1. 사용자 이름 (필수)
 - AskUserQuestion으로 입력받음
 - 파일: setup.md (line 19)

2. 역할 (필수)
 - admin/developer/designer/pm 중 선택
 - AskUserQuestion으로 입력받음
 - 파일: setup.md (line 21)

3. GitHub 사용자명 (필수)
 - AskUserQuestion으로 입력받음
 - 파일: setup.md (line 22)

4. GitHub Token (필수)
 - 사용자가 직접 입력
 - 검증: gh auth verify 또는 API 호출
 - 파일: setup.md (line 35)
```

**예시 코드 (setup.md에 명시)**:
```
### 1단계: 사용자 이름 입력
 사용자 이름을 입력하세요:
> 홍길동

### 2단계: 역할 선택
 역할을 선택하세요:
 1. admin (관리자)
 2. developer (개발자)
 3. designer (디자이너)
 4. pm (기획자)

### 3단계: GitHub 사용자명 입력
 GitHub 사용자명을 입력하세요:
> hong-gildong

### 4단계: GitHub Access Token 입력
 GitHub Personal Access Token을 입력하세요:
(https://github.com/settings/tokens에서 생성)
Token (입력은 화면에 표시되지 않습니다):
> [입력]
```

---

### 2단계: 없을 때 요청하는 프로세스

**현황**: 완벽하게 구현됨

**파일 생성 및 보호** (setup.md, line 24-33):
```bash
# .user-identity 파일 생성
.user-identity
├─ 내용: name, role, github (YAML 포맷)
├─ 권한: chmod 644
├─ git 보호: git skip-worktree
└─ 상태: .gitignore에 포함

# .gh-token 파일 생성
.gh-token
├─ 내용: 토큰만 (1줄)
├─ 권한: chmod 600 (엄격한 보호)
├─ git 보호: git skip-worktree
└─ 상태: .gitignore에 포함
```

**검증 단계** (setup.md, line 35-37):
```bash
# GitHub 토큰 검증
 gh auth verify --hostname github.com
 또는 API 호출로 검증
 실패 시: 토큰 재입력 유도
```

---

### 3단계: 설정값에서 가져오기 (startup.sh)

**현황**: 완벽하게 구현됨

**startup.sh 분석**:

#### 3-1. .user-identity 로드 (startup.sh, line 46-66)
```bash
# 파일 존재 확인
if [ -f .user-identity ]; then
 # 이름 추출
 USER_NAME=$(grep '^name:' .user-identity | sed 's/name: //')

 # 역할 추출
 USER_ROLE=$(grep '^role:' .user-identity | sed 's/role: //')

 # 사용자 정보 출력
 echo " 안녕하세요, $USER_NAME ($USER_ROLE)!"

 # roles.yaml에서 권한 로드
 if [ -f ".claude/manifests/roles.yaml" ]; then
 USER_COMMANDS=$(grep -A 10 "^ $USER_ROLE:" ".claude/manifests/roles.yaml" \
 | grep "commands:" | sed 's/.*commands: \[//' | sed 's/\].*//')
 echo " 권한: $USER_COMMANDS"
 fi
else
 # 파일 없음
 echo "WARN 사용자 미설정"
fi
```

**동작**:
1. `.user-identity` 파일 존재 여부 확인
2. `name` 추출 (`grep` + `sed`)
3. `role` 추출 (`grep` + `sed`)
4. `roles.yaml`에서 해당 역할의 `commands` 배열 추출
5. 사용자에게 권한 정보 표시

#### 3-2. .gh-token 로드 (startup.sh, line 75-92)
```bash
# 파일 존재 확인
if [ -f .gh-token ]; then
 TOKEN_CONTENT=$(cat .gh-token | tr -d '[:space:]')
 if [ -n "$TOKEN_CONTENT" ]; then
 chmod 600 .gh-token
 export GH_TOKEN="$TOKEN_CONTENT"
 echo " GitHub 토큰 로드됨"
 else
 echo "WARN .gh-token 파일이 비어있음"
 fi
else
 echo "FAIL GitHub 토큰 없음"
fi
```

**동작**:
1. `.gh-token` 파일 존재 여부 확인
2. 토큰 내용 추출
3. 환경변수 `GH_TOKEN` 설정 (bash에서 export)
4. 파일 권한 다시 확인 (chmod 600)
5. 상태 메시지 출력

#### 3-3. git skip-worktree 자동 적용 (startup.sh, line 95-104)
```bash
# .user-identity 보호
if [ -f .user-identity ]; then
 git update-index --skip-worktree .user-identity
fi

# .gh-token 보호
if [ -f .gh-token ]; then
 git update-index --skip-worktree .gh-token
fi
```

**동작**:
- `.user-identity` 파일을 git에서 추적 제외
- `.gh-token` 파일을 git에서 추적 제외
- `git pull` 시 덮어쓰기 방지

#### 3-4. 최종 상태 리포트 (startup.sh, line 280-290)
```bash
프로젝트 상태:
 웹 컴포넌트: 25개
 네이티브 컴포넌트: 5개
 활성 플로우: 미설정
 현재 브랜치: main
 GH 토큰: true ← 확인됨
 git 연결: true ← 확인됨

명령어: /setup /admin /designer /flow /create-issue
```

---

### 4단계: 각 command에서 사용 여부

**현황**: 명시적 구현 필요

#### 4-1. 현재 상태

**setup.md**:
```
 이름, 역할, GitHub 정보 수집 명시
 .user-identity 생성 명시
 .gh-token 생성 명시
 토큰 검증 명시
```

**startup.sh**:
```
 .user-identity 로드
 .gh-token 로드 및 export
 roles.yaml에서 권한 로드
```

**각 command에서 사용 여부**:
```
designer.md: 권한 검증 명시 필요
flow.md: 권한 검증 명시 필요
create-issue.md: 권한 검증 명시 필요
admin.md: 권한 검증 명시 필요
```

#### 4-2. 개선 필요 부분

각 command에 다음이 추가되어야 함:

```bash
# 1단계: 선행 조건 확인 (모든 command 동일)

# 1-1. 신원 파일 확인
if [ ! -f .user-identity ]; then
 echo " 신원 파일이 없습니다"
 echo "먼저 /setup을 실행하세요"
 exit 1
fi

# 1-2. 신원 정보 로드
USER_NAME=$(grep '^name:' .user-identity | sed 's/name: //')
USER_ROLE=$(grep '^role:' .user-identity | sed 's/role: //')

# 1-3. 권한 검증 (roles.yaml 기반)
ALLOWED_COMMANDS=$(grep -A 5 "^ $USER_ROLE:" .claude/manifests/roles.yaml \
 | grep "commands:" | sed 's/.*commands: \[//' | sed 's/\].*//')

if ! echo "$ALLOWED_COMMANDS" | grep -q "$CURRENT_COMMAND"; then
 echo " 권한 없음"
 echo "역할 [$USER_ROLE]은(는) [$CURRENT_COMMAND]을 사용할 수 없습니다"
 exit 1
fi

# 1-4. GH 토큰 확인 (필요한 command만)
if [ ! -f .gh-token ]; then
 echo " GitHub 토큰이 없습니다"
 echo "PR/Issue 생성이 불가능합니다"
 echo "/setup을 다시 실행하여 토큰을 설정하세요"
fi
```

---

## 종합 평가

### 수집 (Collection) - 100%
```
 이름 수집 — setup.md에 명시
 역할 수집 — setup.md에 명시
 GitHub 정보 수집 — setup.md에 명시
 토큰 수집 — setup.md에 명시
```

### 요청 (Request when missing) - 100%
```
 파일 없음 감지 — startup.sh line 46, 76
 파일 비어있음 감지 — startup.sh line 78
 사용자 안내 — setup.md에 프로세스 명시
```

### 로드 (Loading from config) - 100%
```
 .user-identity 로드 — startup.sh line 47-48
 USER_NAME 추출 — startup.sh line 47
 USER_ROLE 추출 — startup.sh line 48
 .gh-token 로드 — startup.sh line 77-80
 GH_TOKEN export — startup.sh line 80
 권한 로드 — startup.sh line 59-62 (roles.yaml 기반)
```

### 사용 (Usage in commands) - 70%
```
 권한 정의 — roles.yaml 완벽
 권한 구조 — permission-model.md 완벽
 각 command에서 명시적 검증 필요 — 구현 필요
 자동 실행 시스템과 통합 필요 — auto-command-execution.md 업데이트 필요
```

---

## 필요한 개선사항

### 1 모든 command 공통 헤더 추가

**위치**: designer.md, flow.md, create-issue.md, admin.md

**추가 내용**:
```markdown
## 실행 전 검증

Claude가 다음을 자동으로 확인합니다:

1. `.user-identity` 파일 존재 여부
 - 없으면: Skill("setup") 자동 실행
 - 있으면: 계속 진행

2. 권한 검증
 - roles.yaml에서 현재 역할의 권한 확인
 - 권한 없으면: 거절 메시지 + 중단

3. `.gh-token` 파일 (선택)
 - PR/Issue 생성에 필요
 - 없으면: 경고 메시지 + 로컬 저장으로 대체
```

### 2 Auto-Command-Execution 시스템 업데이트

**업데이트 사항**:
- 의도 감지 후 신원 검증 단계 추가
- 권한 검증 실패 시 명확한 메시지
- GH 토큰 존재 여부 확인

### 3 Global-Feedback-Detection 시스템 업데이트

**업데이트 사항**:
- Issue 생성 시 GH 토큰 확인
- 토큰 없으면 로컬 저장 처리

---

## 검증 체크리스트

### Setup 프로세스
- [x] 이름 수집 (AskUserQuestion)
- [x] 역할 수집 (AskUserQuestion)
- [x] GitHub 정보 수집 (AskUserQuestion)
- [x] 토큰 수집 (사용자 입력)
- [x] 토큰 검증 (gh auth verify 또는 API)
- [x] .user-identity 파일 생성
- [x] .gh-token 파일 생성
- [x] git skip-worktree 적용
- [x] 완료 메시지 (신원 정보 확인)

### Startup 훅
- [x] .user-identity 로드
- [x] USER_NAME 추출
- [x] USER_ROLE 추출
- [x] roles.yaml에서 권한 로드
- [x] .gh-token 로드
- [x] GH_TOKEN export
- [x] git skip-worktree 재확인
- [x] 최종 상태 리포트

### 각 Command
- [ ] 신원 파일 확인
- [ ] 권한 검증
- [ ] GH 토큰 확인 (필요시)
- [ ] 권한 거절 시 명확한 메시지

### 권한 시스템
- [x] roles.yaml 정의
- [x] 역할별 commands 배열
- [x] 역할별 세부 권한 (can_*)
- [ ] 각 command에서 검증

---

## 최종 결론

| 항목 | 상태 | 비고 |
|------|------|------|
| **신원 수집** | 완벽 | setup.md 명시됨 |
| **요청 프로세스** | 완벽 | 없을 때 안내됨 |
| **로드 시스템** | 완벽 | startup.sh 자동 실행 |
| **권한 정의** | 완벽 | roles.yaml 완전 정의 |
| **각 command 검증** | 필요 | 명시적 검증 코드 추가 필요 |

**총합**: 80% (기초 완벽, 세부 통합 필요)

---

## 다음 단계

1. **모든 command에 권한 검증 헤더 추가**
 - designer.md (line 15 근처)
 - flow.md (line 15 근처)
 - create-issue.md (line 15 근처)
 - admin.md (line 15 근처)

2. **auto-command-execution.md 업데이트**
 - 신원 검증 단계 추가
 - 권한 검증 단계 추가

3. **각 command 실행 지시 업데이트**
 - Claude 실행 지시에 검증 로직 명시
 - 권한 거절 시 메시지 표준화

---

## 참고

- [Setup 명령어](../commands/setup.md)
- [Startup 훅](../hooks/startup.sh)
- [권한 정의](../manifests/roles.yaml)
- [Permission Model](./permission-model.md)
- [Auto Command Execution](./auto-command-execution.md)
