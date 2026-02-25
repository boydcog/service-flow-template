# 권한 검증 가이드

## 개요

모든 command에서 **가장 먼저 실행**해야 하는 권한 검증 로직입니다.

---

## 1. 검증 단계 (3단계)

### 1단계: 신원 파일 확인
```bash
if [ ! -f .user-identity ]; then
  echo "❌ 사용자 신원이 설정되지 않았습니다"
  echo "먼저 /setup을 실행해주세요"
  exit 1
fi
```

### 2단계: 사용자 정보 로드
```bash
USER_NAME=$(grep '^name:' .user-identity | sed 's/name: //')
USER_ROLE=$(grep '^role:' .user-identity | sed 's/role: //')
```

### 3단계: 권한 검증 (permission-model.md 기준)
```bash
CURRENT_COMMAND="designer"  # 또는 flow, create-issue, admin

# permission-model.md 참조:
# designer: admin, developer, designer만 가능
# flow: 모두 가능 (admin, developer, designer, pm)
# create-issue: 모두 가능
# admin: admin, developer만 가능

case "$CURRENT_COMMAND" in
  designer)
    if [[ "$USER_ROLE" != "admin" && "$USER_ROLE" != "developer" && "$USER_ROLE" != "designer" ]]; then
      echo "❌ 권한 없음"
      echo "역할 [$USER_ROLE]은 /designer을 사용할 수 없습니다"
      echo "필요한 권한: admin, developer, designer"
      exit 1
    fi
    ;;
  admin)
    if [[ "$USER_ROLE" != "admin" && "$USER_ROLE" != "developer" ]]; then
      echo "❌ 권한 없음"
      echo "역할 [$USER_ROLE]은 /admin을 사용할 수 없습니다"
      echo "필요한 권한: admin, developer"
      exit 1
    fi
    ;;
  flow|create-issue)
    # 모든 역할 가능
    ;;
esac

echo "✅ 권한 확인 완료"
echo "역할: $USER_ROLE | 사용자: $USER_NAME"
```

---

## 2. 각 Command에서의 적용

### designer.md
```markdown
## 선행 조건 확인

1. 신원 파일 확인 (→ /setup 실행 유도)
2. 권한 검증
   - designer: admin, developer, designer만 가능 ✅
   - pm: 경고 후 진행 가능
   - guest: 거절

## 실행 흐름
...
```

### flow.md
```markdown
## 선행 조건 확인

1. 신원 파일 확인
2. 권한 검증
   - 모든 역할 가능 ✅

## 실행 흐름
...
```

### create-issue.md
```markdown
## 선행 조건 확인

1. 신원 파일 확인
2. 권한 검증
   - 모든 역할 가능 ✅

## 실행 흐름
...
```

### admin.md
```markdown
## 선행 조건 확인

1. 신원 파일 확인
2. 권한 검증
   - admin, developer만 가능 ✅
   - designer/pm: 거절

## 실행 흐름
...
```

---

## 3. 권한별 메시지 (표준화)

### 권한 있음 (✅)
```
✅ 권한 확인 완료
역할: [USER_ROLE] | 사용자: [USER_NAME]

이 세션에서는 /[COMMAND]를 사용해서...
[자동 실행 시작]
```

### 권한 경고 (⚠️)
```
⚠️  컴포넌트 제작은 보통 designer가 하는 작업입니다.

[USER_ROLE]이셔도 진행하시겠습니까?

[Yes] 계속 진행
[No]  다른 작업 추천
```

### 권한 거절 (❌)
```
❌ 권한 없음

역할 [USER_ROLE]은 /admin을 사용할 수 없습니다.

필요한 권한: admin, developer
현재 역할이 할 수 있는 작업:
- /designer — 컴포넌트 제작
- /flow — 플로우 설계
- /create-issue — 이슈 제보

다른 작업을 도와드릴까요?
```

---

## 4. 참고 문서

- `spec/1-foundation/1-1-permission-model.md` — 권한 매트릭스
- `spec/README.md` — 명세 네비게이션

---

## 5. 구현 체크리스트

### Phase 2-1: Permission Validation
- [ ] 각 command에 권한 검증 코드 추가
- [ ] 권한별 메시지 표준화
- [ ] 테스트 (모든 역할 × 모든 command)

### Phase 2-2: Intent Detection (다음)
- [ ] auto-dispatcher.sh 구현
- [ ] 키워드 패턴 정의

---

**상태**: Phase 2-1 구현 진행 중
**다음**: 각 command에 이 가이드 적용
