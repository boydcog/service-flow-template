# 전역 피드백 감지 시스템 (Global Feedback Detection)

## 개요

사용자의 불만, 피드백, 제안을 **모든 상황에서 감지**하고 자동으로 Issue 공유 옵션을 제공합니다.

- `/designer` 사용 중에만 감지 ( 이전)
- **어디서나 감지** ( 현재)
 - Command 실행 중
 - 일반 대화 중
 - 다른 작업 중
 - 아무 명령도 없을 때

---

## 1. 피드백 감지 범위

### 1-1. 감지 시점 (언제든)

```
상황 1: /designer 사용 중
 사용자: "Button의 색상이 Figma와 다르네요"
 ↓ 불만 감지
 Claude: "Issue로 등록할까요?"

상황 2: 일반 대화 중
 사용자: "근데 Input 컴포넌트는 언제 나와요?"
 ↓ 요청/피드백 감지
 Claude: "Feature Request로 Issue 등록할까요?"

상황 3: /flow 실행 중
 사용자: "이 화면이 너무 복잡해 보여"
 ↓ 불만/개선 제안 감지
 Claude: "UI 개선 Issue로 등록할까요?"

상황 4: 아무 명령도 없을 때
 사용자: "근데 다크모드는 지원 안 해?"
 ↓ 기능 요청 감지
 Claude: "Feature Request Issue 등록할까요?"

상황 5: 작업 완료 후
 사용자: "좋은데, 애니메이션 있으면 더 좋겠어"
 ↓ 개선 제안 감지
 Claude: "Enhancement Issue 등록할까요?"
```

### 1-2. 감지 대상 (무엇을)

```
1. 명확한 불만/버그
 "버그가 있어"
 "동작이 안 돼"
 "클릭이 안 됨"
 "표시가 안 돼"

2. 요청/기능 요청
 "~는 어떻게 돼?"
 "~하는 기능 있어?"
 "~를 추가해주면 좋을 것 같아"

3. 개선 제안
 "~면 더 좋을 것 같은데"
 "~는 이렇게 하면 어떨까"
 "~가 개선되면 좋겠어"

4. 비판/부정적 의견
 "뭔가 불편한데"
 "다시 생각해보니 아쉬운데"
 "더 나으면 좋을 텐데"

5. 의문/의심
 "정말 이렇게 돼?"
 "이게 맞나?"
 "왜 이렇게?"

6. 명시적 피드백
 "피드백이 있는데"
 "건의가 있는데"
 "의견이 있는데"
```

---

## 2. 감지 알고리즘

### 2-1. 키워드 매칭 (정규식)

```python
def detect_feedback(user_message, context=None):
 """
 모든 상황에서 사용자 피드백 감지

 Args:
 user_message: 사용자 입력
 context: 현재 command/상황 (designer, flow, create-issue 등)

 Returns:
 feedback_info: {
 type: "bug" | "feature_request" | "improvement" | "feedback",
 severity: "critical" | "high" | "medium" | "low",
 message: str,
 confidence: float (0-1)
 }
 또는 None (피드백 없음)
 """

 # 1. 버그 감지
 bug_patterns = [
 r"버그",
 r"동작\s*(안|안\s*해|안\s*됨)",
 r"(클릭|탭|터치)\s*(안|안\s*돼)",
 r"(표시|보임|보이)\s*(안|안\s*돼|안\s*됨)",
 r"깨진|깨짐|오류|에러",
 r"작동\s*안",
 r"(문제|이슈)\s*(있|발생)",
 ]

 # 2. 기능 요청 감지
 feature_patterns = [
 r"(기능|피처|지원)\s*(있|있어|있나|언제)",
 r"(~|—)\s*(추가|지원|구현)해?줄?",
 r"(~|—)\s*있\s*있으면 좋을",
 r"(다크모드|국제화|다국어)\s*(지원|있)",
 ]

 # 3. 개선 제안 감지
 improvement_patterns = [
 r"(~|—)\s*면\s*(더\s*)?좋을\s*것",
 r"개선.*되면\s*좋겠",
 r"(다시\s*생각|생각해보니)\s*(~|—)\s*(아쉬|부족|아깝)",
 r"(~|—)\s*(이렇게|이렇게|이렇게)\s*하면\s*어떨까",
 r"~를\s*(더|조금|좀)\s*(크게|크|작게|작)",
 ]

 # 4. 부정적 의견 감지
 negative_patterns = [
 r"뭔가\s*불편",
 r"불편\s*(해|하)",
 r"복잡\s*(해|하)",
 r"너무\s*(크|작|길|짧)",
 r"좀\s*(부족|아쉬|이상)",
 ]

 # 5. 명시적 피드백 감지
 explicit_patterns = [
 r"피드백",
 r"건의",
 r"의견",
 r"제안",
 r"요청",
 ]

 # 매칭 실행
 for pattern in bug_patterns:
 if re.search(pattern, user_message, re.IGNORECASE):
 return {
 "type": "bug",
 "severity": "high",
 "message": user_message,
 "confidence": 0.9
 }

 for pattern in feature_patterns:
 if re.search(pattern, user_message, re.IGNORECASE):
 return {
 "type": "feature_request",
 "severity": "medium",
 "message": user_message,
 "confidence": 0.8
 }

 for pattern in improvement_patterns:
 if re.search(pattern, user_message, re.IGNORECASE):
 return {
 "type": "improvement",
 "severity": "low",
 "message": user_message,
 "confidence": 0.7
 }

 for pattern in negative_patterns:
 if re.search(pattern, user_message, re.IGNORECASE):
 return {
 "type": "feedback",
 "severity": "medium",
 "message": user_message,
 "confidence": 0.6
 }

 for pattern in explicit_patterns:
 if re.search(pattern, user_message, re.IGNORECASE):
 return {
 "type": "feedback",
 "severity": "low",
 "message": user_message,
 "confidence": 0.5
 }

 return None
```

### 2-2. 신뢰도 점수 (Confidence)

```
버그 리포트
 "버그가 있어요" → 0.95 (명확함)
 "클릭이 안 돼" → 0.90 (매우 명확)
 "뭔가 이상한데" → 0.60 (모호함)

기능 요청
 "다크모드 지원해줘" → 0.95
 "~는 어떻게 돼?" → 0.70 (질문과 구분)

개선 제안
 "이렇게 하면 더 좋을 것 같은데" → 0.85
 "좀 크면 좋을 텐데" → 0.65
```

**신뢰도 임계값**: 0.6 이상일 때만 Issue 공유 옵션 제공

---

## 3. 전역 피드백 감지 플로우

### 3-1. 모든 상황에서 작동

```
Claude와 모든 대화/작업:

매 사용자 입력마다:
 1. 입력 분석
 2. 피드백 감지 알고리즘 실행
 3. 피드백 감지 → 신뢰도 계산
 4. 신뢰도 ≥ 0.6 → Issue 공유 옵션 제공
 신뢰도 < 0.6 → 무시
```

### 3-2. Issue 공유 옵션 제공 위치

```
상황 1: Command 실행 중 (5단계 검증 요청 후)
사용자: "색상이 다르네요"
↓ 피드백 감지 (enhancement 0.85)
Claude: [Issue 공유 옵션 제공]

상황 2: 일반 대화 중
사용자: "Input 컴포넌트 언제 나와?"
↓ 피드백 감지 (feature_request 0.80)
Claude: 응답 + [Issue 공유 옵션 제공]

상황 3: 질문/답변 중
사용자: "이걸 어떻게 써?"
Claude: 설명 제공
사용자: "근데 너무 복잡한데"
↓ 피드백 감지 (improvement 0.75)
Claude: [Issue 공유 옵션 제공]
```

---

## 4. Issue 공유 옵션 (Inline)

### 4-1. 포맷 (모든 상황에 적용)

```
[사용자 피드백 감지]

Claude:
기본 응답...

혹시 이것을 Issue로 등록하시겠습니까?

제목: "Button 컴포넌트: 색상 불일치"
유형: Enhancement

[Yes - Bug] 버그로 등록
[Yes - Enhancement] 개선요청으로 등록
[Yes - Feature Request] 기능 요청으로 등록
[No] 나중에
```

### 4-2. Issue 유형 자동 선택

```python
def map_feedback_to_issue_type(feedback_type, severity):
 """피드백 타입 → Issue 라벨"""

 mapping = {
 "bug": "bug",
 "feature_request": "enhancement",
 "improvement": "enhancement",
 "feedback": "enhancement"
 }

 return mapping[feedback_type]
```

매핑:
```
bug → "bug" 라벨
feature_request → "enhancement" 라벨
improvement → "enhancement" 라벨
feedback → "enhancement" 라벨
```

### 4-3. Issue 제목 자동 생성

```
감지된 피드백: "Button의 색상이 Figma와 다르네요"
↓
자동 생성된 Issue 제목:
"Button 컴포넌트: 색상 불일치"

또는

감지된 피드백: "Input 컴포넌트는 언제 나와요?"
↓
자동 생성된 Issue 제목:
"Feature Request: Input 컴포넌트"
```

---

## 5. 구현 위치 (Claude Code)

### 5-1. 모든 사용자 입력 후

```python
# 예: Claude Code 핵심 루프
while True:
 user_input = get_user_input()

 # 1. 명령 처리
 if user_input.startswith("/"):
 handle_command(user_input)
 else:
 # 2. 일반 대화 처리
 response = generate_response(user_input)

 # 3. [중요] 모든 입력 후 피드백 감지
 feedback = detect_feedback(user_input)
 if feedback and feedback["confidence"] >= 0.6:
 show_issue_share_option(feedback)
```

### 5-2. 통합 위치

- **모든 command 후**
 - `/designer` 완료 후
 - `/flow` 완료 후
 - `/create-issue` 완료 후
 - `/admin` 완료 후

- **command 실행 중**
 - 단계 사이 (2단계 → 3단계 사이)
 - 작업 수행 중

- **일반 대화 중**
 - 질문/답변
 - 설명/가이드
 - 조언/제안

---

## 6. AskUserQuestion 템플릿 (전역)

### 6-1. 기본 Issue 공유 옵션

```json
{
 "question": "불만/피드백을 감지했습니다. Issue로 등록하시겠습니까?",
 "header": "Feedback Detection",
 "options": [
 {
 "label": "Issue 생성 - Bug",
 "description": "버그 리포트로 등록합니다"
 },
 {
 "label": "Issue 생성 - Enhancement",
 "description": "개선요청/기능요청으로 등록합니다"
 },
 {
 "label": "나중에",
 "description": "지금은 등록하지 않습니다"
 },
 {
 "label": "수정",
 "description": "제목/내용을 수정한 후 등록합니다"
 }
 ],
 "multiSelect": false
}
```

### 6-2. 피드백 유형별 옵션 커스터마이즈

**Bug 감지 시**:
```
"명확한 버그를 감지했습니다. Issue로 등록할까요?"

[Yes - Bug] Bug로 등록
[No] 나중에
[Edit] 수정
```

**Feature Request 감지 시**:
```
"기능 요청을 감지했습니다. Issue로 등록할까요?"

[Yes - Enhancement] Enhancement로 등록
[No] 나중에
[Edit] 수정
```

**Improvement 감지 시**:
```
"개선 제안을 감지했습니다. Issue로 등록할까요?"

[Yes - Enhancement] Enhancement로 등록
[No] 나중에
[Edit] 수정
```

---

## 7. 선택 후 처리

### 7-1. Yes 선택

```bash
# 1. Issue 제목 확인/수정
제목: "Button 컴포넌트: 색상 불일치"

# 2. Issue 생성
gh issue create \
 --title "Button 컴포넌트: 색상 불일치" \
 --body "감지된 피드백: Button의 색상이 Figma와 다르네요\n\n..." \
 --label "enhancement"

# 3. 결과 출력
 Issue #123이 생성되었습니다!
 https://github.com/.../issues/123
```

### 7-2. No 선택

```
이해했습니다. 나중에 필요하면 언제든 공유해주세요!
```

### 7-3. Edit 선택

```
Issue 제목을 수정해주세요:
> "Button 컴포넌트: 색상 불일치 (Figma와 비교)"

상세 내용:
> "Button 컴포넌트의 배경색이 Figma 디자인의 파란색(#3B82F6)과 다르게
 노란색으로 표시되고 있습니다. 빠른 해결 부탁드립니다."

이제 등록할까요?
[Yes] Issue 생성
[No] 취소
```

---

## 8. Fallback (토큰 없을 때)

```
GitHub 토큰이 없습니다.

로컬에 저장하겠습니다:
.claude/state/pending-issues/

나중에 gh auth login 후:
/create-issue:sync-pending

로컬 저장 완료!
```

---

## 9. 예제 시나리오

### 예제 1: Designer 작업 중 불만 감지

```
사용자: /designer
Claude: 프레임워크 선택 요청...
사용자: Web
...
[4단계 작업 수행]
...
[5단계 검증 요청]
사용자: "완료 - 모두 정상"
Claude: [6단계 공유 확인]
사용자: "PR 생성"
Claude: [7단계 불만 감지 옵션]
사용자: "아, 그런데 색상이 Figma와 다르네요"
↓ 피드백 감지 (enhancement 0.85)
Claude:
Issue로 등록할까요?
제목: "Button 컴포넌트: 색상 불일치"
[Yes - Enhancement] [No] [Edit]
```

### 예제 2: 일반 대화 중 기능 요청 감지

```
사용자: "근데 Input 컴포넌트는 언제 나와요?"
Claude: "현재 Button, Card, Select 등이 완료되었고,
Input 컴포넌트는 다음주에 개발 예정입니다."
↓ 피드백 감지 (feature_request 0.80)
Claude:
혹시 이를 Feature Request로 Issue 등록할까요?
제목: "Feature Request: Input 컴포넌트"
[Yes - Enhancement] [No] [Edit]
```

### 예제 3: 설명/가이드 제공 중 개선 제안 감지

```
Claude: "Storybook에서 다음을 확인하세요:
1. 시각적 일치
2. 기능 동작
3. 접근성
4. 반응형"

사용자: "좀 복잡한데, 체크리스트로 만들면 어떨까?"
↓ 피드백 감지 (improvement 0.75)
Claude:
개선 제안을 감지했습니다. Issue로 등록할까요?
제목: "검증 프로세스: 체크리스트 형식 개선"
[Yes - Enhancement] [No] [Edit]
```

### 예제 4: 아무 명령 없이 피드백만 제공

```
사용자: "근데 다크모드는 지원 안 해?"
↓ 피드백 감지 (feature_request 0.85)
Claude:
기능 요청을 감지했습니다. Issue로 등록할까요?
제목: "Feature Request: 다크모드 지원"
[Yes - Enhancement] [No] [Edit]
```

---

## 10. 구현 체크리스트

- [ ] 피드백 감지 알고리즘 구현
 - [ ] 버그 패턴
 - [ ] 기능 요청 패턴
 - [ ] 개선 제안 패턴
 - [ ] 부정적 의견 패턴
 - [ ] 명시적 피드백 패턴

- [ ] 신뢰도 계산 로직
 - [ ] 패턴별 가중치 정의
 - [ ] 임계값 설정 (0.6)

- [ ] Issue 공유 옵션 구현
 - [ ] AskUserQuestion 템플릿
 - [ ] Issue 유형 자동 선택
 - [ ] Issue 제목 자동 생성

- [ ] 모든 상황에서 통합
 - [ ] Command 실행 중
 - [ ] Command 완료 후
 - [ ] 일반 대화 중
 - [ ] 아무 명령 없을 때

- [ ] Fallback 처리
 - [ ] 토큰 없을 때
 - [ ] Issue 생성 실패 시

---

## 참고

- [Intent Detection](./intent-detection.md)
- [Flow Standardization](./flow-standardization.md)
- [Validation Flow](./validation-flow.md)
- [Create-Issue Command](../commands/create-issue.md)
