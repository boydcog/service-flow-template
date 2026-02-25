#!/bin/bash

#==============================================================================
# auto-dispatcher.sh — 사용자 의도 자동 감지 및 명령 자동 실행
#==============================================================================
#
# 기능: 사용자 메시지에서 의도를 감지하여 자동으로 적절한 Skill을 실행
# 참고: .claude/spec/2-core-system/2-1-intent-detection.md
#
# 사용: 일반적으로 startup.sh에서 자동 호출
#       또는 Claude가 사용자 메시지 분석 시 직접 호출
#
#==============================================================================

set -euo pipefail

# 스크립트 디렉토리
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

# 설정 파일
USER_IDENTITY_FILE="$PROJECT_ROOT/.user-identity"

#==============================================================================
# 사용자 정보 로드
#==============================================================================

load_user_info() {
  if [ ! -f "$USER_IDENTITY_FILE" ]; then
    # 신원 파일 없음 → setup 필요
    return 1
  fi

  export USER_NAME=$(grep '^name:' "$USER_IDENTITY_FILE" | sed 's/name: //')
  export USER_ROLE=$(grep '^role:' "$USER_IDENTITY_FILE" | sed 's/role: //')
  return 0
}

#==============================================================================
# 권한 검증
#==============================================================================

check_permission() {
  local command="$1"
  local role="$USER_ROLE"

  case "$command" in
    designer)
      # admin, developer, designer만 가능
      if [[ ! "$role" =~ ^(admin|developer|designer)$ ]]; then
        return 1
      fi
      ;;
    admin)
      # admin, developer만 가능
      if [[ ! "$role" =~ ^(admin|developer)$ ]]; then
        return 1
      fi
      ;;
    flow|create-issue)
      # 모든 역할 가능
      ;;
  esac

  return 0
}

#==============================================================================
# 의도 감지 함수
#==============================================================================

detect_designer_intent() {
  local message="$1"
  local message_lower=$(echo "$message" | tr '[:upper:]' '[:lower:]')

  # 컴포넌트 관련 키워드
  if [[ $message_lower =~ (컴포넌트|button|card|input|dialog|modal).*(만들|추가|수정|작성) ]] || \
     [[ $message_lower =~ (만들|추가|수정).*(컴포넌트|button|card|input|dialog|modal) ]] || \
     [[ $message_lower =~ (UI|ui).*(만들|추가|수정) ]] || \
     [[ $message_lower =~ (스토리|storybook).*(만들|추가|작성) ]] || \
     [[ $message_lower =~ 디자인.*시스템 ]] || \
     [[ $message_lower =~ emocog ]] || \
     [[ $message_lower =~ 테마.*컴포넌트 ]]; then
    return 0
  fi

  return 1
}

detect_flow_intent() {
  local message="$1"
  local message_lower=$(echo "$message" | tr '[:upper:]' '[:lower:]')

  # 플로우/화면 설계 키워드
  if [[ $message_lower =~ (플로우|flow).*(만들|설계|디자인) ]] || \
     [[ $message_lower =~ (화면|페이지|page).*(만들|설계|디자인) ]] || \
     [[ $message_lower =~ (서비스|앱|app).*(플로우|흐름|설계) ]] || \
     [[ $message_lower =~ (온보딩|가입|로그인|결제|체크아웃).*(플로우|설계|만들) ]] || \
     [[ $message_lower =~ (대시보드|홈화면).*(만들|설계) ]] || \
     [[ $message_lower =~ (대충|이런.*느낌).*(만들|설계) ]]; then
    return 0
  fi

  return 1
}

detect_create_issue_intent() {
  local message="$1"
  local message_lower=$(echo "$message" | tr '[:upper:]' '[:lower:]')

  # 버그/피드백 키워드
  if [[ $message_lower =~ (버그|bug).*(제보|리포트|신고) ]] || \
     [[ $message_lower =~ (문제|에러|error).*(있|발생|발견) ]] || \
     [[ $message_lower =~ (동작|작동).*(안|안.*됨) ]] || \
     [[ $message_lower =~ (안.*보|안보임|표시.*안) ]] || \
     [[ $message_lower =~ (깨진|버그) ]] || \
     [[ $message_lower =~ (기능|feature).*(추가|요청) ]] || \
     [[ $message_lower =~ (개선|improvement) ]] || \
     [[ $message_lower =~ (피드백|의견|건의) ]] || \
     [[ $message_lower =~ (이슈|issue).*(등록|제보) ]]; then
    return 0
  fi

  return 1
}

detect_admin_intent() {
  local message="$1"
  local message_lower=$(echo "$message" | tr '[:upper:]' '[:lower:]')

  # 관리 키워드
  if [[ $message_lower =~ (팀원|멤버|사용자).*(추가|관리|등록) ]] || \
     [[ $message_lower =~ 권한.*(변경|수정|관리) ]] || \
     [[ $message_lower =~ (컴포넌트|플로우).*스펙 ]] || \
     [[ $message_lower =~ (템플릿|규칙).*(수정|관리) ]] || \
     [[ $message_lower =~ 테마.*(수정|업데이트|변경) ]] || \
     [[ $message_lower =~ emocog.*(테마|색상) ]] || \
     [[ $message_lower =~ 디자인.*토큰 ]] || \
     [[ $message_lower =~ 프로젝트.*설정 ]]; then
    return 0
  fi

  return 1
}

#==============================================================================
# 의도 판단 및 명령 결정
#==============================================================================

dispatch_command() {
  local message="$1"

  # 사용자 정보 로드
  if ! load_user_info; then
    echo "❌ 사용자 신원이 설정되지 않았습니다"
    echo "먼저 /setup을 실행해주세요"
    return 1
  fi

  # 명시적 /command 감지 (우선순위 최상)
  if [[ $message =~ ^/setup ]]; then
    echo "setup"
    return 0
  elif [[ $message =~ ^/designer ]]; then
    echo "designer"
    return 0
  elif [[ $message =~ ^/flow ]]; then
    echo "flow"
    return 0
  elif [[ $message =~ ^/create-issue ]]; then
    echo "create-issue"
    return 0
  elif [[ $message =~ ^/admin ]]; then
    echo "admin"
    return 0
  fi

  # 의도 감지 (우선순위: admin → designer → flow → create-issue)
  # admin이 가장 제한적이므로 먼저 확인
  if detect_admin_intent "$message"; then
    if check_permission "admin"; then
      echo "admin"
      return 0
    else
      echo "❌ 권한 없음: admin" >&2
      echo "[역할] $USER_ROLE은 /admin을 사용할 수 없습니다" >&2
      return 1
    fi
  fi

  if detect_designer_intent "$message"; then
    if check_permission "designer"; then
      echo "designer"
      return 0
    else
      echo "❌ 권한 없음: designer" >&2
      echo "[역할] $USER_ROLE은 /designer를 사용할 수 없습니다" >&2
      return 1
    fi
  fi

  if detect_flow_intent "$message"; then
    if check_permission "flow"; then
      echo "flow"
      return 0
    fi
  fi

  if detect_create_issue_intent "$message"; then
    if check_permission "create-issue"; then
      echo "create-issue"
      return 0
    fi
  fi

  # 의도를 감지할 수 없음
  return 1
}

#==============================================================================
# 메인 실행
#==============================================================================

main() {
  local message="$1"

  if [ -z "$message" ]; then
    echo "사용법: auto-dispatcher.sh '<사용자 메시지>'" >&2
    return 1
  fi

  # 의도 판단
  if ! command=$(dispatch_command "$message"); then
    # 의도를 판단할 수 없거나 권한 없음
    return 1
  fi

  # 결과 출력
  echo "$command"
  return 0
}

main "$@"
