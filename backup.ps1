param(
    [int]$IntervalSeconds = 30,
    [string]$Remote = "origin",
    [string]$Branch = "main"
)

$ErrorActionPreference = "Continue"

Write-Host "[backup] realtime backup started, checking every ${IntervalSeconds}s" -ForegroundColor Green

while ($true) {
    try {
        git add -A 2>$null

        $changes = git status --porcelain 2>$null
        if ($changes) {
            $ts = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
            git commit -m "auto-backup $ts" 2>$null
        }

        $unpushed = git log "origin/$Branch..HEAD" --oneline 2>$null
        if ($unpushed) {
            $ts = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
            $pushed = $false
            for ($i = 1; $i -le 3; $i++) {
                git push $Remote $Branch 2>$null
                if ($LASTEXITCODE -eq 0) { $pushed = $true; break }
                Start-Sleep -Seconds 10
            }
            if ($pushed) {
                Write-Host "[$ts] backup committed and pushed" -ForegroundColor Cyan
            } else {
                Write-Host "[$ts] push failed, will retry next round" -ForegroundColor Yellow
            }
        }
    } catch {
        Write-Host "[backup] error: $_" -ForegroundColor Red
    }
    Start-Sleep -Seconds $IntervalSeconds
}
