[CmdletBinding()]
param(
    [Parameter(Mandatory = $false, Position = 0)]
    [string[]]$Skills,

    [Parameter(Mandatory = $false)]
    [switch]$All,

    [Parameter(Mandatory = $false)]
    [switch]$Prune
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
    Write-Host "  .\\sync_skills.ps1 -All -Prune" -ForegroundColor Yellow
    Write-Host "  .\\sync_skills.ps1 -Skills invest_analysis,analysis_code" -ForegroundColor Yellow
    Write-Host "  .\\sync_skills.ps1 -Skills invest_analysis,analysis_code -Prune" -ForegroundColor Yellow
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

    if ($Prune) {
        Write-Host "Pruning stale files: $skill" -ForegroundColor DarkCyan

        $srcFiles = Get-ChildItem -Path $src -Recurse -File |
            ForEach-Object { $_.FullName.Substring($src.Length + 1) }

        $dstFiles = Get-ChildItem -Path $dst -Recurse -File |
            ForEach-Object { $_.FullName.Substring($dst.Length + 1) }

        $staleFiles = $dstFiles | Where-Object { $_ -notin $srcFiles }

        foreach ($relPath in $staleFiles) {
            $stalePath = Join-Path $dst $relPath
            if (Test-Path $stalePath) {
                Remove-Item -Path $stalePath -Force
                Write-Host "  Removed stale file: $relPath" -ForegroundColor DarkGray
            }
        }

        Get-ChildItem -Path $dst -Recurse -Directory |
            Sort-Object FullName -Descending |
            ForEach-Object {
                if (-not (Get-ChildItem -Path $_.FullName -Force)) {
                    Remove-Item -Path $_.FullName -Force
                }
            }
    }
}

Write-Host "Sync completed" -ForegroundColor Green
