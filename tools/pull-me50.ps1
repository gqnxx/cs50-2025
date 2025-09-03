param(
  [string]$RepoDir = "$PSScriptRoot\..\..\me50-gqnxx"
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path $RepoDir)) {
  throw "me50 repo not found at: $RepoDir"
}

Push-Location $RepoDir
try {
  git remote -v | Out-Host
  git fetch --all --prune | Out-Host
  git switch main | Out-Host
  # Force local main to exactly match origin/main (discard local changes)
  git reset --hard origin/main | Out-Host
  Write-Host "--- latest commit on main ---" -ForegroundColor Cyan
  git log -1 --oneline | Out-Host
  Write-Host "--- pset1 files ---" -ForegroundColor Cyan
  Get-ChildItem -Recurse -File 'pset1' | Select-Object -ExpandProperty FullName | Out-Host
  Write-Host "Pull complete." -ForegroundColor Green
}
finally {
  Pop-Location
}
