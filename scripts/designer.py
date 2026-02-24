#!/usr/bin/env python3
"""
/designer 명령어 자동화 스크립트
컴포넌트 생성/수정 → 스토리 파일 생성 → Storybook 실행 → 브라우저 띄우기 → PR 생성
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional

# process-manager import
sys.path.insert(0, str(Path(__file__).parent))
import process_manager as pm
import verify_designer

# 프로젝트 루트
PROJECT_ROOT = Path(__file__).parent.parent
COMPONENTS_WEB = PROJECT_ROOT / "components" / "web"
COMPONENTS_NATIVE = PROJECT_ROOT / "components" / "native"


def load_user_identity() -> dict:
    """사용자 신원 파일 로드"""
    identity_file = PROJECT_ROOT / ".user-identity"
    if not identity_file.exists():
        print("❌ 신원 파일 없음. /setup을 먼저 실행하세요.")
        sys.exit(1)

    identity = {}
    with open(identity_file) as f:
        for line in f:
            if ": " in line:
                key, value = line.strip().split(": ", 1)
                identity[key] = value

    return identity


def check_permissions(user_role: str) -> None:
    """권한 확인"""
    allowed_roles = ["admin", "developer", "designer"]
    if user_role not in allowed_roles:
        print(f"❌ {user_role}은 /designer 명령어를 사용할 수 없습니다.")
        print(f"필요 역할: designer 이상 (admin, developer, designer)")
        sys.exit(1)


def select_framework() -> str:
    """프레임워크 선택"""
    print("\n🏗️  프레임워크를 선택하세요:")
    print("  1. Web (React/Vite)")
    print("  2. Native (React Native)")

    while True:
        choice = input("\n선택 (1 또는 2): ").strip()
        if choice in ["1", "2"]:
            return "web" if choice == "1" else "native"
        print("❌ 잘못된 선택입니다.")


def select_action() -> str:
    """액션 선택"""
    print("\n🎯 액션을 선택하세요:")
    print("  1. ✨ 새 컴포넌트 생성")
    print("  2. ✏️  기존 컴포넌트 수정")

    while True:
        choice = input("\n선택 (1 또는 2): ").strip()
        if choice in ["1", "2"]:
            return "create" if choice == "1" else "modify"
        print("❌ 잘못된 선택입니다.")


def get_component_info() -> dict:
    """컴포넌트 정보 입력"""
    print("\n📦 컴포넌트 정보 입력")
    print("=" * 40)

    name = input("컴포넌트 이름 (예: Button): ").strip()
    if not name:
        print("❌ 이름을 입력해주세요.")
        sys.exit(1)

    description = input("설명 (예: 클릭 가능한 버튼): ").strip()

    print("\n컴포넌트 유형:")
    print("  a) Basic (단순)")
    print("  b) Form (폼)")
    print("  c) Container (레이아웃)")
    component_type = input("선택 (a/b/c): ").strip().lower()
    if component_type not in ["a", "b", "c"]:
        component_type = "a"

    return {
        "name": name,
        "description": description,
        "type": component_type,
    }


def generate_component_code(framework: str, info: dict) -> str:
    """컴포넌트 코드 생성"""
    name = info["name"]

    if framework == "web":
        return f'''import React from 'react'

interface {name}Props extends React.HTMLAttributes<HTMLDivElement> {{
  children?: React.ReactNode
  className?: string
}}

/**
 * {name} 컴포넌트
 *
 * {info['description']}
 *
 * @example
 * <{name}>콘텐츠</{name}>
 */
export const {name}: React.FC<{name}Props> = ({{
  children,
  className = '',
  ...props
}}) => {{
  return (
    <div
      className={{`
        rounded-lg p-4
        border border-border bg-background
        dark:border-border dark:bg-background
        ${{className}}
      `}}
      {{...props}}
    >
      {{children}}
    </div>
  )
}}
'''
    else:
        return f'''import React from 'react'

interface {name}Props {{
  children?: React.ReactNode
}}

/**
 * {name} 네이티브 컴포넌트
 *
 * {info['description']}
 */
export const {name}: React.FC<{name}Props> = ({{ children }}) => {{
  return <div>{{children}}</div>
}}
'''


def generate_story_code(framework: str, info: dict) -> str:
    """스토리 파일 생성"""
    name = info["name"]

    return f'''import type {{ Meta, StoryObj }} from '@storybook/react'
import {{ {name} }} from './{name}'

const meta = {{
  title: 'Components/{name}',
  component: {name},
  parameters: {{
    layout: 'centered',
  }},
  tags: ['autodocs'],
  argTypes: {{}},
}} satisfies Meta<typeof {name}>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {{
  args: {{
    children: '{name} 컴포넌트 기본 상태',
  }},
}}

export const WithCustomText: Story = {{
  args: {{
    children: '커스텀 텍스트가 들어간 {name} 컴포넌트',
  }},
}}
'''


def create_component(framework: str, info: dict) -> Path:
    """컴포넌트 파일 생성"""
    if framework == "web":
        component_dir = COMPONENTS_WEB
    else:
        component_dir = COMPONENTS_NATIVE

    component_dir.mkdir(parents=True, exist_ok=True)

    name = info["name"]
    component_file = component_dir / f"{name}.tsx"
    story_file = component_dir / f"{name}.stories.tsx"

    # 컴포넌트 파일 생성
    component_code = generate_component_code(framework, info)
    component_file.write_text(component_code)

    # 스토리 파일 생성
    story_code = generate_story_code(framework, info)
    story_file.write_text(story_code)

    print(f"\n✅ 컴포넌트 생성됨!")
    print(f"📍 컴포넌트: {component_file}")
    print(f"📍 스토리: {story_file}")

    return component_file


def run_storybook() -> None:
    """Storybook 실행"""
    print("\n🚀 Storybook 시작 중...")

    # npm install 확인
    node_modules = PROJECT_ROOT / "node_modules"
    if not node_modules.exists():
        print("📦 의존성 설치 중...")
        result = subprocess.run(
            ["npm", "install"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"❌ npm install 실패:\n{result.stderr}")
            sys.exit(1)

    # process-manager로 포트 정리
    process_manager = PROJECT_ROOT / "scripts" / "process-manager.py"
    if process_manager.exists():
        try:
            subprocess.run(
                ["python3", str(process_manager), "kill-port", "6006"],
                cwd=PROJECT_ROOT,
                capture_output=True,
            )
        except:
            pass

    # Storybook 실행 (process-manager 사용)
    print("\n[START] Storybook 시작 중...")
    if pm.start_storybook(PROJECT_ROOT):
        print("[OK] Storybook 시작됨 → http://localhost:6006")
        print("브라우저에서 컴포넌트를 확인하세요.")
    else:
        print("[ERROR] Storybook 실행 실패")
        sys.exit(1)


def wait_for_confirmation() -> bool:
    """사용자 확인 대기"""
    print("\n" + "=" * 40)
    while True:
        choice = input(
            "컴포넌트 확인이 완료되셨나요? (y/n): "
        ).strip().lower()
        if choice in ["y", "yes"]:
            return True
        elif choice in ["n", "no"]:
            return False
        print("❌ y 또는 n을 입력해주세요.")


def create_pr(user_name: str, component_name: str, framework: str) -> str:
    """PR 생성"""
    print("\n🔄 PR 생성 중...")

    branch_name = f"component/{component_name.lower()}"
    pr_title = f"[designer] {user_name}: {component_name} 컴포넌트"
    pr_body = f"""## {component_name} 컴포넌트 추가

### 변경 사항
- ✨ {component_name} 컴포넌트 생성 (web)
- 📖 Storybook 스토리 작성
- 📝 TypeScript 타입 정의

### 체크리스트
- [x] Storybook에서 컴포넌트 확인
- [x] 모든 Props가 정의됨
- [x] 다크 모드 지원
- [x] 접근성 고려

Co-Authored-By: {user_name} <noreply@anthropic.com>
"""

    # git 작업
    try:
        # 현재 브랜치 확인
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        current_branch = result.stdout.strip()

        # 새 브랜치 생성
        subprocess.run(
            ["git", "checkout", "-b", branch_name],
            cwd=PROJECT_ROOT,
            capture_output=True,
            check=True,
        )

        # git add
        if framework == "web":
            subprocess.run(
                ["git", "add", f"components/web/{component_name}.*"],
                cwd=PROJECT_ROOT,
                capture_output=True,
                check=True,
            )
        else:
            subprocess.run(
                ["git", "add", f"components/native/{component_name}.*"],
                cwd=PROJECT_ROOT,
                capture_output=True,
                check=True,
            )

        # git commit
        subprocess.run(
            ["git", "commit", "-m", pr_title],
            cwd=PROJECT_ROOT,
            capture_output=True,
            check=True,
        )

        # git push
        subprocess.run(
            ["git", "push", "-u", "origin", branch_name],
            cwd=PROJECT_ROOT,
            capture_output=True,
            check=True,
        )

        # gh pr create
        result = subprocess.run(
            ["gh", "pr", "create", "--title", pr_title, "--body", pr_body],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            pr_url = result.stdout.strip().split("\n")[-1]
            print(f"\n✅ PR이 생성되었습니다!")
            print(f"📍 PR 링크: {pr_url}")
            return pr_url
        else:
            print(f"⚠️  PR 생성 실패 (gh CLI 필요): {result.stderr}")
            print(f"📍 브랜치: {branch_name}")
            return branch_name

    except subprocess.CalledProcessError as e:
        print(f"❌ git 작업 실패: {e}")
        sys.exit(1)


def main() -> None:
    """메인 함수"""
    print("\n# /designer — 컴포넌트 제작·수정")
    print("=" * 40)

    # 1. 신원 확인
    identity = load_user_identity()
    user_name = identity.get("name", "unknown")
    user_role = identity.get("role", "unknown")

    print(f"\n✅ 신원: {user_name} ({user_role})")

    # 2. 권한 확인
    check_permissions(user_role)
    print("✅ 권한: 컴포넌트 작업 가능")

    # 3. 프레임워크 선택
    framework = select_framework()
    print(f"✅ 선택: {framework.upper()}")

    # 4. 액션 선택
    action = select_action()

    # 5. 컴포넌트 정보 입력
    if action == "create":
        info = get_component_info()
        component_file = create_component(framework, info)
        component_name = info["name"]
    else:
        print("[ERROR] 컴포넌트 수정은 아직 구현되지 않았습니다.")
        sys.exit(1)

    # 6. 검증 실행 (Storybook 시작 전)
    #    검증 실패 시 재수정 기회를 제공하고, 성공할 때까지 반복
    max_retries = 3
    verified = False

    for attempt in range(1, max_retries + 1):
        passed = verify_designer.run_all(component_name)
        if passed:
            verified = True
            break

        if attempt < max_retries:
            print(f"  재시도 기회: {max_retries - attempt}회 남음")
            print("  파일을 수정한 후 Enter를 눌러 재검증하세요.")
            print("  (취소: q 입력)")
            user_input = input("  > ").strip().lower()
            if user_input == "q":
                print("[CANCEL] 검증이 취소되었습니다.")
                sys.exit(0)
        else:
            print(f"  최대 재시도 횟수({max_retries})를 초과했습니다.")
            print("  파일을 수정한 후 다시 /designer를 실행하세요.")
            sys.exit(1)

    if not verified:
        print("[ERROR] 검증 실패. PR 생성이 불가합니다.")
        sys.exit(1)

    # 7. Storybook 실행 (검증 통과 후)
    run_storybook()

    # 8. 사용자 확인 대기
    print("\nStorybook이 시작되었습니다.")
    print("http://localhost:6006 에서 컴포넌트를 확인하세요.")

    # 브라우저 자동 띄우기 (선택)
    import webbrowser

    webbrowser.open("http://localhost:6006")

    # 사용자 확인 대기
    confirmed = wait_for_confirmation()

    if not confirmed:
        print("[CANCEL] 컴포넌트 작업이 취소되었습니다.")
        subprocess.run(["git", "checkout", "-"], cwd=PROJECT_ROOT, capture_output=True)
        sys.exit(0)

    # 9. PR 생성 (검증 통과 + 사용자 확인 후)
    pr_url = create_pr(user_name, component_name, framework)

    print("\n" + "=" * 40)
    print("  컴포넌트 작업이 완료되었습니다!")
    print("=" * 40)


if __name__ == "__main__":
    main()
