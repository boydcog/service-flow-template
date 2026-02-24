#!/usr/bin/env python3
"""
포트/프로세스 관리 유틸리티
포트 감지, 종료, 재시작 기능 제공
"""

import os
import sys
import subprocess
import time
import signal
import json
from pathlib import Path
from typing import Optional, List


def kill_port(port: int) -> bool:
    """특정 포트의 프로세스 종료"""
    try:
        # macOS/Linux: lsof 사용
        result = subprocess.run(
            f"lsof -ti :{port} | xargs kill -9",
            shell=True,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"[OK] 포트 {port} 프로세스 종료 완료")
            time.sleep(1)  # 포트가 완전히 해제될 때까지 대기
            return True
        else:
            # 프로세스가 없을 수도 있음
            return True
    except Exception as e:
        print(f"[WARNING] 포트 {port} 종료 중 오류: {e}")
        return False


def is_port_in_use(port: int) -> bool:
    """포트 사용 중 여부 확인"""
    try:
        result = subprocess.run(
            f"lsof -ti :{port}",
            shell=True,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except:
        return False


def init_state_dirs() -> None:
    """상태 디렉토리 초기화 (로그, PID 저장소)"""
    Path(".claude/state/logs").mkdir(parents=True, exist_ok=True)
    Path(".claude/state/pids").mkdir(parents=True, exist_ok=True)


def kill_service(service_name: str) -> bool:
    """PID 파일 기반 서비스 종료 (데몬 모드 프로세스 그룹 포함)"""
    pid_file = Path(f".claude/state/pids/{service_name}.pid")

    if not pid_file.exists():
        print(f"[WARNING] {service_name} PID 파일 없음 (실행 중이 아님)")
        return True

    try:
        pid = int(pid_file.read_text().strip())
        print(f"[STOP] {service_name} (PID {pid}) 종료 중...")

        # start_new_session=True인 경우 프로세스 그룹으로 종료 (-pid)
        try:
            os.killpg(os.getpgid(pid), signal.SIGTERM)
        except ProcessLookupError:
            # 프로세스가 없으면 직접 종료 시도
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                print(f"[OK] {service_name} 이미 종료됨")
                pid_file.unlink()
                return True

        time.sleep(1)

        # SIGKILL로 강제 종료 (필요시)
        try:
            pgid = os.getpgid(pid)
            os.killpg(pgid, 0)  # 프로세스 그룹 확인
            os.killpg(pgid, signal.SIGKILL)
            print(f"[WARNING] {service_name} 강제 종료됨 (SIGKILL)")
        except (ProcessLookupError, PermissionError):
            # ProcessLookupError: 프로세스 없음
            # PermissionError: 프로세스 이미 종료됨 (접근 거부 = 존재하지 않음)
            print(f"[OK] {service_name} 정상 종료됨")

        pid_file.unlink()
        return True
    except Exception as e:
        print(f"[ERROR] {service_name} 종료 실패: {e}")
        try:
            pid_file.unlink()
        except:
            pass
        return False


def start_storybook(project_root: Path) -> bool:
    """Storybook 시작 (포트 6006, 데몬 모드)"""
    port = 6006
    service_name = "storybook"

    init_state_dirs()

    print(f"\n[SETUP] {service_name} 정리 중...")
    kill_service(service_name)
    kill_port(port)

    print(f"[START] {service_name} 시작 중 (포트 {port})...")
    try:
        log_file = Path(".claude/state/logs") / f"{service_name}.log"
        pid_file = Path(".claude/state/pids") / f"{service_name}.pid"

        with open(log_file, "a") as log:
            process = subprocess.Popen(
                ["npm", "run", "storybook"],
                cwd=project_root,
                stdout=log,
                stderr=log,
                stdin=subprocess.DEVNULL,
                start_new_session=True,  # 데몬화: Claude 세션 독립적으로 실행
            )

        # PID 저장
        pid_file.write_text(str(process.pid))
        print(f"   (PID: {process.pid}, 로그: {log_file})")

        time.sleep(3)  # Storybook 시작 대기

        if is_port_in_use(port):
            print(f"[OK] {service_name} 시작됨 → http://localhost:{port}")
            return True
        else:
            print(f"[WARNING] {service_name} 포트 {port}에서 실행 중이 아닙니다.")
            return False
    except Exception as e:
        print(f"[ERROR] {service_name} 시작 실패: {e}")
        return False


def start_dev_server(project_path: Path, port: int = 3000) -> bool:
    """개발 서버 시작 (기본 포트 3000, 데몬 모드)"""
    service_name = "devserver"

    init_state_dirs()

    print(f"\n[SETUP] {service_name} 정리 중...")
    kill_service(service_name)
    kill_port(port)

    print(f"[START] {service_name} 시작 중 (포트 {port})...")
    try:
        log_file = Path(".claude/state/logs") / f"{service_name}.log"
        pid_file = Path(".claude/state/pids") / f"{service_name}.pid"

        with open(log_file, "a") as log:
            process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=project_path,
                stdout=log,
                stderr=log,
                stdin=subprocess.DEVNULL,
                start_new_session=True,  # 데몬화: Claude 세션 독립적으로 실행
            )

        # PID 저장
        pid_file.write_text(str(process.pid))
        print(f"   (PID: {process.pid}, 로그: {log_file})")

        time.sleep(3)  # 서버 시작 대기

        if is_port_in_use(port):
            print(f"[OK] {service_name} 시작됨 → http://localhost:{port}")
            return True
        else:
            print(f"[WARNING] {service_name} 포트 {port}에서 실행 중이 아닙니다.")
            return False
    except Exception as e:
        print(f"[ERROR] {service_name} 시작 실패: {e}")
        return False


def start_react_native(project_path: Path, port: int = 8081) -> bool:
    """React Native 개발 서버 시작 (기본 포트 8081, 데몬 모드)"""
    service_name = "metro"

    init_state_dirs()

    print(f"\n[SETUP] {service_name} 정리 중...")
    kill_service(service_name)
    kill_port(port)

    print(f"[START] {service_name} 시작 중 (포트 {port})...")
    try:
        log_file = Path(".claude/state/logs") / f"{service_name}.log"
        pid_file = Path(".claude/state/pids") / f"{service_name}.pid"

        with open(log_file, "a") as log:
            process = subprocess.Popen(
                ["npm", "start"],
                cwd=project_path,
                stdout=log,
                stderr=log,
                stdin=subprocess.DEVNULL,
                start_new_session=True,  # 데몬화: Claude 세션 독립적으로 실행
            )

        # PID 저장
        pid_file.write_text(str(process.pid))
        print(f"   (PID: {process.pid}, 로그: {log_file})")

        time.sleep(3)  # 서버 시작 대기

        if is_port_in_use(port):
            print(f"[OK] {service_name} 시작됨 → http://localhost:{port}")
            return True
        else:
            print(f"[WARNING] {service_name} 포트 {port}에서 실행 중이 아닙니다.")
            return False
    except Exception as e:
        print(f"[ERROR] {service_name} 시작 실패: {e}")
        return False


def get_ports_for_project(project_path: Path) -> dict:
    """프로젝트의 포트 설정 조회"""
    config_file = project_path / "config.json"

    if config_file.exists():
        import json
        try:
            with open(config_file) as f:
                config = json.load(f)
                return {
                    "type": config.get("type", "web"),
                    "devPort": config.get("devPort", 3000),
                    "nativePort": config.get("nativePort", 8081),
                }
        except:
            pass

    # 기본값
    return {
        "type": "web",
        "devPort": 3000,
        "nativePort": 8081,
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        action = sys.argv[1]

        if action == "kill-port" and len(sys.argv) > 2:
            port = int(sys.argv[2])
            kill_port(port)
        elif action == "kill-service" and len(sys.argv) > 2:
            service = sys.argv[2]
            kill_service(service)
        elif action == "is-in-use" and len(sys.argv) > 2:
            port = int(sys.argv[2])
            print(is_port_in_use(port))
        else:
            print("Usage: process-manager.py [kill-port <port> | kill-service <name> | is-in-use <port>]")
