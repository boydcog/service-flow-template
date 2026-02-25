# Settings 업데이트 계획

현재 상태:
- 실행 스크립트: `.claude/hooks/` 에만 존재
- Settings 등록: 미비
- Intent Detection: 구현 필요

---

## 1 Settings.json 에 추가할 내용

### SessionStart 훅 - 마이그레이션 자동 실행
```json
{
 "hooks": {
 "SessionStart": [
 {
 "matcher": "",
 "hooks": [
 {
 "type": "command",
 "command": "bash .claude/hooks/startup.sh"
 }
 ]
 }
 ]
 }
}
```
 이미 있음 - startup.sh가 마이그레이션을 자동 실행

---

## 2 Skills 구조로 정리할 것

### `/admin` 스킬
- **파일**: `.claude/commands/admin.md` (스킬 정의)
- **실행**: `.claude/hooks/admin-workflow.sh` + 기타 로직
- **권한**: admin, developer
- **Intent Detection**:
 - "팀원 추가", "테마 수정", "스펙 업데이트" → `/admin`

### `/designer` 스킬
- **파일**: `.claude/commands/designer.md` (스킬 정의)
- **권한**: designer, admin, developer
- **Intent Detection**:
 - "컴포넌트 만들어줘", "버튼 추가", "UI 수정" → `/designer`

### `/flow` 스킬
- **파일**: `.claude/commands/flow.md` (스킬 정의)
- **권한**: 모든 역할
- **Intent Detection**:
 - "플로우 만들어줘", "화면 설계", "서비스 기획" → `/flow`

### `/admin-status` 스킬 (신규)
- **목적**: `check-status.sh` 래핑
- **사용**: `/admin-status`
- **기능**: GitHub 진입 없이 변경사항 확인
- **권한**: 모든 역할

---

## 3 구현 구조 개선

### 현재 (문제)
```
.claude/
├── commands/
│ ├── admin.md (문서만)
│ ├── designer.md (문서만)
│ └── flow.md (문서만)
└── hooks/
 ├── admin-workflow.sh (실행 스크립트)
 ├── create-pr.sh
 ├── check-status.sh
 └── startup.sh
```

 실행 로직이 스킬 정의와 분리되어 있음

### 개선 후
```
.claude/
├── commands/
│ ├── admin.md (스킬 정의 + 실행 로직)
│ ├── designer.md (스킬 정의 + 실행 로직)
│ ├── flow.md (스킬 정의 + 실행 로직)
│ ├── status.md (신규: 상태 확인 스킬)
│ └── setup.md (기존)
├── hooks/
│ ├── startup.sh (세션 시작)
│ ├── admin-workflow.sh (유틸)
│ ├── create-pr.sh (유틸)
│ ├── check-status.sh (유틸)
│ └── post-*.sh (Post-action 훅)
└── settings.json (스킬 등록 + 권한 + Intent Detection)
```

 스킬이 명확하게 정의되고 권한/Intent Detection과 연결됨

---

## 4 Settings.json 에 추가할 규칙

### Intent Detection 추가
```json
{
 "intentDetection": {
 "patterns": {
 "/admin": [
 "팀원 추가",
 "테마 수정",
 "스펙 업데이트",
 "권한 변경",
 "템플릿 관리"
 ],
 "/designer": [
 "컴포넌트 만들어줘",
 "버튼 추가",
 "UI 수정",
 "스토리 만들어줘",
 "카드 만들어",
 "입력창 만들기"
 ],
 "/flow": [
 "플로우 만들어줘",
 "화면 설계",
 "서비스 기획",
 "앱 만들어줘",
 "페이지 만들어줘",
 "온보딩 만들어"
 ],
 "/admin-status": [
 "상태 확인",
 "변경사항 확인",
 "PR 상태",
 "브랜치 상태"
 ],
 "/create-issue": [
 "이슈 등록",
 "버그 제보",
 "피드백 남길게",
 "신고할게",
 "문제 보고"
 ]
 },
 "requiresSetup": true
 }
}
```

---

## 5 우선순위

### Phase A: 통합 (필수)
1. `/.claude/commands/admin.md` → 스킬 정의 + `admin-workflow.sh` 참조
2. `settings.json` → Intent Detection 규칙 추가
3. `/admin-status` 신규 스킬 생성

### Phase B: 검증 (권장)
1. `/designer` 스킬 개선 (post-designer 훅과 연결)
2. `/flow` 스킬 개선 (post-flow 훅과 연결)
3. 각 스킬별 Intent Detection 테스트

### Phase C: 고도화 (선택)
1. Python 스크립트로 구현 변경
2. 더 복잡한 Intent Detection 로직
3. 팀 협업 자동화 (Agent Teams)

---

## 다음 작업

[ ] `/admin` 스킬에 admin-workflow.sh 통합
[ ] `settings.json` Intent Detection 추가
[ ] `/admin-status` 신규 스킬 생성
[ ] 권한 검증 로직 추가
[ ] 테스트
