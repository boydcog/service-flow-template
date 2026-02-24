# Service Flow Template — Session Start (Windows)
Write-Host "=== Service Flow Template — Session Start ===" -ForegroundColor Green
Write-Host ""

# 1. 사용자 신원 로드
if (!(Test-Path .user-identity)) {
  Write-Host "⚠️  신원 파일 없음. /setup을 먼저 실행하세요." -ForegroundColor Yellow
  Write-Host ""
} else {
  $identityContent = Get-Content .user-identity
  $userName = ($identityContent | Select-String "^name:" | ForEach-Object { $_.ToString().Replace("name: ", "") }) -join ""
  $userRole = ($identityContent | Select-String "^role:" | ForEach-Object { $_.ToString().Replace("role: ", "") }) -join ""
  Write-Host "✅ 안녕하세요, $userName ($userRole)!" -ForegroundColor Green
}

# 2. GH 토큰 로드
if (Test-Path .gh-token) {
  $env:GH_TOKEN = Get-Content .gh-token -Raw | ForEach-Object { $_.Trim() }
  Write-Host "✅ GitHub 토큰 로드됨" -ForegroundColor Green
}

# 3. 로컬 파일 보호 (git pull에서 덮어쓰기 방지)
if (Test-Path .user-identity) {
  git update-index --skip-worktree .user-identity 2>$null | Out-Null
}
if (Test-Path .gh-token) {
  git update-index --skip-worktree .gh-token 2>$null | Out-Null
}

# 4. Git 동기화
$currentBranch = git branch --show-current 2>$null
if ($null -eq $currentBranch) {
  $currentBranch = "main"
}

git stash 2>$null | Out-Null
if (git pull --rebase origin $currentBranch 2>$null) {
  Write-Host "✅ Git 동기화 완료" -ForegroundColor Green
} else {
  Write-Host "⚠️  Git pull 실패 (오프라인 또는 네트워크 오류)" -ForegroundColor Yellow
}
git stash pop 2>$null | Out-Null

# 5. 상태 리포트
Write-Host ""
$webComponents = @(Get-ChildItem -Path "components/web" -Name "*.tsx" -ErrorAction SilentlyContinue).Count
$nativeComponents = @(Get-ChildItem -Path "components/native" -Name "*.tsx" -ErrorAction SilentlyContinue).Count
Write-Host "📦 웹 컴포넌트: $webComponents개"
Write-Host "📱 네이티브 컴포넌트: $nativeComponents개"
Write-Host "🌿 브랜치: $currentBranch"
Write-Host ""
Write-Host "명령어: /setup  /admin  /designer  /flow  /create-issue"
Write-Host ""
