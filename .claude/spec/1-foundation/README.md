# 기초 명세 (1-Foundation)

## 개요

모든 다른 명세의 기반이 되는 **기초 명세** 모음입니다.

이 디렉토리의 문서들은:
- 다른 모든 문서가 참조함
- 독립적으로 이해 가능
- 구현의 첫 번째 단계

---

## 1-1-permission-model.md

### 역할
- **모든 것의 기초**
- 권한 시스템의 근간

### 내용
- 3-tier 권한 모델 (완전/안내/거절)
- 5가지 역할 (admin, developer, designer, pm, guest)
- 5가지 intent별 권한 매트릭스

### 사용처

```
1-1-permission-model.md
    ↓ 의존 (참조)
    ├─ 2-1-intent-detection.md (의도 감지 시 권한 검증)
    ├─ 2-2-auto-command-execution.md (자동 실행 시 권한 검증)
    ├─ 3-1-validation-flow.md (권한 정보 제공)
    ├─ 3-2-flow-standardization.md (권한 기반 흐름)
    ├─ 4-1-global-feedback-detection.md (권한 기반 접근)
    └─ 모든 command 파일들 (권한 검증)
```

### 구현 순서
1단계 (가장 먼저): 이 문서부터 시작
- permission-model.py 구현
- 각 command에 권한 검증 로직 추가
- 역할별 접근 제어 테스트

---

## 다음 단계

기초를 이해한 후:
- `../2-core-system/` 진행
- `../3-workflow/` 진행
- `../4-detection/` 진행

---

**참고**: 이 디렉토리는 **기초(Foundation)** 역할을 합니다.
- 현재: 1-1-permission-model.md만 있음
- 향후: 1-2-setup-process.md 추가 예정
