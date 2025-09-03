param(
  [string]$Me50Url = "https://github.com/me50/gqnxx.git",
  [string]$Me50Dir = "$PSScriptRoot\..\..\me50-gqnxx",
  [string]$YearSlug = "2025",
  [string]$Pset1Path = "$PSScriptRoot\..\pset1-c"
)

$ErrorActionPreference = 'Stop'

function Ensure-Repo($url, $dir) {
  if (-not (Test-Path $dir)) {
    git clone $url $dir | Out-Null
  }
}

function Publish-FileToBranch($repoDir, $branch, $srcFile, $dstName) {
  Push-Location $repoDir
  try {
    if (git show-ref --verify --quiet "refs/heads/$branch") {
      git switch $branch | Out-Null
    } else {
      git switch -c $branch | Out-Null
    }
    Copy-Item $srcFile (Join-Path $repoDir $dstName) -Force
    git add $dstName | Out-Null
    if ((git status --porcelain).Trim()) {
      git commit -m "submit: $dstName" | Out-Null
      git push -u origin $branch | Out-Null
      Write-Host "Pushed $branch" -ForegroundColor Green
    } else {
      Write-Host "No changes for $branch" -ForegroundColor Yellow
    }
  } finally {
    Pop-Location
  }
}

function Publish-FileToMain($repoDir, $srcFile, $dstRelPath) {
  Push-Location $repoDir
  try {
    if (git show-ref --verify --quiet "refs/heads/main") {
      git switch main | Out-Null
    } else {
      git switch -c main | Out-Null
    }
    $dstPath = Join-Path $repoDir $dstRelPath
    $dstDir = Split-Path $dstPath -Parent
    if (-not (Test-Path $dstDir)) { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
    Copy-Item $srcFile $dstPath -Force
    git add $dstRelPath | Out-Null
    if ((git status --porcelain).Trim()) {
      git commit -m "pset sync: update $dstRelPath" | Out-Null
      git push | Out-Null
      Write-Host "Updated main:$dstRelPath" -ForegroundColor Cyan
    } else {
      Write-Host "No changes for main:$dstRelPath" -ForegroundColor Yellow
    }
  } finally {
    Pop-Location
  }
}

# Ensure me50 repo exists
Ensure-Repo -url $Me50Url -dir $Me50Dir

# Map pset1 problems (dev sources in cs50-2025)
$problems = @(
  @{ branch = "cs50/problems/$YearSlug/x/hello";      src = (Join-Path $Pset1Path "hello\hello.c");       root = "hello.c";  main = "pset1/hello/hello.c" },
  @{ branch = "cs50/problems/$YearSlug/x/mario/less"; src = (Join-Path $Pset1Path "mario-less\mario.c");  root = "mario.c";  main = "pset1/mario-less/mario.c" },
  @{ branch = "cs50/problems/$YearSlug/x/mario/more"; src = (Join-Path $Pset1Path "mario-more\mario.c");  root = "mario.c";  main = "pset1/mario-more/mario.c" },
  @{ branch = "cs50/problems/$YearSlug/x/cash";       src = (Join-Path $Pset1Path "cash\cash.c");          root = "cash.c";   main = "pset1/cash/cash.c" },
  @{ branch = "cs50/problems/$YearSlug/x/credit";     src = (Join-Path $Pset1Path "credit\credit.c");      root = "credit.c"; main = "pset1/credit/credit.c" }
)

foreach ($p in $problems) {
  if (-not (Test-Path $p.src)) { throw "Missing source file: $($p.src)" }
  Publish-FileToBranch -repoDir $Me50Dir -branch $p.branch -srcFile $p.src -dstName $p.root
  Publish-FileToMain   -repoDir $Me50Dir -srcFile $p.src -dstRelPath $p.main
}

Write-Host "Sync complete (branches + main)." -ForegroundColor Green
