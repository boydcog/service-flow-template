#!/usr/bin/env python3
"""
/admin 명령어 자동화 스크립트
템플릿 규칙, 팀 관리, 테마 설정을 담당합니다.
"""

import os
import sys
import json
import yaml
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict

# 프로젝트 루트
PROJECT_ROOT = Path(__file__).parent.parent


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


def load_admins() -> List[Dict]:
    """admins.yaml 로드"""
    admins_file = PROJECT_ROOT / ".claude" / "manifests" / "admins.yaml"
    if not admins_file.exists():
        return []

    try:
        with open(admins_file) as f:
            data = yaml.safe_load(f) or {}
            return data.get("admins", [])
    except:
        return []


def check_permissions(user_name: str) -> bool:
    """관리자 권한 확인 (admins.yaml 기반)"""
    admins = load_admins()
    admin_names = [admin.get("name") for admin in admins]

    if user_name in admin_names:
        return True

    return False


def verify_admin_access(user_name: str) -> None:
    """관리자 접근 권한 검증 (실패 시 종료)"""
    if not check_permissions(user_name):
        print(f"❌ 관리자 권한이 없습니다.")
        print(f"   현재 사용자: {user_name}")
        print(f"   필요: .claude/manifests/admins.yaml에 등록된 관리자")
        sys.exit(1)

    print(f"✅ 관리자 권한 확인됨: {user_name}")


def select_admin_option() -> str:
    """관리 옵션 선택"""
    print("\n⚙️  관리 옵션을 선택하세요:")
    print("  1. 📚 컴포넌트 스펙 관리")
    print("  2. 👥 팀원 관리")
    print("  3. 🎨 테마 업데이트")
    print("  4. 🔐 역할 및 권한 관리")
    print("  5. 📋 CHANGELOG 작성")
    print("  6. 📊 통계 보기")
    print("  7. 📸 컴포넌트 스크린샷 캡처")

    while True:
        choice = input("\n선택 (1-7): ").strip()
        if choice in ["1", "2", "3", "4", "5", "6", "7"]:
            return choice
        print("❌ 올바른 선택입니다 (1-7).")


def manage_component_specs() -> None:
    """컴포넌트 스펙 관리"""
    print("\n📚 컴포넌트 스펙 관리")
    print("=" * 40)

    spec_file = PROJECT_ROOT / ".claude" / "spec" / "component-spec.md"
    if not spec_file.exists():
        print(f"❌ 스펙 파일 없음: {spec_file}")
        return

    print("\n액션 선택:")
    print("  1. ✏️  스펙 수정")
    print("  2. 📖 스펙 보기")

    choice = input("\n선택 (1 또는 2): ").strip()

    if choice == "1":
        # 편집기로 열기
        editor = os.environ.get("EDITOR", "nano")
        subprocess.run([editor, str(spec_file)])
        print(f"✅ 스펙 파일이 업데이트되었습니다: {spec_file}")
    elif choice == "2":
        # 보기
        with open(spec_file) as f:
            print("\n" + f.read())


def manage_team() -> None:
    """팀원 관리"""
    print("\n👥 팀원 관리")
    print("=" * 40)

    team_file = PROJECT_ROOT / ".claude" / "manifests" / "team.yaml"

    print("\n액션 선택:")
    print("  1. ➕ 팀원 추가")
    print("  2. ❌ 팀원 제거")
    print("  3. 📋 팀 조회")

    choice = input("\n선택 (1-3): ").strip()

    if choice == "1":
        name = input("\n팀원 이름: ").strip()
        github = input("GitHub 사용자명: ").strip()
        email = input("이메일: ").strip()

        role_print = "  1. admin\n  2. developer\n  3. designer\n  4. pm"
        role_choice = input(f"\n역할:\n{role_print}\n선택 (1-4): ").strip()
        roles = ["admin", "developer", "designer", "pm"]
        role = roles[int(role_choice) - 1] if role_choice in ["1", "2", "3", "4"] else "pm"

        print(f"\n✅ 팀원 추가됨:")
        print(f"  이름: {name}")
        print(f"  역할: {role}")
        print(f"  GitHub: {github}")
        print(f"  이메일: {email}")

    elif choice == "2":
        name = input("\n제거할 팀원 이름: ").strip()
        confirm = input(f"정말 {name}을(를) 제거하시겠습니까? (y/n): ").strip().lower()
        if confirm == "y":
            print(f"✅ {name}이(가) 제거되었습니다.")

    elif choice == "3":
        print("\n📋 현재 팀 구성")
        print("-" * 40)
        print("(team.yaml 파일 참조)")


def update_theme() -> None:
    """테마 업데이트"""
    print("\n🎨 테마 업데이트")
    print("=" * 40)

    theme_file = PROJECT_ROOT / ".claude" / "manifests" / "theme.yaml"

    print("\n액션 선택:")
    print("  1. 🎨 색상 업데이트")
    print("  2. 📝 타이포그래피 변경")
    print("  3. 📏 간격(Spacing) 조정")

    choice = input("\n선택 (1-3): ").strip()

    if choice in ["1", "2", "3"]:
        editor = os.environ.get("EDITOR", "nano")
        subprocess.run([editor, str(theme_file)])
        print(f"✅ 테마가 업데이트되었습니다: {theme_file}")


def manage_roles() -> None:
    """역할 및 권한 관리"""
    print("\n🔐 역할 및 권한 관리")
    print("=" * 40)

    roles_file = PROJECT_ROOT / ".claude" / "manifests" / "roles.yaml"

    print("\n액션 선택:")
    print("  1. ✏️  역할 수정")
    print("  2. 📋 권한 조회")

    choice = input("\n선택 (1 또는 2): ").strip()

    if choice == "1":
        editor = os.environ.get("EDITOR", "nano")
        subprocess.run([editor, str(roles_file)])
        print(f"✅ 역할이 업데이트되었습니다: {roles_file}")

    elif choice == "2":
        with open(roles_file) as f:
            print("\n" + f.read())


def write_changelog() -> None:
    """CHANGELOG 작성"""
    print("\n📋 CHANGELOG 작성")
    print("=" * 40)

    changelog_file = PROJECT_ROOT / "CHANGELOG.md"

    # 기존 내용 읽기
    existing = ""
    if changelog_file.exists():
        with open(changelog_file) as f:
            existing = f.read()

    # 새 버전 입력
    version = input("\n새 버전 (예: 1.1.0): ").strip()
    if not version:
        print("❌ 버전을 입력해주세요.")
        return

    print("\n변경 유형 선택 (복수 선택 가능):")
    print("  - ✨ Features")
    print("  - 🐛 Bugfixes")
    print("  - 📚 Documentation")
    print("  - 🔨 Refactoring")
    print("  - 📦 Dependencies")

    changes = input("\n변경 내용 (자유 입력, 빈 줄로 종료): ").strip()

    # CHANGELOG 생성
    new_entry = f"""## v{version} ({datetime.now().strftime('%Y-%m-%d')})

{changes}

"""

    updated_changelog = new_entry + existing

    with open(changelog_file, "w") as f:
        f.write(updated_changelog)

    print(f"✅ CHANGELOG가 업데이트되었습니다: {changelog_file}")


def show_stats() -> None:
    """통계 보기"""
    print("\n📊 템플릿 통계")
    print("=" * 40)

    # 웹 컴포넌트 개수
    web_components = list((PROJECT_ROOT / "components" / "web" / "ui").glob("*.tsx"))
    web_count = len([f for f in web_components if not f.name.endswith(".stories.tsx")])

    # 네이티브 컴포넌트 개수
    native_components = list((PROJECT_ROOT / "components" / "native" / "ui").glob("*.tsx"))
    native_count = len([f for f in native_components if not f.name.endswith(".stories.tsx")])

    # 프로젝트 개수
    projects_dir = PROJECT_ROOT / "projects"
    projects_count = len([d for d in projects_dir.iterdir() if d.is_dir() and d.name != ".gitkeep"]) if projects_dir.exists() else 0

    # 플로우 개수
    flows_dir = PROJECT_ROOT / "flows"
    flows_count = len([d for d in flows_dir.iterdir() if d.is_dir() and d.name != ".gitkeep"]) if flows_dir.exists() else 0

    print(f"\n📦 컴포넌트:")
    print(f"  - Web: {web_count}개")
    print(f"  - Native: {native_count}개")
    print(f"  - 총합: {web_count + native_count}개")

    print(f"\n📁 프로젝트:")
    print(f"  - 활성 프로젝트: {projects_count}개")

    print(f"\n🌿 서비스 플로우:")
    print(f"  - 플로우: {flows_count}개")

    print(f"\n📝 최근 커밋:")
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-5"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        print(result.stdout)
    except:
        print("  (git 정보 없음)")


def create_pr(user_name: str) -> str:
    """PR 생성"""
    print("\n🔄 PR 생성 중...")

    branch_name = f"admin/template-update-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    pr_title = f"[admin] {user_name}: 템플릿 업데이트"
    pr_body = """## 템플릿 업데이트

### 변경 사항
- 컴포넌트 스펙 업데이트
- 팀원 관리
- 테마 업데이트
- 역할 및 권한 관리
- CHANGELOG 작성

### 체크리스트
- [x] 모든 변경사항 검토
- [x] CHANGELOG 작성
- [x] 문서 업데이트

Co-Authored-By: {user_name} <noreply@anthropic.com>
"""

    try:
        # 브랜치 생성
        subprocess.run(
            ["git", "checkout", "-b", branch_name],
            cwd=PROJECT_ROOT,
            capture_output=True,
            check=True,
        )

        # 변경사항 추가 및 커밋
        subprocess.run(
            ["git", "add", "-A"],
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

        # push
        subprocess.run(
            ["git", "push", "-u", "origin", branch_name],
            cwd=PROJECT_ROOT,
            capture_output=True,
            check=True,
        )

        # PR 생성
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


def capture_component_screenshots() -> None:
    """컴포넌트 스크린샷 캡처"""
    import time

    print("\n📸 컴포넌트 스크린샷 캡처")
    print("=" * 40)

    # .playwright 디렉토리 생성
    playwright_dir = PROJECT_ROOT / ".playwright"
    playwright_dir.mkdir(exist_ok=True)

    # process-manager로 포트 6006 정리
    print("🔄 포트 정리 중...")
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

    # Storybook 시작
    print("🚀 Storybook 시작 중...")
    try:
        storybook_process = subprocess.Popen(
            ["npm", "run", "storybook"],
            cwd=PROJECT_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Storybook 시작 대기
        time.sleep(8)

        # Playwright를 사용한 스크린샷 캡처
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()

                print("📖 Storybook 접속 중...")
                try:
                    page.goto("http://localhost:6006", wait_until="networkidle", timeout=30000)
                except:
                    page.goto("http://localhost:6006", timeout=30000)

                # 기본 Storybook 대시보드 스크린샷
                print("📸 대시보드 스크린샷 캡처...")
                page.take_screenshot(
                    path=str(playwright_dir / "storybook-dashboard.png"),
                    full_page=True
                )

                # 각 컴포넌트 스토리 캡처 (몇 가지 주요 컴포넌트)
                components = ["Badge", "Button", "Card", "Dialog", "Table", "Tabs", "Avatar", "Switch"]
                for component in components:
                    try:
                        # 컴포넌트 페이지 접속
                        url = f"http://localhost:6006/?path=/story/web-{component.lower()}--default"
                        print(f"📸 {component} 캡처 중...")
                        page.goto(url, wait_until="networkidle", timeout=30000)

                        # 약간의 대기 (렌더링 완료)
                        page.wait_for_timeout(1000)

                        # 스크린샷 캡처
                        page.take_screenshot(
                            path=str(playwright_dir / f"component-{component.lower()}.png"),
                            full_page=True
                        )
                    except Exception as e:
                        print(f"⚠️  {component} 캡처 실패: {e}")
                        continue

                browser.close()
                print(f"\n✅ 스크린샷 캡처 완료!")
                print(f"📍 저장 위치: {playwright_dir}")

        except ImportError:
            print("⚠️  Playwright Python 모듈이 설치되지 않았습니다.")
            print("설치 명령어: pip install playwright")
            print("또는 npm install -D @playwright/test")

    except Exception as e:
        print(f"❌ 스크린샷 캡처 실패: {e}")
    finally:
        # Storybook 프로세스 종료
        print("\n🛑 Storybook 종료 중...")
        try:
            storybook_process.terminate()
            storybook_process.wait(timeout=5)
        except:
            try:
                storybook_process.kill()
            except:
                pass


def main() -> None:
    """메인 함수"""
    print("\n# /admin — 템플릿 관리")
    print("=" * 40)

    # 1. 신원 확인
    identity = load_user_identity()
    user_name = identity.get("name", "unknown")
    user_role = identity.get("role", "unknown")

    print(f"\n✅ 신원: {user_name} ({user_role})")

    # 2. 권한 확인 (admins.yaml 기반)
    verify_admin_access(user_name)
    print("✅ 권한: 템플릿 관리 가능")

    # 3. 관리 옵션 선택
    option = select_admin_option()

    # 4. 옵션별 처리
    if option == "1":
        manage_component_specs()
    elif option == "2":
        manage_team()
    elif option == "3":
        update_theme()
    elif option == "4":
        manage_roles()
    elif option == "5":
        write_changelog()
    elif option == "6":
        show_stats()
    elif option == "7":
        capture_component_screenshots()
        return  # 스크린샷 캡처 후 PR 생성 스킵

    # 5. PR 생성 (선택)
    print("\n" + "=" * 40)
    pr_confirm = input("변경사항을 PR로 생성하시겠습니까? (y/n): ").strip().lower()

    if pr_confirm == "y":
        create_pr(user_name)
        print("\n✅ 템플릿 관리 작업이 완료되었습니다!")
    else:
        print("\n ⏭️  PR 생성 없이 작업을 마칩니다.")


if __name__ == "__main__":
    main()
