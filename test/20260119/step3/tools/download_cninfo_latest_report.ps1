param(
  [Parameter(Mandatory=$true)]
  [string[]]$Codes,

  [Parameter(Mandatory=$true)]
  [string]$OutDir
)

$ErrorActionPreference = "Stop"

function Get-CninfoColumn([string]$code) {
  if ($code.StartsWith("6")) { return "sse" }
  if ($code.StartsWith("8") -or $code.StartsWith("4")) { return "bj" }
  return "szse"
}

$ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
$referer = "http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search"

$headers = @{
  "User-Agent" = $ua
  "Referer" = $referer
  "X-Requested-With" = "XMLHttpRequest"
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
Invoke-WebRequest -Uri "http://www.cninfo.com.cn/" -WebSession $session -Headers $headers | Out-Null

# orgId mapping is easiest from szse_stock.json; it includes many A-shares (not only SZ) in practice.
$stockJson = Invoke-RestMethod -Uri "http://www.cninfo.com.cn/new/data/szse_stock.json" -WebSession $session -Headers $headers

$categories = @(
  @{ name = "年报"; code = "category_ndbg_szsh" },
  @{ name = "半年报"; code = "category_bndbg_szsh" },
  @{ name = "一季报"; code = "category_yjdbg_szsh" },
  @{ name = "三季报"; code = "category_sjdbg_szsh" }
)

function Get-LatestReportAnnouncement($code, $orgId, $column) {
  $start = (Get-Date).AddYears(-3).ToString("yyyy-MM-dd")
  $end = (Get-Date).ToString("yyyy-MM-dd")

  $all = @()
  foreach ($cat in $categories) {
    $body = @{
      pageNum   = "1"
      pageSize  = "30"
      column    = $column
      tabName   = "fulltext"
      plate     = ""
      stock     = "$code,$orgId"
      searchkey = ""
      secid     = ""
      category  = $cat.code
      trade     = ""
      seDate    = "$start~$end"
      sortName  = ""
      sortType  = ""
      isHLtitle = "true"
    }

    try {
      $res = Invoke-RestMethod -Method Post -Uri "http://www.cninfo.com.cn/new/hisAnnouncement/query" -WebSession $session -Headers $headers -ContentType "application/x-www-form-urlencoded; charset=UTF-8" -Body $body
      if ($res -and $res.announcements) {
        $res.announcements | ForEach-Object {
          $_ | Add-Member -NotePropertyName categoryName -NotePropertyValue $cat.name -Force
          $_ | Add-Member -NotePropertyName categoryCode -NotePropertyValue $cat.code -Force
        }
        $all += $res.announcements
      }
    } catch {
      # ignore individual category failure; we will continue
    }

    Start-Sleep -Milliseconds 250
  }

  if (-not $all -or $all.Count -eq 0) {
    return $null
  }

  return $all | Sort-Object -Property announcementTime -Descending | Select-Object -First 1
}

foreach ($code in $Codes) {
  $hit = $stockJson.stockList | Where-Object { $_.code -eq $code } | Select-Object -First 1
  if (-not $hit) {
    Write-Warning "[SKIP] orgId not found for code=$code"
    continue
  }

  $orgId = $hit.orgId
  $column = Get-CninfoColumn $code

  $ann = Get-LatestReportAnnouncement -code $code -orgId $orgId -column $column
  if (-not $ann) {
    Write-Warning "[SKIP] no report announcement found for code=$code"
    continue
  }

  $tz = [TimeZoneInfo]::FindSystemTimeZoneById("China Standard Time")
  $dtUtc = [DateTimeOffset]::FromUnixTimeMilliseconds([int64]$ann.announcementTime).UtcDateTime
  $dtCn  = [TimeZoneInfo]::ConvertTimeFromUtc($dtUtc, $tz)
  $announceDate = $dtCn.ToString("yyyy-MM-dd")

  $announcementId = $ann.announcementId
  $title = $ann.announcementTitle
  $safeTitle = ($title -replace '[\\/:*?"<>|]', '_')

  $codeDir = Join-Path $OutDir $code
  New-Item -ItemType Directory -Force -Path $codeDir | Out-Null

  $outFile = Join-Path $codeDir ("{0}_{1}_{2}.pdf" -f $code, $ann.categoryName, $safeTitle)

  # Prefer direct download endpoint; fallback to static URL
  $downloadUrl = "http://www.cninfo.com.cn/new/announcement/download?bulletinId=$announcementId&announceTime=$announceDate"

  $ok = $false
  try {
    Invoke-WebRequest -Uri $downloadUrl -WebSession $session -Headers $headers -OutFile $outFile
    $ok = $true
  } catch {
    $ok = $false
  }

  if (-not $ok -and $ann.adjunctUrl) {
    $staticUrl = "http://static.cninfo.com.cn/$($ann.adjunctUrl)"
    try {
      Invoke-WebRequest -Uri $staticUrl -WebSession $session -Headers $headers -OutFile $outFile
      $ok = $true
    } catch {
      $ok = $false
    }
  }

  if ($ok) {
    Write-Host "[OK] $code -> $outFile" -ForegroundColor Green
  } else {
    Write-Warning "[FAIL] download failed for code=$code (announcementId=$announcementId)"
  }

  Start-Sleep -Milliseconds 400
}
