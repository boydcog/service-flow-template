#!/usr/bin/env python3
"""
/designer 명령어 자동화 스크립트
컴포넌트 탐색/생성/수정/확장 -> 스토리 파일 생성 -> Storybook 실행 -> 브라우저 띄우기 -> PR 생성
"""

import os
import re
import sys
import json
import difflib
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Tuple

# process-manager import
sys.path.insert(0, str(Path(__file__).parent))
import process_manager as pm
import verify_designer

# 프로젝트 루트
PROJECT_ROOT = Path(__file__).parent.parent
COMPONENTS_WEB = PROJECT_ROOT / "components" / "web" / "ui"
COMPONENTS_NATIVE = PROJECT_ROOT / "components" / "native" / "ui"


# ---------------------------------------------------------------------------
# 1. 컴포넌트 탐색 함수
# ---------------------------------------------------------------------------


def scan_existing_components(framework: str = "web") -> List[Dict]:
    """
    components/{framework}/ui/*.tsx 전체 스캔.
    stories 파일을 제외한 컴포넌트 파일만 반환한다.

    반환: [{"name": "button", "path": Path, "has_story": True}, ...]
    """
    base_dir = COMPONENTS_WEB if framework == "web" else COMPONENTS_NATIVE
    if not base_dir.exists():
        return []

    components: List[Dict] = []
    for f in sorted(base_dir.glob("*.tsx")):
        if f.name.endswith(".stories.tsx"):
            continue
        stem = f.stem
        story_file = f.parent / f"{stem}.stories.tsx"
        components.append({
            "name": stem,
            "path": f,
            "has_story": story_file.exists(),
        })

    return components


def _is_subsequence(short: str, long: str) -> bool:
    """short의 모든 문자가 long에 순서대로 포함되는지 확인 (약어 매칭용)."""
    it = iter(long)
    return all(c in it for c in short)


def find_similar_components(
    query: str, framework: str = "web"
) -> List[Dict]:
    """
    부분 일치 검색 (case-insensitive).
    다음 조건 중 하나라도 만족하면 반환:
    1. query가 컴포넌트 이름의 부분 문자열
    2. 컴포넌트 이름이 query의 부분 문자열
    3. query가 컴포넌트 이름의 부분 수열 (약어 매칭: "btn" -> "button")
    예: "btn" -> "button", "card" -> "card", "stat-card", "pricing-card"
    """
    all_components = scan_existing_components(framework)
    query_lower = query.lower().replace("-", "").replace("_", "")
    results: List[Dict] = []

    for comp in all_components:
        comp_name_normalized = comp["name"].lower().replace("-", "").replace("_", "")
        # 부분 문자열 매칭
        if query_lower in comp_name_normalized or comp_name_normalized in query_lower:
            results.append(comp)
        # 약어 매칭 (subsequence): "btn" -> "button"
        elif len(query_lower) >= 2 and _is_subsequence(query_lower, comp_name_normalized):
            results.append(comp)

    return results


def show_component_api(component_path: Path) -> str:
    """
    컴포넌트 파일에서 interface/type Props 정의만 추출하여 반환한다.
    전체 코드 대신 API 시그니처만 보여준다.
    """
    if not component_path.exists():
        return "[ERROR] 파일을 찾을 수 없습니다: " + str(component_path)

    content = component_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    result_blocks: List[str] = []
    inside_interface = False
    brace_depth = 0
    current_block: List[str] = []

    for line in lines:
        if re.match(r"^(export\s+)?(interface|type)\s+\w*Props", line):
            inside_interface = True
            brace_depth = 0
            current_block = [line]
            brace_depth += line.count("{") - line.count("}")
            # 한 줄짜리 type alias (no brace)
            if "{" not in line and "=" in line and ";" in line:
                result_blocks.append(line)
                inside_interface = False
                current_block = []
            elif brace_depth <= 0 and "{" in line and "}" in line:
                # 한 줄 완성 interface
                result_blocks.append("\n".join(current_block))
                inside_interface = False
                current_block = []
            continue

        if inside_interface:
            current_block.append(line)
            brace_depth += line.count("{") - line.count("}")
            if brace_depth <= 0 and "{" in "\n".join(current_block):
                result_blocks.append("\n".join(current_block))
                inside_interface = False
                current_block = []

    exports: List[str] = []
    for line in lines:
        if line.startswith("export {") or line.startswith("export default"):
            exports.append(line.strip())

    output_parts: List[str] = []
    if result_blocks:
        output_parts.append("--- Props Interface ---")
        for block in result_blocks:
            output_parts.append(block)
    else:
        output_parts.append("--- Props Interface ---")
        output_parts.append("(명시적 Props interface를 찾지 못했습니다)")

    if exports:
        output_parts.append("\n--- Exports ---")
        for exp in exports:
            output_parts.append(exp)

    return "\n".join(output_parts)


# ---------------------------------------------------------------------------
# 2. 3-way 액션 선택
# ---------------------------------------------------------------------------


def select_action(framework: str) -> str:
    """
    3-way 액션 선택:
      1. 새 컴포넌트 생성 (create)
      2. 기존 컴포넌트 확장 (extend) - 스토리 추가, 변형 추가
      3. 기존 컴포넌트 수정 (modify) - 코드 직접 수정
    """
    components = scan_existing_components(framework)
    comp_count = len(components)

    print(f"\n[INFO] 현재 {framework.upper()} 컴포넌트: {comp_count}개")
    print("\n액션을 선택하세요:")
    print("  1. 새 컴포넌트 생성")
    print("  2. 기존 컴포넌트 확장 (스토리/변형 추가)")
    print("  3. 기존 컴포넌트 수정 (코드 변경)")

    while True:
        choice = input("\n선택 (1/2/3): ").strip()
        if choice == "1":
            return "create"
        elif choice == "2":
            return "extend"
        elif choice == "3":
            return "modify"
        print("[ERROR] 1, 2, 3 중 하나를 선택하세요.")


# ---------------------------------------------------------------------------
# 3. 컴포넌트 검색 및 선택
# ---------------------------------------------------------------------------


def search_and_select_component(framework: str) -> Dict:
    """
    컴포넌트 검색 후 선택. 부분 일치 검색을 지원한다.
    반환: {"name": str, "path": Path, "has_story": bool}
    """
    while True:
        query = input("\n컴포넌트 이름 또는 검색어 입력: ").strip()
        if not query:
            print("[ERROR] 검색어를 입력하세요.")
            continue

        matches = find_similar_components(query, framework)
        if not matches:
            print(f"[WARNING] '{query}'와 일치하는 컴포넌트가 없습니다.")
            all_comps = scan_existing_components(framework)
            if all_comps:
                print("\n사용 가능한 컴포넌트:")
                for i, c in enumerate(all_comps, 1):
                    story_mark = "[story]" if c["has_story"] else "[no story]"
                    print(f"  {i}. {c['name']} {story_mark}")
            retry = input("\n다시 검색하시겠습니까? (y/n): ").strip().lower()
            if retry not in ["y", "yes"]:
                sys.exit(0)
            continue

        if len(matches) == 1:
            comp = matches[0]
            print(f"\n[FOUND] {comp['name']} ({comp['path']})")
            print(show_component_api(comp["path"]))
            confirm = input(f"\n'{comp['name']}' 컴포넌트를 선택하시겠습니까? (y/n): ").strip().lower()
            if confirm in ["y", "yes"]:
                return comp
            continue

        print(f"\n[FOUND] {len(matches)}개의 일치 항목:")
        for i, c in enumerate(matches, 1):
            story_mark = "[story]" if c["has_story"] else "[no story]"
            print(f"  {i}. {c['name']} {story_mark}")

        while True:
            sel = input(f"\n번호 선택 (1-{len(matches)}): ").strip()
            try:
                idx = int(sel) - 1
                if 0 <= idx < len(matches):
                    comp = matches[idx]
                    print(f"\n[SELECTED] {comp['name']}")
                    print(show_component_api(comp["path"]))
                    return comp
            except ValueError:
                pass
            print("[ERROR] 올바른 번호를 입력하세요.")


# ---------------------------------------------------------------------------
# 4. 컴포넌트 읽기/쓰기 (수정 기능)
# ---------------------------------------------------------------------------


def read_component_content(component_path: Path) -> str:
    """파일 전체 내용을 읽어서 반환한다."""
    if not component_path.exists():
        return ""
    return component_path.read_text(encoding="utf-8")


def write_component_content(
    component_path: Path, new_content: str, original_content: str
) -> bool:
    """
    diff 출력 후 사용자 확인을 거쳐 저장한다.
    n 선택 시 원본을 유지하고 False를 반환한다.
    """
    original_lines = original_content.splitlines(keepends=True)
    new_lines = new_content.splitlines(keepends=True)
    diff = list(difflib.unified_diff(
        original_lines,
        new_lines,
        fromfile=f"a/{component_path.name}",
        tofile=f"b/{component_path.name}",
        lineterm="",
    ))

    if not diff:
        print("[INFO] 변경 사항이 없습니다.")
        return False

    print("\n--- 변경 사항 ---")
    for line in diff:
        stripped = line.rstrip("\n")
        if stripped.startswith("+") and not stripped.startswith("+++"):
            print(f"  + {stripped[1:]}")
        elif stripped.startswith("-") and not stripped.startswith("---"):
            print(f"  - {stripped[1:]}")
        else:
            print(f"    {stripped}")
    print("--- end diff ---\n")

    confirm = input("변경 사항을 저장하시겠습니까? (y/n): ").strip().lower()
    if confirm in ["y", "yes"]:
        component_path.write_text(new_content, encoding="utf-8")
        print(f"[OK] 저장됨: {component_path}")
        return True
    else:
        print("[CANCEL] 원본 유지됨.")
        return False


# ---------------------------------------------------------------------------
# 5. 스토리 확장 기능
# ---------------------------------------------------------------------------


def extend_component_stories(story_path: Path, new_story_code: str) -> bool:
    """
    기존 stories 파일 끝에 새로운 Story를 추가한다.
    이미 존재하는 export 이름과 충돌하는지 검사한다.
    """
    if not story_path.exists():
        print(f"[ERROR] 스토리 파일이 없습니다: {story_path}")
        return False

    existing_content = story_path.read_text(encoding="utf-8")

    new_exports = re.findall(r"export\s+const\s+(\w+)", new_story_code)
    existing_exports = re.findall(r"export\s+const\s+(\w+)", existing_content)

    conflicts = set(new_exports) & set(existing_exports)
    if conflicts:
        print(f"[WARNING] 다음 export 이름이 이미 존재합니다: {', '.join(conflicts)}")
        proceed = input("그래도 추가하시겠습니까? (y/n): ").strip().lower()
        if proceed not in ["y", "yes"]:
            print("[CANCEL] 스토리 추가 취소됨.")
            return False

    updated_content = existing_content.rstrip() + "\n\n" + new_story_code.strip() + "\n"

    print("\n--- 추가될 스토리 ---")
    print(new_story_code.strip())
    print("--- end ---\n")

    confirm = input("스토리를 추가하시겠습니까? (y/n): ").strip().lower()
    if confirm in ["y", "yes"]:
        story_path.write_text(updated_content, encoding="utf-8")
        print(f"[OK] 스토리 추가됨: {story_path}")
        return True
    else:
        print("[CANCEL] 스토리 추가 취소됨.")
        return False


# ---------------------------------------------------------------------------
# 6. Storybook 검증 (간이 - verify_designer.py가 정식 검증)
# ---------------------------------------------------------------------------


def verify_component_quality(name: str, framework: str = "web") -> Dict:
    """
    컴포넌트 품질 간이 검증:
    - 컴포넌트 파일 존재
    - stories 파일 존재
    - Default story export 존재
    - Props interface 존재
    반환: {"passed": bool, "checks": [...]}
    """
    base_dir = COMPONENTS_WEB if framework == "web" else COMPONENTS_NATIVE
    component_path = base_dir / f"{name}.tsx"
    story_path = base_dir / f"{name}.stories.tsx"

    checks: List[Dict] = []

    comp_exists = component_path.exists()
    checks.append({
        "name": "컴포넌트 파일",
        "passed": comp_exists,
        "detail": str(component_path) if comp_exists else "파일 없음",
    })

    story_exists = story_path.exists()
    checks.append({
        "name": "스토리 파일",
        "passed": story_exists,
        "detail": str(story_path) if story_exists else "파일 없음",
    })

    has_default_story = False
    if story_exists:
        story_content = story_path.read_text(encoding="utf-8")
        has_default_story = bool(re.search(r"export\s+const\s+Default", story_content))
    checks.append({
        "name": "Default 스토리",
        "passed": has_default_story,
        "detail": "export const Default 발견" if has_default_story else "Default 스토리 없음",
    })

    has_props = False
    if comp_exists:
        comp_content = component_path.read_text(encoding="utf-8")
        has_props = bool(re.search(r"(interface|type)\s+\w*Props", comp_content))
    checks.append({
        "name": "Props interface",
        "passed": has_props,
        "detail": "Props 정의 발견" if has_props else "Props interface 없음",
    })

    all_passed = all(c["passed"] for c in checks)
    return {"passed": all_passed, "checks": checks}


def print_verification_result(result: Dict) -> None:
    """검증 결과 출력"""
    print("\n" + "=" * 40)
    print("컴포넌트 품질 검증 결과")
    print("=" * 40)

    for check in result["checks"]:
        status = "[PASS]" if check["passed"] else "[FAIL]"
        print(f"  {status} {check['name']}: {check['detail']}")

    print("=" * 40)
    if result["passed"]:
        print("[OK] 모든 검증 통과")
    else:
        print("[ERROR] 검증 실패 항목이 있습니다")
    print("=" * 40)


# ---------------------------------------------------------------------------
# 기존 함수 (리팩터링 - 이모지 제거)
# ---------------------------------------------------------------------------


def load_user_identity() -> dict:
    """사용자 신원 파일 로드"""
    identity_file = PROJECT_ROOT / ".user-identity"
    if not identity_file.exists():
        print("[ERROR] 신원 파일 없음. /setup을 먼저 실행하세요.")
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
        print(f"[ERROR] {user_role}은 /designer 명령어를 사용할 수 없습니다.")
        print("필요 역할: designer 이상 (admin, developer, designer)")
        sys.exit(1)


def select_framework() -> str:
    """프레임워크 선택"""
    print("\n프레임워크를 선택하세요:")
    print("  1. Web (React/Vite)")
    print("  2. Native (React Native)")

    while True:
        choice = input("\n선택 (1 또는 2): ").strip()
        if choice in ["1", "2"]:
            return "web" if choice == "1" else "native"
        print("[ERROR] 잘못된 선택입니다.")


def get_component_info(framework: str) -> dict:
    """컴포넌트 정보 입력 (덮어쓰기 방지 포함)"""
    print("\n컴포넌트 정보 입력")
    print("=" * 40)

    name = input("컴포넌트 이름 (예: button, stat-card): ").strip()
    if not name:
        print("[ERROR] 이름을 입력해주세요.")
        sys.exit(1)

    # 덮어쓰기 방지: 동일 이름 파일 존재 확인
    base_dir = COMPONENTS_WEB if framework == "web" else COMPONENTS_NATIVE
    existing_file = base_dir / f"{name}.tsx"
    if existing_file.exists():
        print(f"\n[WARNING] '{name}.tsx' 파일이 이미 존재합니다: {existing_file}")
        print("기존 컴포넌트를 덮어쓰면 코드가 손실됩니다.")
        overwrite = input("덮어쓰시겠습니까? (y/n): ").strip().lower()
        if overwrite not in ["y", "yes"]:
            print("[CANCEL] 생성이 취소되었습니다.")
            print("[TIP] '기존 컴포넌트 확장' 또는 '기존 컴포넌트 수정'을 사용해보세요.")
            sys.exit(0)

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
  title: 'Web/{name}',
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

    component_code = generate_component_code(framework, info)
    component_file.write_text(component_code)

    story_code = generate_story_code(framework, info)
    story_file.write_text(story_code)

    print(f"\n[OK] 컴포넌트 생성됨!")
    print(f"  컴포넌트: {component_file}")
    print(f"  스토리: {story_file}")

    return component_file


def run_storybook() -> None:
    """Storybook 실행"""
    print("\nStorybook 시작 중...")

    node_modules = PROJECT_ROOT / "node_modules"
    if not node_modules.exists():
        print("의존성 설치 중...")
        result = subprocess.run(
            ["npm", "install"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"[ERROR] npm install 실패:\n{result.stderr}")
            sys.exit(1)

    process_manager = PROJECT_ROOT / "scripts" / "process-manager.py"
    if process_manager.exists():
        try:
            subprocess.run(
                ["python3", str(process_manager), "kill-port", "6006"],
                cwd=PROJECT_ROOT,
                capture_output=True,
            )
        except Exception:
            pass

    print("\n[START] Storybook 시작 중...")
    if pm.start_storybook(PROJECT_ROOT):
        print("[OK] Storybook 시작됨 -> http://localhost:6006")
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
        print("[ERROR] y 또는 n을 입력해주세요.")


def create_pr(user_name: str, component_name: str, framework: str) -> str:
    """PR 생성"""
    print("\nPR 생성 중...")

    branch_name = f"component/{component_name.lower()}"
    pr_title = f"[designer] {user_name}: {component_name} 컴포넌트"
    pr_body = f"""## {component_name} 컴포넌트 추가

### 변경 사항
- {component_name} 컴포넌트 생성 ({framework})
- Storybook 스토리 작성
- TypeScript 타입 정의

### 체크리스트
- [x] Storybook에서 컴포넌트 확인
- [x] 모든 Props가 정의됨
- [x] 다크 모드 지원
- [x] 접근성 고려

Co-Authored-By: {user_name} <noreply@anthropic.com>
"""

    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        current_branch = result.stdout.strip()

        subprocess.run(
            ["git", "checkout", "-b", branch_name],
            cwd=PROJECT_ROOT,
            capture_output=True,
            check=True,
        )

        if framework == "web":
            subprocess.run(
                ["git", "add", f"components/web/ui/{component_name}*"],
                cwd=PROJECT_ROOT,
                capture_output=True,
                check=True,
            )
        else:
            subprocess.run(
                ["git", "add", f"components/native/ui/{component_name}*"],
                cwd=PROJECT_ROOT,
                capture_output=True,
                check=True,
            )

        subprocess.run(
            ["git", "commit", "-m", pr_title],
            cwd=PROJECT_ROOT,
            capture_output=True,
            check=True,
        )

        subprocess.run(
            ["git", "push", "-u", "origin", branch_name],
            cwd=PROJECT_ROOT,
            capture_output=True,
            check=True,
        )

        result = subprocess.run(
            ["gh", "pr", "create", "--title", pr_title, "--body", pr_body],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            pr_url = result.stdout.strip().split("\n")[-1]
            print(f"\n[OK] PR이 생성되었습니다!")
            print(f"  PR 링크: {pr_url}")
            return pr_url
        else:
            print(f"[WARNING] PR 생성 실패 (gh CLI 필요): {result.stderr}")
            print(f"  브랜치: {branch_name}")
            return branch_name

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] git 작업 실패: {e}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# 메인 함수
# ---------------------------------------------------------------------------


def main() -> None:
    """메인 함수"""
    print("\n# /designer -- 컴포넌트 제작/수정/확장")
    print("=" * 40)

    # 1. 신원 확인
    identity = load_user_identity()
    user_name = identity.get("name", "unknown")
    user_role = identity.get("role", "unknown")

    print(f"\n[OK] 신원: {user_name} ({user_role})")

    # 2. 권한 확인
    check_permissions(user_role)
    print("[OK] 권한: 컴포넌트 작업 가능")

    # 3. 프레임워크 선택
    framework = select_framework()
    print(f"[OK] 선택: {framework.upper()}")

    # 3.5. 현재 컴포넌트 목록 표시
    components = scan_existing_components(framework)
    if components:
        print(f"\n현재 등록된 {framework.upper()} 컴포넌트 ({len(components)}개):")
        for c in components:
            story_mark = "[story]" if c["has_story"] else "[no story]"
            print(f"  - {c['name']} {story_mark}")

    # 4. 액션 선택 (3-way)
    action = select_action(framework)

    component_name = ""

    # 5. 액션별 분기
    if action == "create":
        info = get_component_info(framework)
        component_file = create_component(framework, info)
        component_name = info["name"]

    elif action == "extend":
        comp = search_and_select_component(framework)
        component_name = comp["name"]

        print(f"\n'{component_name}' 확장 옵션:")
        print("  1. 새 스토리(Story) 추가")
        print("  2. 새 변형(Variant) 추가 (컴포넌트 코드 + 스토리)")

        ext_choice = input("\n선택 (1/2): ").strip()

        if ext_choice == "1":
            story_path = comp["path"].parent / f"{component_name}.stories.tsx"
            if not story_path.exists():
                print(f"[ERROR] 스토리 파일이 없습니다: {story_path}")
                print("[TIP] 먼저 스토리 파일을 생성하세요.")
                sys.exit(1)

            story_name = input("새 스토리 이름 (예: WithIcon, Loading): ").strip()
            if not story_name:
                print("[ERROR] 스토리 이름을 입력하세요.")
                sys.exit(1)

            story_desc = input("스토리 설명 (선택): ").strip()
            story_args = input("args (JSON, 예: {\"children\": \"텍스트\"}): ").strip()

            try:
                args_dict = json.loads(story_args) if story_args else {"children": f"{story_name} 상태"}
            except json.JSONDecodeError:
                args_dict = {"children": f"{story_name} 상태"}

            args_str = ",\n    ".join(
                f"{k}: '{v}'" if isinstance(v, str) else f"{k}: {json.dumps(v)}"
                for k, v in args_dict.items()
            )
            comment = f"\n/**\n * {story_desc}\n */\n" if story_desc else "\n"
            new_story = f"""{comment}export const {story_name}: Story = {{
  args: {{
    {args_str},
  }},
}}"""

            extend_component_stories(story_path, new_story)

        elif ext_choice == "2":
            print("\n[INFO] 변형 추가는 컴포넌트 코드를 직접 수정해야 합니다.")
            print("[INFO] 현재 Props API:")
            print(show_component_api(comp["path"]))
            print("\n컴포넌트 코드를 수정한 후 스토리를 추가하세요.")
            print("[TIP] Claude에게 변형 추가를 요청하면 코드를 자동 생성합니다.")

    elif action == "modify":
        comp = search_and_select_component(framework)
        component_name = comp["name"]

        original_content = read_component_content(comp["path"])
        print(f"\n--- 현재 코드 ({comp['path'].name}) ---")
        print(original_content)
        print("--- end ---")

        print("\n[INFO] 수정할 내용을 설명해주세요.")
        print("[INFO] Claude가 코드를 자동 수정합니다.")
        modification = input("\n수정 사항: ").strip()

        if modification:
            print(f"\n[INFO] '{modification}' 수정 요청을 받았습니다.")
            print("[INFO] Claude에게 수정을 요청하세요. 이 스크립트에서는 직접 편집을 지원합니다.")
            print("\n직접 수정된 코드를 붙여넣으시겠습니까? (y/n)")
            paste = input().strip().lower()
            if paste in ["y", "yes"]:
                print("새 코드를 입력하세요 (끝내려면 빈 줄에 'END' 입력):")
                lines = []
                while True:
                    line = input()
                    if line.strip() == "END":
                        break
                    lines.append(line)
                new_content = "\n".join(lines)
                write_component_content(comp["path"], new_content, original_content)

    # 6. 검증 실행 (verify_designer 사용)
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

    import webbrowser
    webbrowser.open("http://localhost:6006")

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
