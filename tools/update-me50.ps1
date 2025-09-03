$ErrorActionPreference = 'Stop'

# 1) Sync me50 submit branches and main from cs50-2025 source of truth
& "$PSScriptRoot\sync-me50.ps1"

# 2) Backup local me50 working tree if there are local changes
$me50Dir = "$PSScriptRoot\..\..\me50-gqnxx"
if (-not (Test-Path $me50Dir)) { throw "me50 repo not found at: $me50Dir" }

Push-Location $me50Dir
try {
  $status = (git status --porcelain | Out-String).Trim()
  if ($status) {
    $ts = Get-Date -Format 'yyyyMMdd-HHmmss'
    $backupDir = Join-Path $me50Dir ".backups\$ts"
    New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
    # Use robocopy to mirror working tree excluding .git
    robocopy . $backupDir /MIR /XD .git | Out-Null
    Write-Host "Local edits detected and backed up to: $backupDir" -ForegroundColor Yellow
  }
}
finally {
  Pop-Location
}

# 3) Hard reset local main to origin/main and show current files
& "$PSScriptRoot\pull-me50.ps1"

Write-Host "Update complete." -ForegroundColor Green
