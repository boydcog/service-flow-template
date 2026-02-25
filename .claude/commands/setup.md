# /setup — 초기 설정

## 개요

`/setup`은 처음 세션에서 한 번만 실행하는 명령어입니다.

사용자 신원(이름, 역할, GitHub 정보)을 설정하고 GitHub 토큰을 저장합니다.

---

## Claude 실행 지시

이 명령을 실행할 때 Claude가 따라야 할 단계:

1. `.user-identity` 파일이 이미 존재하는지 확인
 - 존재하면: "이미 설정됨" 메시지 표시하고, 수정 여부 확인
 - 없으면: 새로 설정 시작

2. AskUserQuestion으로 다음 정보 수집:
 - 사용자 이름 (필수)
 - 역할 (선택: admin/developer/designer/pm)
 - GitHub 사용자명 (필수)

3. 사용자 입력 확인 후:
 - `.user-identity` 파일 생성 (포맷 하단 참조)
 - chmod 644 설정
 - git skip-worktree 활성화: `git update-index --skip-worktree .user-identity`

4. GitHub 토큰 저장:
 - 사용자에게 GitHub Personal Access Token 입력 요청 (토큰 생성 URL 제공)
 - `.gh-token` 파일 생성 (1줄, 토큰 내용만)
 - chmod 600 설정
 - git skip-worktree 활성화: `git update-index --skip-worktree .gh-token`

5. GitHub 토큰 검증:
 - `gh auth verify --hostname github.com` 실행 또는 API 호출로 검증
 - 실패 시: 토큰 재입력 유도

6. 완료 메시지 출력:
 - 설정된 신원 정보 확인
 - 다음 사용 가능한 명령어 안내 (역할에 따라)

---

## 사용 방법

```bash
/setup
```

---

## 단계별 진행

### 1단계: 사용자 이름 입력

```
 사용자 이름을 입력하세요:
> 홍길동
```

### 2단계: 역할 선택

```
 역할을 선택하세요:
 1. admin (관리자)
 2. developer (개발자)
 3. designer (디자이너)
 4. pm (기획자)

선택:
> 3
```

### 3단계: GitHub 사용자명 입력

```
 GitHub 사용자명을 입력하세요 (예: john-doe):
> hong-gildong
```

### 4단계: GitHub Access Token 입력

```
 GitHub Personal Access Token을 입력하세요:
(https://github.com/settings/tokens에서 생성)

Token (입력은 화면에 표시되지 않습니다):
> [입력 후 엔터]
```

**GH Token 생성 방법**:
1. https://github.com/settings/tokens로 이동
2. "Generate new token (classic)" 클릭
3. `repo` 권한 선택
4. 토큰 복사 후 위 입력창에 붙여넣기

### 5단계: 연결 확인

```
 GitHub 토큰 검증 중...
 연결 성공! (사용자: hong-gildong)

설정이 완료되었습니다!
- 이름: 홍길동
- 역할: designer
- GitHub: hong-gildong

다음 명령어: /designer, /flow, /create-issue
```

---

## 생성 파일

### `.user-identity` (로컬, git에서 skip)

```
name: 홍길동
role: designer
github: hong-gildong
```

**주의**: 이 파일은 `.gitignore`에 포함되어 있으며, `git skip-worktree`로 보호됩니다.

### `.gh-token` (로컬, git에서 skip, chmod 600)

```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**주의**: 이 파일도 로컬에만 유지되며, git에 커밋되지 않습니다.

---

## 역할별 액세스 권한

| 역할 | 사용 가능 명령어 |
|------|-----------------|
| **admin** | `/setup` `/admin` `/designer` `/flow` `/create-issue` |
| **developer** | `/setup` `/admin` `/designer` `/flow` `/create-issue` |
| **designer** | `/setup` `/designer` `/flow` `/create-issue` |
| **pm** | `/setup` `/flow` `/create-issue` |

---

## 다시 설정하기

기존 설정을 변경하려면 `.user-identity` 파일을 직접 수정하거나 `/setup`을 다시 실행하세요.

```bash
# 파일 직접 수정
cat > .user-identity << 'EOF'
name: 새 이름
role: designer
github: new-github-handle
EOF

# 또는 다시 실행
/setup
```

---

## 문제 해결

### "GitHub 토큰이 유효하지 않습니다" 오류

1. 토큰이 만료되었는지 확인: https://github.com/settings/tokens
2. 새 토큰 생성 후 다시 실행
3. 토큰에 `repo` 권한이 있는지 확인

### "신원 파일을 생성할 수 없습니다" 오류

- 디렉토리 권한 확인: `ls -la .user-identity`
- 파일이 이미 존재하는 경우: 기존 파일 삭제 후 재시도

### "git skip-worktree 설정 실패" 오류

- Git 설치 확인: `git --version`
- 리포지토리 상태 확인: `git status`

---

## 다음 단계

설정 완료 후:

- **Designer**: [`/designer`](./designer.md)로 컴포넌트 생성
- **PM**: [`/flow`](./flow.md)로 서비스 플로우 설계
- **Admin**: [`/admin`](./admin.md)로 템플릿 관리
- **모두**: [`/create-issue`](./create-issue.md)로 이슈 제보

---

## 참고

- [GitHub CLI 설정](https://cli.github.com/manual/gh_auth_login)
- [Personal Access Token 생성](https://github.com/settings/tokens)
- [Roles 정의](../manifests/roles.yaml)
