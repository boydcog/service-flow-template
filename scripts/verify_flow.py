#!/usr/bin/env python3
"""
/flow 검증 자동화 스크립트
플로우 생성 후 품질 검증을 수행합니다.

검증 항목:
1. import 경로 모두 실제 존재
2. import한 컴포넌트 모두 JSX에서 사용
3. header/navbar/sidebar 최소 1개 사용 (레이아웃 검증)
4. TypeScript 컴파일 에러 0개
"""

import re
import subprocess
from pathlib import Path
from typing import List, Tuple

# 프로젝트 루트
PROJECT_ROOT = Path(__file__).parent.parent


def _get_tsx_files(flow_dir: Path) -> List[Path]:
    """플로우 디렉토리 내 모든 .tsx 파일 반환"""
    tsx_files: List[Path] = []
    if not flow_dir.exists():
        return tsx_files
    for f in flow_dir.rglob("*.tsx"):
        tsx_files.append(f)
    return tsx_files


def _parse_imports(content: str) -> List[dict]:
    """import 구문 파싱 -> [{names: [str], path: str}]"""
    imports: List[dict] = []

    # import { A, B } from 'path' 또는 import X from 'path'
    pattern = re.compile(
        r"""import\s+(?:"""
        r"""(?:\{([^}]*)\})|"""         # named imports: { A, B }
        r"""(\w+)|"""                    # default import: X
        r"""(?:\*\s+as\s+(\w+))"""      # namespace: * as X
        r""")\s*(?:,\s*\{([^}]*)\})?\s*from\s*['"]([^'"]+)['"]""",
        re.MULTILINE,
    )

    for match in pattern.finditer(content):
        named = match.group(1) or ""
        default_name = match.group(2) or ""
        namespace = match.group(3) or ""
        extra_named = match.group(4) or ""
        import_path = match.group(5)

        names: List[str] = []
        if default_name:
            names.append(default_name)
        if namespace:
            names.append(namespace)
        for block in [named, extra_named]:
            for item in block.split(","):
                item = item.strip()
                if item:
                    # 'type X' import 건너뛰기
                    if item.startswith("type "):
                        continue
                    # 'X as Y' -> Y 사용
                    if " as " in item:
                        item = item.split(" as ")[1].strip()
                    names.append(item)

        if names and import_path:
            imports.append({"names": names, "path": import_path})

    return imports


def verify_imports_exist(flow_dir: Path) -> Tuple[bool, str]:
    """import 경로 모두 실제 존재하는지 확인

    상대 경로 (./, ../)와 alias 경로 (@components/ 등)를 모두 확인합니다.
    node_modules 패키지(react, next 등)는 건너뜁니다.
    """
    tsx_files = _get_tsx_files(flow_dir)
    if not tsx_files:
        return False, "플로우 디렉토리에 .tsx 파일 없음"

    missing: List[str] = []

    for tsx_file in tsx_files:
        content = tsx_file.read_text()
        imports = _parse_imports(content)

        for imp in imports:
            path = imp["path"]

            # node_modules 패키지 건너뛰기 (상대 경로가 아니고 alias도 아닌 경우)
            if not path.startswith(".") and not path.startswith("@components"):
                continue

            # alias 경로 해석
            if path.startswith("@components/"):
                resolved = PROJECT_ROOT / "components" / path[len("@components/"):]
            else:
                resolved = (tsx_file.parent / path).resolve()

            # .tsx, .ts, /index.tsx, /index.ts 순서로 확인
            found = False
            for suffix in ["", ".tsx", ".ts", "/index.tsx", "/index.ts"]:
                candidate = Path(str(resolved) + suffix)
                if candidate.exists():
                    found = True
                    break

            if not found:
                rel_tsx = tsx_file.relative_to(flow_dir)
                missing.append(f"{rel_tsx}: import '{path}' -> 파일 없음")

    if not missing:
        return True, "모든 import 경로 존재 확인됨"
    return False, "존재하지 않는 import:\n    " + "\n    ".join(missing)


def verify_imports_used(flow_dir: Path) -> Tuple[bool, str]:
    """import한 컴포넌트 모두 JSX에서 사용되는지 확인"""
    tsx_files = _get_tsx_files(flow_dir)
    if not tsx_files:
        return False, "플로우 디렉토리에 .tsx 파일 없음"

    unused: List[str] = []

    for tsx_file in tsx_files:
        content = tsx_file.read_text()
        imports = _parse_imports(content)

        # import 구문 이후의 코드 부분 추출
        # 모든 import 구문을 제거한 나머지 코드에서 사용 여부 확인
        code_without_imports = re.sub(
            r"^import\s+.*?from\s+['\"].*?['\"];?\s*$",
            "",
            content,
            flags=re.MULTILINE,
        )

        for imp in imports:
            # node_modules 유틸리티 (React, cn, cva 등)는 건너뛰기
            for name in imp["names"]:
                # React, React.xxx 형태는 특수 처리
                if name == "React":
                    # React.xxx 또는 JSX에서 자동 사용
                    continue

                # 코드 내에서 사용되는지 확인
                # JSX: <Name />, <Name> / 함수 호출: Name(, Name.xxx / 참조: Name,
                pattern = re.compile(r"\b" + re.escape(name) + r"\b")
                if not pattern.search(code_without_imports):
                    rel_tsx = tsx_file.relative_to(flow_dir)
                    unused.append(f"{rel_tsx}: '{name}' import됨, 사용되지 않음")

    if not unused:
        return True, "모든 import가 코드에서 사용됨"
    return False, "사용되지 않는 import:\n    " + "\n    ".join(unused)


def verify_layout_used(flow_dir: Path) -> Tuple[bool, str]:
    """header/navbar/sidebar 최소 1개 사용 확인 (레이아웃 검증)"""
    tsx_files = _get_tsx_files(flow_dir)
    if not tsx_files:
        return False, "플로우 디렉토리에 .tsx 파일 없음"

    layout_components = ["header", "navbar", "sidebar", "nav", "layout", "appbar"]
    found_layouts: List[str] = []

    for tsx_file in tsx_files:
        content = tsx_file.read_text().lower()
        for layout in layout_components:
            # import 또는 JSX에서 레이아웃 컴포넌트 사용 확인
            if re.search(r"(?:import.*" + layout + r"|<" + layout + r")", content, re.IGNORECASE):
                found_layouts.append(layout)

    unique_found = list(set(found_layouts))
    if unique_found:
        return True, f"레이아웃 컴포넌트 사용됨: {', '.join(unique_found)}"
    return False, "레이아웃 컴포넌트 없음 (header, navbar, sidebar 중 최소 1개 필요)"


def verify_tsc_clean(project_path: Path) -> Tuple[bool, str]:
    """TypeScript 컴파일 에러 0개 확인"""
    try:
        result = subprocess.run(
            ["npx", "tsc", "--noEmit", "--pretty", "false"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            return True, "TypeScript 컴파일 에러 없음"

        # 에러 메시지에서 라인 수 추출
        errors = result.stdout.strip().split("\n") if result.stdout.strip() else []
        stderr_lines = result.stderr.strip().split("\n") if result.stderr.strip() else []
        all_errors = [line for line in (errors + stderr_lines) if line.strip()]
        error_count = len([line for line in all_errors if "error TS" in line])

        if error_count == 0:
            # tsc가 실패했지만 TS 에러가 아닌 경우 (설정 문제 등)
            return False, f"TypeScript 실행 실패: {result.stderr[:200]}"

        # 최대 5개 에러만 표시
        shown_errors = all_errors[:5]
        suffix = f" (외 {error_count - 5}개)" if error_count > 5 else ""
        return False, f"TypeScript 에러 {error_count}개{suffix}:\n    " + "\n    ".join(shown_errors)

    except subprocess.TimeoutExpired:
        return False, "TypeScript 컴파일 타임아웃 (60초 초과)"
    except FileNotFoundError:
        return False, "npx/tsc를 찾을 수 없음 (Node.js 설치 필요)"
    except Exception as e:
        return False, f"TypeScript 컴파일 확인 실패: {e}"


def run_all(flow_dir: str | Path, project_path: str | Path) -> bool:
    """전체 검증 실행 -> bool

    모든 검증 항목을 순서대로 실행하고 결과를 출력합니다.
    모든 항목이 통과해야 True를 반환합니다.
    """
    flow_dir = Path(flow_dir)
    project_path = Path(project_path)

    checks = [
        ("import 경로 존재", verify_imports_exist, [flow_dir]),
        ("import 사용 확인", verify_imports_used, [flow_dir]),
        ("레이아웃 사용", verify_layout_used, [flow_dir]),
        ("TypeScript 검증", verify_tsc_clean, [project_path]),
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

    if len(sys.argv) < 3:
        print("Usage: verify_flow.py <flow_dir> <project_path>")
        print("Example: verify_flow.py flows/my-app projects/my-app")
        sys.exit(1)

    flow_dir = sys.argv[1]
    project_path = sys.argv[2]
    success = run_all(flow_dir, project_path)
    sys.exit(0 if success else 1)
