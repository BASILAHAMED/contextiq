$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

$env:PYTHONPATH = "src"
$outDir = Join-Path $root "build\contextiq-demo"

Write-Host "Running ContextIQ demo..."
python -m contextiq ingest examples --out $outDir

Write-Host ""
Write-Host "Generated files:"
Get-ChildItem $outDir | ForEach-Object { Write-Host "- $($_.Name)" }

Write-Host ""
Write-Host "Manifest summary:"
Get-Content (Join-Path $outDir "manifest.json")
