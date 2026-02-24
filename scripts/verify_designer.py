#!/usr/bin/env python3
"""
/designer 검증 자동화 스크립트
컴포넌트 생성 후 품질 검증을 수행합니다.

검증 항목:
1. 컴포넌트 파일 존재 확인
2. 스토리 파일 존재 확인
3. Default 스토리 export 확인
4. Props interface/type 정의 확인
5. any 타입 사용 금지 확인
6. Storybook 실행 상태 확인
"""

import re
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Tuple

# 프로젝트 루트
PROJECT_ROOT = Path(__file__).parent.parent
COMPONENTS_WEB = PROJECT_ROOT / "components" / "web"
COMPONENTS_NATIVE = PROJECT_ROOT / "components" / "native"


def _find_component_file(component_name: str) -> Path | None:
    """컴포넌트 파일 탐색 (web/ui, web, native/ui, native 순)"""
    candidates = [
        COMPONENTS_WEB / "ui" / f"{component_name}.tsx",
        COMPONENTS_WEB / f"{component_name}.tsx",
        COMPONENTS_NATIVE / "ui" / f"{component_name}.tsx",
        COMPONENTS_NATIVE / f"{component_name}.tsx",
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def _find_story_file(component_name: str) -> Path | None:
    """스토리 파일 탐색 (web/ui, web, native/ui, native 순)"""
    candidates = [
        COMPONENTS_WEB / "ui" / f"{component_name}.stories.tsx",
        COMPONENTS_WEB / f"{component_name}.stories.tsx",
        COMPONENTS_NATIVE / "ui" / f"{component_name}.stories.tsx",
        COMPONENTS_NATIVE / f"{component_name}.stories.tsx",
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def verify_component_file(component_name: str) -> Tuple[bool, str]:
    """컴포넌트 .tsx 파일 존재 확인"""
    found = _find_component_file(component_name)
    if found:
        return True, f"컴포넌트 파일 존재: {found.relative_to(PROJECT_ROOT)}"
    return False, f"컴포넌트 파일 없음: {component_name}.tsx"


def verify_story_file(component_name: str) -> Tuple[bool, str]:
    """스토리 .stories.tsx 파일 존재 확인"""
    found = _find_story_file(component_name)
    if found:
        return True, f"스토리 파일 존재: {found.relative_to(PROJECT_ROOT)}"
    return False, f"스토리 파일 없음: {component_name}.stories.tsx"


def verify_default_story(component_name: str) -> Tuple[bool, str]:
    """'export const Default' 포함 확인"""
    story_path = _find_story_file(component_name)
    if not story_path:
        return False, "스토리 파일이 없어 Default 스토리 확인 불가"

    content = story_path.read_text()
    if re.search(r"export\s+const\s+Default", content):
        return True, "Default 스토리 export 확인됨"
    return False, "Default 스토리가 없음 (export const Default 필요)"


def verify_props_interface(component_name: str) -> Tuple[bool, str]:
    """Props interface 또는 type 정의 확인"""
    comp_path = _find_component_file(component_name)
    if not comp_path:
        return False, "컴포넌트 파일이 없어 Props 확인 불가"

    content = comp_path.read_text()
    # interface XxxProps 또는 type XxxProps 패턴 검색
    has_interface = re.search(r"(interface|type)\s+\w*Props", content)
    if has_interface:
        return True, f"Props 정의 확인됨: {has_interface.group(0)}"
    return False, "Props interface 또는 type 정의 없음 (interface ...Props 또는 type ...Props 필요)"


def verify_no_any_type(component_name: str) -> Tuple[bool, str]:
    """any 타입 0개 확인 (정규식 검색)"""
    comp_path = _find_component_file(component_name)
    if not comp_path:
        return False, "컴포넌트 파일이 없어 any 타입 확인 불가"

    content = comp_path.read_text()
    # ': any', '<any>', 'as any' 패턴 검색 (주석 제외)
    lines = content.split("\n")
    any_lines: List[int] = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # 주석 라인 건너뛰기
        if stripped.startswith("//") or stripped.startswith("*") or stripped.startswith("/*"):
            continue
        # any 타입 패턴 검색
        if re.search(r":\s*any\b|<any\b|as\s+any\b|\bany\s*\[", stripped):
            any_lines.append(i)

    if not any_lines:
        return True, "any 타입 사용 없음"
    return False, f"any 타입 발견 (라인: {', '.join(str(n) for n in any_lines)})"


def verify_storybook_running() -> Tuple[bool, str]:
    """포트 6006 응답 확인"""
    try:
        req = urllib.request.Request("http://localhost:6006", method="HEAD")
        req.add_header("User-Agent", "verify-designer/1.0")
        response = urllib.request.urlopen(req, timeout=5)
        if response.status == 200:
            return True, "Storybook 실행 중 (포트 6006)"
        return False, f"Storybook 응답 비정상 (HTTP {response.status})"
    except urllib.error.URLError:
        return False, "Storybook 응답 없음 (포트 6006 연결 실패)"
    except Exception as e:
        return False, f"Storybook 확인 실패: {e}"


def run_all(component_name: str) -> bool:
    """전체 검증 실행 -> bool

    모든 검증 항목을 순서대로 실행하고 결과를 출력합니다.
    모든 항목이 통과해야 True를 반환합니다.
    """
    checks = [
        ("컴포넌트 파일", verify_component_file, [component_name]),
        ("스토리 파일", verify_story_file, [component_name]),
        ("Default 스토리", verify_default_story, [component_name]),
        ("Props 정의", verify_props_interface, [component_name]),
        ("any 타입 금지", verify_no_any_type, [component_name]),
        ("Storybook 실행", verify_storybook_running, []),
    ]

    print("")
    print("=" * 48)
    print("  검증 시작 (Strict Mode)")
    print("=" * 48)
    print("")

    all_passed = True
    results: List[Tuple[str, bool, str]] = []

    for label, func, args in checks:
        passed, message = func(*args)
        results.append((label, passed, message))
        if not passed:
            all_passed = False

    # 결과 출력
    for label, passed, message in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status}  {label}: {message}")

    print("")

    if all_passed:
        print("=" * 48)
        print("  검증 완료 (Strict Mode 통과)")
        print("=" * 48)
        print("")
        print("  모든 검증 항목 통과. PR 생성 가능합니다.")
        print("")
    else:
        print("=" * 48)
        print("  검증 실패 (Strict Mode)")
        print("=" * 48)
        print("")
        failed_items = [r for r in results if not r[1]]
        for label, _, message in failed_items:
            print(f"  - {label}: {message}")
        print("")
        print("  위 항목을 수정한 후 재검증하세요.")
        print("")

    return all_passed


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: verify_designer.py <component_name>")
        print("Example: verify_designer.py button")
        sys.exit(1)

    component_name = sys.argv[1]
    success = run_all(component_name)
    sys.exit(0 if success else 1)
