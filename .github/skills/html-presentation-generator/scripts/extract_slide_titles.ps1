param(
    [Parameter(Mandatory = $true)]
    [string]$HtmlPath,
    [int]$HeadCount = 3,
    [int]$TailCount = 3
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $HtmlPath)) {
    throw "文件不存在: $HtmlPath"
}

$content = Get-Content -Raw -Encoding UTF8 -LiteralPath $HtmlPath
$options = [System.Text.RegularExpressions.RegexOptions]::Singleline
$sections = [regex]::Matches($content, '<section\b[^>]*class="([^"]*)"[^>]*data-index="(\d+)"[^>]*>(.*?)</section>', $options)

$titles = New-Object System.Collections.Generic.List[string]
foreach ($m in $sections) {
    $idx = [int]$m.Groups[2].Value + 1
    $body = $m.Groups[3].Value

    $titleMatch = [regex]::Match($body, '<h1\b[^>]*>(.*?)</h1>|<h2\b[^>]*>(.*?)</h2>|<h3\b[^>]*>(.*?)</h3>', $options)
    $raw = ''
    if ($titleMatch.Success) {
        if ($titleMatch.Groups[1].Success) { $raw = $titleMatch.Groups[1].Value }
        elseif ($titleMatch.Groups[2].Success) { $raw = $titleMatch.Groups[2].Value }
        else { $raw = $titleMatch.Groups[3].Value }
    }
    else {
        $topicMatch = [regex]::Match($body, '<span class="topic">(.*?)</span>', $options)
        if ($topicMatch.Success) { $raw = $topicMatch.Groups[1].Value }
        else { $raw = '[无标题]' }
    }

    $clean = [regex]::Replace($raw, '<[^>]+>', ' ')
    $clean = [System.Net.WebUtility]::HtmlDecode($clean)
    $clean = [regex]::Replace($clean, '\s+', ' ').Trim()
    $titles.Add("$idx:$clean") | Out-Null
}

Write-Output ("TOTAL=" + $titles.Count)
Write-Output ("FIRST=" + (($titles | Select-Object -First $HeadCount) -join ' || '))
Write-Output ("LAST=" + (($titles | Select-Object -Last $TailCount) -join ' || '))
