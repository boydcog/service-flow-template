# Service Flow Template — Session Start (Windows)
Set-StrictMode -Version 2
$ErrorActionPreference = "SilentlyContinue"

$PROJECT_DIR = Get-Location
$STATUS = @()

Write-Host "=== Service Flow Template — Session Start ===" -ForegroundColor Green
Write-Host ""

# ──────────────────────────────────────
# 1. 의존성 감지 및 자동 설치
# ──────────────────────────────────────
$HAS_GIT = $false
$HAS_GH = $false
$HAS_NODE = $false
$HAS_PNPM = $false

if (Get-Command git -ErrorAction SilentlyContinue) { $HAS_GIT = $true }
if (Get-Command gh -ErrorAction SilentlyContinue) { $HAS_GH = $true }
if (Get-Command node -ErrorAction SilentlyContinue) { $HAS_NODE = $true }
if (Get-Command pnpm -ErrorAction SilentlyContinue) { $HAS_PNPM = $true }

# Git 설치 확인 (Windows에서는 Git Bash 필요)
if (-not $HAS_GIT) {
  Write-Host "Git을 설치하세요: https://git-scm.com/download/win" -ForegroundColor Yellow
  $STATUS += "FAIL git 미설치"
} else {
  $STATUS += "OK git 설치됨"
}

# GitHub CLI 설치 확인
if (-not $HAS_GH) {
  $STATUS += "WARN gh CLI 미설치"
} else {
  $STATUS += "OK gh CLI 설치됨"
}

# Node.js 및 pnpm 확인
if (Test-Path "package.json") {
  if (-not $HAS_NODE) {
    Write-Host "Node.js를 설치하세요: https://nodejs.org/" -ForegroundColor Yellow
    $STATUS += "WARN Node.js 미설치"
  } else {
    $STATUS += "OK Node.js 설치됨"
  }

  if (-not $HAS_PNPM) {
    Write-Host "pnpm을 설치하세요: npm install -g pnpm" -ForegroundColor Yellow
    $STATUS += "WARN pnpm 미설치"
  } else {
    $STATUS += "OK pnpm 설치됨"
  }
}

# ──────────────────────────────────────
# 2. 사용자 신원 & Git Remote 로드
# ──────────────────────────────────────
$USER_NAME = ""
$USER_ROLE = "unknown"
$USER_GITHUB = ""
$GIT_REMOTE_URL = ""

if (Test-Path .user-identity) {
  $identityContent = Get-Content .user-identity -Raw
  $USER_NAME = ($identityContent | Select-String "^name:" | ForEach-Object { $_.ToString() -replace "name: ", "" }).Trim()
  $USER_ROLE = ($identityContent | Select-String "^role:" | ForEach-Object { $_.ToString() -replace "role: ", "" }).Trim()
  $USER_GITHUB = ($identityContent | Select-String "^github:" | ForEach-Object { $_.ToString() -replace "github: ", "" }).Trim()

  Write-Host "✅ 안녕하세요, $USER_NAME ($USER_ROLE)!" -ForegroundColor Green
  $STATUS += "OK 사용자: $USER_NAME ($USER_ROLE)"

  # GitHub 사용자명으로 repository URL 구성
  if ($USER_GITHUB) {
    $GIT_REMOTE_URL = "git@github.com:${USER_GITHUB}/service-flow-template.git"
  }
} else {
  $STATUS += "WARN 사용자 미설정"
}

# ──────────────────────────────────────
# 3. GH 토큰 로드 및 Git 인증 설정
# ──────────────────────────────────────
$GH_TOKEN_LOADED = $false
if (Test-Path .gh-token) {
  $tokenContent = (Get-Content .gh-token -Raw).Trim()
  if ($tokenContent) {
    $env:GH_TOKEN = $tokenContent
    $GH_TOKEN_LOADED = $true

    # Git 인증 설정
    git config --local user.name "Claude Code Bot"
    git config --local user.email "bot@claudecode.local"
    git config --local credential.helper wincred

    Write-Host "✅ GitHub 토큰 로드됨" -ForegroundColor Green
    Write-Host "✅ Git 인증 설정 완료" -ForegroundColor Green
    $STATUS += "OK GitHub 토큰 로드"
  }
}

# ──────────────────────────────────────
# 4. 로컬 파일 보호 (git pull에서 덮어쓰기 방지)
# ──────────────────────────────────────
if (Test-Path .user-identity) {
  git update-index --skip-worktree .user-identity 2>$null | Out-Null
}
if (Test-Path .gh-token) {
  git update-index --skip-worktree .gh-token 2>$null | Out-Null
}

# ──────────────────────────────────────
# 5. Git 저장소 초기화 및 Remote 설정
# ──────────────────────────────────────
$GIT_READY = $false
$CURRENT_BRANCH = "main"

if ($HAS_GIT) {
  # 5.1. Git 저장소 확인
  if (-not (Test-Path .git)) {
    Write-Host "Git 저장소를 초기화 중입니다..." -ForegroundColor Cyan
    git init 2>$null | Out-Null
    $GIT_READY = $true
    $CURRENT_BRANCH = "main"
  } else {
    $GIT_READY = $true
    $CURRENT_BRANCH = git branch --show-current 2>$null
    if (-not $CURRENT_BRANCH) { $CURRENT_BRANCH = "main" }
  }

  # 5.2. Git Remote 설정
  $CURRENT_REMOTE = git config --get remote.origin.url 2>$null

  if (-not $CURRENT_REMOTE) {
    # Remote가 없으면 설정
    $REMOTE_URL = ""

    # 우선순위 1: .user-identity에서 GitHub 사용자명
    if ($GIT_REMOTE_URL) {
      $REMOTE_URL = $GIT_REMOTE_URL
    } elseif (Test-Path .git-remote-url) {
      # 우선순위 2: .git-remote-url 파일
      $REMOTE_URL = (Get-Content .git-remote-url -Raw).Trim()
    } elseif ($GH_TOKEN_LOADED -and $HAS_GH) {
      # 우선순위 3: GitHub API
      try {
        $response = curl.exe -s -H "Authorization: token $env:GH_TOKEN" https://api.github.com/user/repos | ConvertFrom-Json
        $REMOTE_URL = $response[0].clone_url
      } catch {}
    }

    # 기본값 (boydcog의 service-flow-template)
    if (-not $REMOTE_URL) {
      $REMOTE_URL = "git@github.com:boydcog/service-flow-template.git"
    }

    git remote add origin $REMOTE_URL 2>$null | Out-Null
    $STATUS += "OK Git Remote 설정: $REMOTE_URL"
  } else {
    $STATUS += "OK Git Remote 확인됨: $CURRENT_REMOTE"
  }

  # 5.3. Git Pull
  if ($GIT_READY) {
    $pullResult = git pull --rebase origin $CURRENT_BRANCH 2>&1
    if ($?) {
      Write-Host "✅ git pull 완료" -ForegroundColor Green
      $STATUS += "OK git pull 완료"
    } else {
      Write-Host "⚠️  git pull 실패 (오프라인 또는 네트워크 오류)" -ForegroundColor Yellow
      $STATUS += "WARN git pull 실패"
    }
  }
}

# ──────────────────────────────────────
# 6. 최종 상태 리포트
# ──────────────────────────────────────
Write-Host ""
Write-Host "의존성:" -ForegroundColor Cyan
Write-Host "  git: $HAS_GIT"
Write-Host "  gh: $HAS_GH"
Write-Host "  Node.js: $HAS_NODE"
Write-Host "  pnpm: $HAS_PNPM"
Write-Host ""

# 컴포넌트 개수 계산
$WEB_COUNT = 0
$NATIVE_COUNT = 0
if (Test-Path "components/web/ui") {
  $WEB_COUNT = @(Get-ChildItem -Path "components/web/ui" -Name "*.tsx" -ErrorAction SilentlyContinue).Count
}
if (Test-Path "components/native/ui") {
  $NATIVE_COUNT = @(Get-ChildItem -Path "components/native/ui" -Name "*.tsx" -ErrorAction SilentlyContinue).Count
}

Write-Host "프로젝트 상태:" -ForegroundColor Cyan
Write-Host "  웹 컴포넌트: $WEB_COUNT개"
Write-Host "  네이티브 컴포넌트: $NATIVE_COUNT개"
Write-Host "  현재 브랜치: $CURRENT_BRANCH"
Write-Host "  GH 토큰: $GH_TOKEN_LOADED"
Write-Host "  git 연결: $GIT_READY"
Write-Host ""

Write-Host "명령어: /setup  /admin  /designer  /flow  /create-issue" -ForegroundColor Green
Write-Host ""

# 상태 요약
if ($STATUS.Count -gt 0) {
  Write-Host "상태:" -ForegroundColor Cyan
  foreach ($msg in $STATUS) {
    Write-Host "  $msg"
  }
  Write-Host ""
}
