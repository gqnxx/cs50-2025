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

function Test-BranchExists($branch) {
  git show-ref --verify --quiet "refs/heads/$branch" | Out-Null
  return ($LASTEXITCODE -eq 0)
}

function Publish-FileToBranch($repoDir, $branch, $srcFile, $dstName) {
  Push-Location $repoDir
  try {
    if (Test-BranchExists $branch) {
      git switch $branch | Out-Null
    } else {
      git switch -c $branch | Out-Null
    }
    Copy-Item $srcFile (Join-Path $repoDir $dstName) -Force
    git add $dstName | Out-Null
    $changes = (git status --porcelain | Out-String).Trim()
    if ($changes) {
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
    if (Test-BranchExists 'main') {
      git switch main | Out-Null
    } else {
      git switch -c main | Out-Null
    }
    $dstPath = Join-Path $repoDir $dstRelPath
    $dstDir = Split-Path $dstPath -Parent
    if (-not (Test-Path $dstDir)) { New-Item -ItemType Directory -Force -Path $dstDir | Out-Null }
    Copy-Item $srcFile $dstPath -Force
    git add $dstRelPath | Out-Null
    $changes = (git status --porcelain | Out-String).Trim()
    if ($changes) {
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
  @{ branch = "cs50/problems/2024/x/hello";           src = (Join-Path $Pset1Path "hello\hello.c");       root = "hello.c";  main = "pset1/hello/hello.c" },
  @{ branch = "cs50/problems/$YearSlug/x/mario/less"; src = (Join-Path $Pset1Path "mario-less\mario.c");  root = "mario.c";  main = "pset1/mario-less/mario.c" },
  @{ branch = "cs50/problems/$YearSlug/x/mario/more"; src = (Join-Path $Pset1Path "mario-more\mario.c");  root = "mario.c";  main = "pset1/mario-more/mario.c" },
  @{ branch = "cs50/problems/$YearSlug/x/cash";       src = (Join-Path $Pset1Path "cash\cash.c");          root = "cash.c";   main = "pset1/cash/cash.c" },
  @{ branch = "cs50/problems/$YearSlug/x/credit";     src = (Join-Path $Pset1Path "credit\credit.c");      root = "credit.c"; main = "pset1/credit/credit.c" },
  # Mirror hello onto the scratch default branch for quick viewing
  @{ branch = "cs50/problems/$YearSlug/x/scratch";    src = (Join-Path $Pset1Path "hello\hello.c");       root = "hello.c" }
  
  # Week 2
  @{ branch = "cs50/problems/$YearSlug/x/scrabble";   src = (Join-Path $PSScriptRoot "..\pset2-c\scrabble\scrabble.c");       root = "scrabble.c";   main = "pset2/scrabble/scrabble.c" },
  @{ branch = "cs50/problems/$YearSlug/x/readability";src = (Join-Path $PSScriptRoot "..\pset2-c\readability\readability.c"); root = "readability.c"; main = "pset2/readability/readability.c" },
  @{ branch = "cs50/problems/$YearSlug/x/caesar";     src = (Join-Path $PSScriptRoot "..\pset2-c\caesar\caesar.c");         root = "caesar.c";     main = "pset2/caesar/caesar.c" },
  
  # Week 3
  @{ branch = "cs50/problems/$YearSlug/x/sort";       src = (Join-Path $PSScriptRoot "..\pset3-c\sort\sort.c");           root = "sort.c";       main = "pset3/sort/sort.c" },
  @{ branch = "cs50/problems/$YearSlug/x/plurality";  src = (Join-Path $PSScriptRoot "..\pset3-c\plurality\plurality.c"); root = "plurality.c";  main = "pset3/plurality/plurality.c" },
  @{ branch = "cs50/problems/$YearSlug/x/runoff";     src = (Join-Path $PSScriptRoot "..\pset3-c\runoff\runoff.c");       root = "runoff.c";     main = "pset3/runoff/runoff.c" },
  @{ branch = "cs50/problems/$YearSlug/x/tideman";    src = (Join-Path $PSScriptRoot "..\pset3-c\tideman\tideman.c");     root = "tideman.c";    main = "pset3/tideman/tideman.c" },
  
  # Week 4
  @{ branch = "cs50/problems/$YearSlug/x/volume";     src = (Join-Path $PSScriptRoot "..\pset4-c\volume\volume.c");       root = "volume.c";     main = "pset4/volume/volume.c" },
  @{ branch = "cs50/problems/$YearSlug/x/filter";     src = (Join-Path $PSScriptRoot "..\pset4-c\filter\filter.c");       root = "filter.c";     main = "pset4/filter/filter.c" },
  @{ branch = "cs50/problems/$YearSlug/x/recover";    src = (Join-Path $PSScriptRoot "..\pset4-c\recover\recover.c");     root = "recover.c";    main = "pset4/recover/recover.c" },
  
  # Week 5
  @{ branch = "cs50/problems/$YearSlug/x/inheritance"; src = (Join-Path $PSScriptRoot "..\pset5-c\inheritance\inheritance.c"); root = "inheritance.c"; main = "pset5/inheritance/inheritance.c" },
  @{ branch = "cs50/problems/$YearSlug/x/speller";     src = (Join-Path $PSScriptRoot "..\pset5-c\speller\dictionary.c");      root = "dictionary.c";  main = "pset5/speller/dictionary.c" },
  
  # Week 6 (Python)
  @{ branch = "cs50/problems/$YearSlug/x/sentimental-hello";      src = (Join-Path $PSScriptRoot "..\pset6-py\hello\hello.py");         root = "hello.py";         main = "pset6/hello/hello.py" },
  @{ branch = "cs50/problems/$YearSlug/x/sentimental-mario-less"; src = (Join-Path $PSScriptRoot "..\pset6-py\mario-less\mario.py");    root = "mario.py";         main = "pset6/mario-less/mario.py" },
  @{ branch = "cs50/problems/$YearSlug/x/sentimental-mario-more"; src = (Join-Path $PSScriptRoot "..\pset6-py\mario-more\mario.py");    root = "mario.py";         main = "pset6/mario-more/mario.py" },
  @{ branch = "cs50/problems/$YearSlug/x/sentimental-cash";       src = (Join-Path $PSScriptRoot "..\pset6-py\cash\cash.py");           root = "cash.py";          main = "pset6/cash/cash.py" },
  @{ branch = "cs50/problems/$YearSlug/x/sentimental-credit";     src = (Join-Path $PSScriptRoot "..\pset6-py\credit\credit.py");       root = "credit.py";        main = "pset6/credit/credit.py" },
  @{ branch = "cs50/problems/$YearSlug/x/sentimental-readability"; src = (Join-Path $PSScriptRoot "..\pset6-py\readability\readability.py"); root = "readability.py"; main = "pset6/readability/readability.py" },
  @{ branch = "cs50/problems/$YearSlug/x/dna";                    src = (Join-Path $PSScriptRoot "..\pset6-py\dna\dna.py");             root = "dna.py";           main = "pset6/dna/dna.py" }
)

foreach ($p in $problems) {
  if (-not (Test-Path $p.src)) { throw "Missing source file: $($p.src)" }
  Publish-FileToBranch -repoDir $Me50Dir -branch $p.branch -srcFile $p.src -dstName $p.root
  if ($p.ContainsKey('main') -and $p.main) {
    Publish-FileToMain -repoDir $Me50Dir -srcFile $p.src -dstRelPath $p.main
  }
}

Write-Host "Sync complete (branches + main)." -ForegroundColor Green
