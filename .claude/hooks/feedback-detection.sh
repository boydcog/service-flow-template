#!/bin/bash

#==============================================================================
# feedback-detection.sh — 전역 피드백 감지 시스템
#==============================================================================
#
# 기능: 사용자 메시지에서 불만/피드백/제안을 감지
# 참고: .claude/spec/4-detection/4-1-global-feedback-detection.md
#
# 사용: feedback_type=$(bash feedback-detection.sh "<user_message>")
#
#==============================================================================

set -euo pipefail

# 사용자 메시지
USER_MESSAGE="$1"

#==============================================================================
# 피드백 감지 함수
#==============================================================================

detect_feedback() {
  local message="$1"
  local message_lower=$(echo "$message" | tr '[:upper:]' '[:lower:]')

  # 1. 버그 감지 (confidence: 0.9)
  if [[ $message_lower =~ 버그|동작.*(안|안.?해|안.?됨)|클릭.*(안|안.*돼)|(탭|터치).*(안|안.*돼)|표시.*(안|안.*돼|안.*됨)|깨진|깨짐|오류|에러|작동.?안|(문제|이슈).*(있|발생) ]]; then
    echo '{"type":"bug","severity":"high","confidence":0.9}'
    return 0
  fi

  # 2. 기능 요청 감지 (confidence: 0.8)
  if [[ $message_lower =~ (기능|피처|지원).*(있|있어|있나|언제)|(추가|지원|구현).?(해|줘)|다크모드|국제화|다국어 ]]; then
    echo '{"type":"feature_request","severity":"medium","confidence":0.8}'
    return 0
  fi

  # 3. 개선 제안 감지 (confidence: 0.7)
  if [[ $message_lower =~ 면.?(더.?)?좋을.?것|개선.*되면.?좋겠|다시.?생각|생각해보니.*(아쉬|부족|아깝)|이렇게.?하면.?어떨까|더.?(크게|크|작게|작) ]]; then
    echo '{"type":"improvement","severity":"low","confidence":0.7}'
    return 0
  fi

  # 4. 부정적 의견 감지 (confidence: 0.6)
  if [[ $message_lower =~ 불편|복잡|너무.?(크|작|길|짧)|좀.?(부족|아쉬|이상) ]]; then
    echo '{"type":"feedback","severity":"medium","confidence":0.6}'
    return 0
  fi

  # 5. 명시적 피드백 감지 (confidence: 0.5)
  if [[ $message_lower =~ 피드백|건의|의견|제안|요청 ]]; then
    echo '{"type":"feedback","severity":"low","confidence":0.5}'
    return 0
  fi

  # 피드백 없음
  echo "null"
  return 1
}

#==============================================================================
# 메인 실행
#==============================================================================

if [ -z "$USER_MESSAGE" ]; then
  echo "사용법: feedback-detection.sh '<사용자 메시지>'" >&2
  exit 1
fi

detect_feedback "$USER_MESSAGE"
