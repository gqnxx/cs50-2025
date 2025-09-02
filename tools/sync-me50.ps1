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

function Publish-File($repoDir, $branch, $srcFile, $dstName) {
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

# Ensure me50 repo exists
Ensure-Repo -url $Me50Url -dir $Me50Dir

# Map pset1 problems
$problems = @(
  @{ branch = "cs50/problems/$YearSlug/x/mario/less"; src = Join-Path $Pset1Path "mario-less\mario.c"; dst = "mario.c" },
  @{ branch = "cs50/problems/$YearSlug/x/mario/more"; src = Join-Path $Pset1Path "mario-more\mario.c"; dst = "mario.c" },
  @{ branch = "cs50/problems/$YearSlug/x/cash";       src = Join-Path $Pset1Path "cash\cash.c";         dst = "cash.c" },
  @{ branch = "cs50/problems/$YearSlug/x/credit";     src = Join-Path $Pset1Path "credit\credit.c";     dst = "credit.c" }
)

foreach ($p in $problems) {
  if (-not (Test-Path $p.src)) { throw "Missing source file: $($p.src)" }
  Publish-File -repoDir $Me50Dir -branch $p.branch -srcFile $p.src -dstName $p.dst
}

Write-Host "Sync complete." -ForegroundColor Cyan
