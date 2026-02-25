# Service Flow Template

**회사 전체가 공유하는 Claude Code 템플릿입니다.**

3가지 역할(Admin/Developer, Designer, PM)이 협업하여 공통 컴포넌트 라이브러리와 서비스 플로우를 구축합니다.

---

## Overview

이 템플릿은 **PRD → 컴포넌트 → 서비스 플로우** 까지의 전체 개발 워크플로우를 자동화합니다.

### 역할별 작업

| 역할 | 주요 기능 | 명령어 |
|------|---------|--------|
| **Admin/Developer** | 템플릿, 컴포넌트 스펙 관리 | `/admin`, `/designer` |
| **Designer** | Emocog 테마 기반 컴포넌트 제작 | `/designer` |
| **PM** | 완성된 컴포넌트로 서비스 플로우 설계 | `/flow` |
| **모두** | 이슈 제보, 신원 설정 | `/setup`, `/create-issue` |

---

## Quick Start

### 1단계: 신원 설정

```bash
/setup
```

- 이름, 역할, GitHub 정보 입력
- GH Access Token 저장

### 2단계: 역할별 작업 시작

**Designer라면**:
```bash
/designer
```
→ 새 컴포넌트 생성 또는 기존 컴포넌트 수정

**PM이라면**:
```bash
/flow
```
→ 서비스 플로우 설계

**Admin/Developer라면**:
```bash
/admin
```
→ 템플릿 및 시스템 관리

### 3단계: PR 생성 및 공유

모든 작업은 자동으로 **git worktree**에서 수행되고 **PR**로 생성됩니다.

리뷰 후 `main` 브랜치에 병합됩니다.

---

## Directory Structure

```
service-flow-template/
├── .claude/ # Claude Code 설정
│ ├── commands/ # 명령어 구현 (/setup, /designer, /flow, 등)
│ ├── manifests/ # 설정 파일 (roles, team, theme)
│ ├── spec/ # 개발 규칙 (component-spec, flow-spec)
│ ├── templates/ # PR/이슈 템플릿
│ ├── hooks/ # 세션 시작 훅 (git sync + 신원 로드)
│ └── settings.json # Claude 권한 설정
├── components/ # 재사용 가능한 컴포넌트 라이브러리
│ ├── web/ # Next.js / Vite / Remix 컴포넌트
│ ├── native/ # React Native (Gluestack) 컴포넌트
│ └── theme/ # Emocog 테마 (CSS vars + Gluestack)
├── flows/ # 서비스 플로우 (main에서는 gitignored)
│ └── {product-name}/ # 제품별 플로우
├── CLAUDE.md # 프로젝트 AI 지침
└── README.md # 이 파일
```

---

## Emocog Theme

전체 프로젝트는 **Emocog 테마**를 기반으로 합니다.

### 웹 (Tailwind CSS)

```typescript
<button className="bg-primary text-primary-foreground hover:opacity-90">
 Primary Button
</button>
```

### 네이티브 (Gluestack)

```typescript
<Button bg="$primary">
 <Text>Primary Button</Text>
</Button>
```

### 테마 정의

- **색상**: `.claude/manifests/theme.yaml`
- **CSS 변수**: `components/theme/tokens.css`
- **Gluestack 토큰**: `components/theme/gluestack-theme.ts`

---

## Documentation

### 개발자용

- [CLAUDE.md](./CLAUDE.md) — 프로젝트 개요 및 명령어 가이드
- [컴포넌트 스펙](./claude/spec/component-spec.md) — 웹/네이티브 컴포넌트 규칙
- [플로우 스펙](./claude/spec/flow-spec.md) — 서비스 플로우 설계 컨벤션

### 설정

- [Roles 정의](./claude/manifests/roles.yaml) — 역할별 권한
- [Team 관리](./claude/manifests/team.yaml) — 팀원 명단
- [Emocog 테마](./claude/manifests/theme.yaml) — 디자인 토큰

### 명령어

- [/setup](./claude/commands/setup.md) — 초기 설정
- [/admin](./claude/commands/admin.md) — 템플릿 관리
- [/designer](./claude/commands/designer.md) — 컴포넌트 제작
- [/flow](./claude/commands/flow.md) — 서비스 플로우 설계
- [/create-issue](./claude/commands/create-issue.md) — 이슈 제보

---

## Branch Strategy

| 브랜치 | 내용 | `flows/` 추적 |
|--------|------|--------|
| `main` | 템플릿 + 컴포넌트 라이브러리 | gitignored |
| `flow/{product-name}` | 제품별 서비스 플로우 | 추적됨 |

**워크플로우**:
1. PM이 `/flow {product-name}` 실행
2. `flow/{product-name}` 브랜치 자동 생성 (main에서 분기)
3. 로컬에서 바이브코딩 및 테스트
4. PR 자동 생성
5. 리뷰 후 main으로 병합

---

## Security

### 로컬 파일 보호

`.user-identity` 및 `.gh-token`은:
- `.gitignore`에 포함
- `git skip-worktree`로 보호
- 로컬 환경에만 유지
- 공유 레포지토리에 커밋되지 않음

### 메인 브랜치 보호

- `git worktree`를 사용하여 메인 브랜치 직접 수정 방지
- 모든 변경은 PR을 통해 코드 리뷰 후 병합
- force-push 불가

---

## Session Startup Automation

매 세션 시작 시 자동으로:

1. 사용자 신원 로드
2. GH 토큰 로드
3. 로컬 파일 보호
4. Git 동기화 (pull --rebase)
5. 상태 리포트 출력

```
=== Service Flow Template — Session Start ===
 안녕하세요, 홍길동 (designer)!

 웹 컴포넌트: 12개
 네이티브 컴포넌트: 5개
 브랜치: main

명령어: /setup /admin /designer /flow /create-issue
```

---

## Completion Criteria

- [ ] 모든 필수 명령어 구현
- [ ] 사용자 신원 및 토큰 보호 작동
- [ ] git 자동 동기화 확인
- [ ] 역할별 권한 검증
- [ ] 컴포넌트 및 플로우 PR 생성 작동
- [ ] 메인 브랜치 보호 (force-push 방지)

---

## Contributing

### 버그 리포트

```bash
/create-issue
```

버그를 발견하면 이슈를 제출하세요. 자동으로 적절한 라벨이 추가됩니다.

### 기능 제안

GitHub Discussions에서 새로운 아이디어를 제안하거나 `/create-issue`로 enhancement 라벨을 붙여 제출하세요.

### 코드 기여

1. `/setup`으로 신원 설정
2. 역할에 맞는 명령어 실행 (`/designer`, `/flow`, 등)
3. PR 생성 및 리뷰
4. main 브랜치에 병합

---

## References

- [Emocog 테마](https://tweakcn.com/themes/cmlyp83mj000004kt9m73dbqt?p=custom)
- [Next.js 문서](https://nextjs.org/docs)
- [Tailwind CSS 문서](https://tailwindcss.com)
- [React Native / Gluestack](https://gluestack.io)
- [GitHub CLI](https://cli.github.com)

---

## Support

문제가 발생하거나 도움이 필요하면:

1. 관련 문서 확인 ([CLAUDE.md](./CLAUDE.md), spec/ 등)
2. `/create-issue`로 이슈 제보
3. admin에게 직접 연락

---

## License

이 템플릿은 내부용입니다. 저작권 및 라이선스 정책을 참조하세요.

---

**Happy Coding!**

시작하려면 `/setup`을 실행하세요.
