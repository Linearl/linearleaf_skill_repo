[CmdletBinding()]
param(
    [Parameter(Mandatory = $false, Position = 0)]
    [string[]]$Skills,

    [Parameter(Mandatory = $false)]
    [switch]$All
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillsRoot = Join-Path $root ".github\skills"

function Test-IsSkillDir {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    $skillFile = Join-Path $Path "SKILL.md"
    return (Test-Path $skillFile)
}

if (-not (Test-Path $skillsRoot)) {
    Write-Error "Missing .github\\skills directory: $skillsRoot"
    exit 1
}

if ($All) {
    $Skills = Get-ChildItem -Path $root -Directory |
        Where-Object { Test-IsSkillDir $_.FullName } |
        Select-Object -ExpandProperty Name
}

if (-not $Skills -or $Skills.Count -eq 0) {
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\\sync_skills.ps1 -All" -ForegroundColor Yellow
    Write-Host "  .\\sync_skills.ps1 -Skills invest_analysis,analysis_code" -ForegroundColor Yellow
    exit 1
}

foreach ($skill in $Skills) {
    $src = Join-Path $root $skill
    $dst = Join-Path $skillsRoot $skill

    if (-not (Test-Path $src)) {
        Write-Warning "Skip: source directory not found $src"
        continue
    }

    if (-not (Test-IsSkillDir $src)) {
        Write-Warning "Skip: $src is not a skill directory (missing SKILL.md)"
        continue
    }

    if (-not (Test-Path $dst)) {
        New-Item -ItemType Directory -Path $dst -Force | Out-Null
    }

    Write-Host "Syncing: $skill" -ForegroundColor Cyan
    Copy-Item -Path (Join-Path $src "*") -Destination $dst -Recurse -Force
}

Write-Host "Sync completed" -ForegroundColor Green
