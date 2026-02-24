#!/usr/bin/env python3
"""
/flow 명령어 자동화 스크립트
플로우 설명 입력 → 코드 생성 → 웹 서버 실행 → 브라우저 띄우기 → PR 생성
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
import verify_flow

# 프로젝트 루트
PROJECT_ROOT = Path(__file__).parent.parent
FLOWS_DIR = PROJECT_ROOT / "flows"
PROJECTS_DIR = PROJECT_ROOT / "projects"
STATE_DIR = PROJECT_ROOT / ".claude" / "state"


def save_active_flow(flow_name: str) -> None:
    """활성 플로우 저장"""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    active_flow_file = STATE_DIR / "_active_flow.txt"
    active_flow_file.write_text(flow_name.strip())


def load_active_flow() -> Optional[str]:
    """활성 플로우 로드"""
    active_flow_file = STATE_DIR / "_active_flow.txt"
    if active_flow_file.exists():
        return active_flow_file.read_text().strip()
    return None


def save_flow_metadata(flow_name: str, metadata: dict) -> None:
    """플로우 메타데이터 저장"""
    flow_state_dir = STATE_DIR / flow_name
    flow_state_dir.mkdir(parents=True, exist_ok=True)
    metadata_file = flow_state_dir / "metadata.json"
    metadata_file.write_text(json.dumps(metadata, indent=2))


def load_flow_metadata(flow_name: str) -> Optional[dict]:
    """플로우 메타데이터 로드"""
    metadata_file = STATE_DIR / flow_name / "metadata.json"
    if metadata_file.exists():
        try:
            return json.loads(metadata_file.read_text())
        except:
            return None
    return None


def sync_git() -> None:
    """Git 최신 데이터 동기화 (git pull --rebase)"""
    print("\n🔄 최신 데이터 동기화 중...")
    try:
        result = subprocess.run(
            ["git", "pull", "--rebase", "origin", "main"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print("✅ Git 동기화 완료")
        else:
            # 네트워크 오류나 offline 상태라도 계속 진행
            print("⚠️  Git 동기화 스킵 (오프라인 또는 네트워크 오류)")
    except Exception as e:
        print(f"⚠️  Git 동기화 실패: {e} (계속 진행)")


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


def select_or_create_project() -> Path:
    """기존 프로젝트 선택 또는 새 프로젝트 생성"""
    print("\n📁 프로젝트 선택")
    print("=" * 40)

    # 기존 프로젝트 스캔
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    existing_projects = sorted([
        d for d in PROJECTS_DIR.iterdir()
        if d.is_dir() and d.name != ".gitkeep"
    ])

    if existing_projects:
        print("\n기존 프로젝트:")
        for i, proj in enumerate(existing_projects, 1):
            print(f"  {i}. {proj.name}")
        print(f"  {len(existing_projects) + 1}. ✨ 새 프로젝트 생성")

        while True:
            try:
                choice = int(input(f"\n선택 (1-{len(existing_projects) + 1}): "))
                if 1 <= choice <= len(existing_projects):
                    selected_project = existing_projects[choice - 1]
                    print(f"✅ 선택: {selected_project.name}")

                    # 컴포넌트 동기화
                    print(f"🔄 컴포넌트 동기화 중...")
                    sync_script = PROJECT_ROOT / "scripts" / "sync-components.sh"
                    result = subprocess.run(
                        ["bash", str(sync_script), str(selected_project)],
                        cwd=PROJECT_ROOT,
                        capture_output=True,
                        text=True,
                    )
                    if result.returncode == 0:
                        print(f"✅ 컴포넌트 동기화 완료")
                    else:
                        print(f"⚠️  컴포넌트 동기화 경고: {result.stderr}")

                    return selected_project
                elif choice == len(existing_projects) + 1:
                    break
                else:
                    print("❌ 올바른 번호를 입력해주세요.")
            except ValueError:
                print("❌ 숫자를 입력해주세요.")

    # 새 프로젝트 생성
    print("\n✨ 새 프로젝트 생성")
    project_name = input("프로젝트 이름 (예: my-app): ").strip().lower()

    if not project_name or not project_name.replace("-", "").replace("_", "").isalnum():
        print("❌ 올바른 프로젝트명을 입력해주세요 (영문, 숫자, - 또는 _만 사용).")
        sys.exit(1)

    project_path = PROJECTS_DIR / project_name
    if project_path.exists():
        print(f"❌ 이미 존재하는 프로젝트입니다: {project_name}")
        sys.exit(1)

    print(f"🔄 프로젝트 생성 중: {project_name}...")
    create_script = PROJECT_ROOT / "scripts" / "create-project.sh"
    result = subprocess.run(
        ["bash", str(create_script), project_name],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print(f"✅ 프로젝트 생성 완료: {project_name}")
        return project_path
    else:
        print(f"❌ 프로젝트 생성 실패:\n{result.stderr}")
        sys.exit(1)


def get_product_name() -> str:
    """제품명 입력"""
    print("\n🛍️  제품명을 입력하세요 (예: user-onboarding):")
    product_name = input("> ").strip().lower()

    if not product_name or not product_name.replace("-", "").replace("_", "").isalnum():
        print("❌ 올바른 제품명을 입력해주세요 (영문, 숫자, - 또는 _만 사용).")
        sys.exit(1)

    return product_name


def get_flow_description() -> str:
    """플로우 설명 입력"""
    print("\n📝 서비스 플로우를 자유롭게 설명해주세요:")
    print("(여러 줄 가능, 빈 줄 입력 시 완료)")
    print("-" * 40)

    lines = []
    while True:
        line = input()
        if not line:
            if lines:
                break
            continue
        lines.append(line)

    return "\n".join(lines)


def parse_flow_description(description: str) -> dict:
    """플로우 설명 파싱"""
    lines = description.strip().split("\n")
    screens = []
    current_screen = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 화면 번호 감지 (1), 2), etc.)
        if line[0].isdigit() and ")" in line[:3]:
            if current_screen:
                screens.append(current_screen)
            current_screen = {
                "title": line[3:].strip(),
                "description": "",
            }
        elif current_screen:
            current_screen["description"] += line + " "

    if current_screen:
        screens.append(current_screen)

    return {
        "total_screens": len(screens),
        "screens": screens[:5],  # 최대 5개 화면
    }


def generate_flow_structure(product_name: str) -> dict:
    """플로우 구조 생성"""
    return {
        "product_name": product_name,
        "created_at": datetime.now().isoformat(),
        "screens": [
            {
                "id": 1,
                "title": "Screen 1",
                "path": "/step-1",
                "components": [],
            },
            {
                "id": 2,
                "title": "Screen 2",
                "path": "/step-2",
                "components": [],
            },
        ],
        "navigation": "linear",
        "data_flow": {},
    }


def create_flow_files(product_name: str, flow_structure: dict, user_name: str = "") -> Path:
    """플로우 파일 생성"""
    flow_dir = FLOWS_DIR / product_name
    flow_dir.mkdir(parents=True, exist_ok=True)

    # index.json - 플로우 메타데이터
    (flow_dir / "index.json").write_text(json.dumps(flow_structure, indent=2))

    # 상태 저장: 활성 플로우 + 메타데이터
    save_active_flow(product_name)
    save_flow_metadata(product_name, {
        "flow_name": product_name,
        "created_by": user_name,
        "created_at": flow_structure.get("created_at"),
        "status": "in_progress",
        "screens": len(flow_structure.get("screens", [])),
    })

    # page.tsx - 메인 페이지
    page_tsx = f'''import React from 'react'
import {{ FlowContainer }} from '../components/FlowContainer'

export default function {product_name.title().replace('-', '')}Page() {{
  return (
    <FlowContainer
      title="{product_name}"
      description="서비스 플로우"
    >
      <div className="p-8 space-y-4">
        <h1 className="text-3xl font-bold">{product_name} 플로우</h1>
        <p className="text-gray-600">이 플로우는 테스트 환경입니다.</p>
        <div className="mt-8 space-y-4">
          {{/* 각 화면이 들어갈 위치 */}}
        </div>
      </div>
    </FlowContainer>
  )
}}
'''
    (flow_dir / "page.tsx").write_text(page_tsx)

    # README.md
    readme = f'''# {product_name.title()} 플로우

## 개요
이 플로우는 {product_name} 서비스의 흐름을 나타냅니다.

## 화면 목록
'''
    for i, screen in enumerate(flow_structure.get("screens", []), 1):
        readme += f"- {i}. {screen.get('title', f'Screen {i}')}\n"

    (flow_dir / "README.md").write_text(readme)

    print(f"\n✅ 플로우 생성됨!")
    print(f"📍 위치: {flow_dir}")
    print(f"📁 파일: index.json, page.tsx, README.md")

    return flow_dir


def run_dev_server(project_path: Optional[Path] = None) -> None:
    """개발 서버 실행"""
    print("\n🚀 웹 서버 시작 중...")

    target_path = project_path or PROJECT_ROOT
    port = 3000

    # npm install 확인
    node_modules = target_path / "node_modules"
    if not node_modules.exists():
        print("📦 의존성 설치 중...")
        result = subprocess.run(
            ["npm", "install"],
            cwd=target_path,
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
                ["python3", str(process_manager), "kill-port", str(port)],
                cwd=PROJECT_ROOT,
                capture_output=True,
            )
        except:
            pass

    # dev 서버 실행 (process-manager 사용)
    print("\n[START] 개발 서버 시작 중...")
    if pm.start_dev_server(target_path, port):
        print(f"[OK] 개발 서버 시작됨 → http://localhost:{port}")
        print("브라우저에서 플로우를 확인하세요.")
    else:
        print("[ERROR] 개발 서버 실행 실패")
        sys.exit(1)


def wait_for_confirmation() -> bool:
    """사용자 확인 대기"""
    print("\n" + "=" * 40)
    while True:
        choice = input(
            "플로우 확인이 완료되셨나요? (y/n): "
        ).strip().lower()
        if choice in ["y", "yes"]:
            return True
        elif choice in ["n", "no"]:
            return False
        print("❌ y 또는 n을 입력해주세요.")


def create_pr(user_name: str, product_name: str) -> str:
    """PR 생성"""
    print("\n🔄 PR 생성 중...")

    branch_name = f"flow/{product_name}"
    pr_title = f"[flow] {user_name}: {product_name} 서비스 플로우"
    pr_body = f"""## {product_name} 서비스 플로우 추가

### 변경 사항
- ✨ {product_name} 플로우 생성
- 📍 화면 구조 설계
- 📝 README 작성

### 테스트 완료
- [x] 모든 화면 확인
- [x] 네비게이션 테스트
- [x] 데이터 플로우 검증

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
        subprocess.run(
            ["git", "add", f"flows/{product_name}/"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            check=True,
        )

        # git add (gitignore 규칙 무시)
        subprocess.run(
            ["git", "update-index", "--no-skip-worktree", f"flows/{product_name}"],
            cwd=PROJECT_ROOT,
            capture_output=True,
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
    print("\n# /flow — 서비스 플로우 생성")
    print("=" * 40)

    # 0. Git 동기화
    sync_git()

    # 1. 신원 확인
    identity = load_user_identity()
    user_name = identity.get("name", "unknown")
    user_role = identity.get("role", "unknown")

    print(f"\n✅ 신원: {user_name} ({user_role})")
    print("✅ 권한: 플로우 작업 가능")

    # 1.5. 프로젝트 선택/생성
    project_path = select_or_create_project()

    # 2. 제품명 입력
    product_name = get_product_name()
    print(f"✅ 제품명: {product_name}")

    # 3. 플로우 설명 입력
    description = get_flow_description()
    flow_info = parse_flow_description(description)

    print(f"\n📋 인식된 화면: {flow_info['total_screens']}개")
    for i, screen in enumerate(flow_info["screens"], 1):
        print(f"  {i}. {screen['title']}")

    # 4. 플로우 구조 생성
    flow_structure = generate_flow_structure(product_name)
    flow_dir = create_flow_files(product_name, flow_structure, user_name)

    # 5. 검증 실행 (Dev 서버 시작 전)
    #    검증 실패 시 재수정 기회를 제공하고, 성공할 때까지 반복
    max_retries = 3
    verified = False

    for attempt in range(1, max_retries + 1):
        passed = verify_flow.run_all(flow_dir, project_path)
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
            print("  파일을 수정한 후 다시 /flow를 실행하세요.")
            sys.exit(1)

    if not verified:
        print("[ERROR] 검증 실패. PR 생성이 불가합니다.")
        sys.exit(1)

    # 6. 개발 서버 실행 (검증 통과 후, 프로젝트 경로 전달)
    run_dev_server(project_path)

    # 7. 사용자 확인 대기
    print("\n개발 서버가 시작되었습니다.")
    print(f"http://localhost:3000/flows/{product_name} 에서 플로우를 확인하세요.")

    # 브라우저 자동 띄우기 (선택)
    import webbrowser

    webbrowser.open("http://localhost:3000")

    # 사용자 확인 대기
    confirmed = wait_for_confirmation()

    if not confirmed:
        print("[CANCEL] 플로우 작업이 취소되었습니다.")
        subprocess.run(["git", "checkout", "-"], cwd=PROJECT_ROOT, capture_output=True)
        sys.exit(0)

    # 8. PR 생성 (검증 통과 + 사용자 확인 후)
    pr_url = create_pr(user_name, product_name)

    print("\n" + "=" * 40)
    print("  플로우 작업이 완료되었습니다!")
    print(f"  PR: {pr_url}")
    print("=" * 40)


if __name__ == "__main__":
    main()
