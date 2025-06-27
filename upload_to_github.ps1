# Script for uploading files to GitHub release
param(
    [string]$Version = "",
    [string]$Token = "",
    [string]$Repo = "",
    [switch]$Help
)

if ($Help) {
    Write-Host "Usage: .\upload_to_github.ps1 [parameters]" -ForegroundColor Cyan
    Write-Host "Parameters:" -ForegroundColor Yellow
    Write-Host "  -Version <version>        Version to upload (e.g., 1.3.0)" -ForegroundColor White
    Write-Host "  -Token <token>            GitHub Personal Access Token" -ForegroundColor White
    Write-Host "  -Repo <repo>              Repository name (owner/repo)" -ForegroundColor White
    Write-Host "  -Help                     Show this help" -ForegroundColor White
    Write-Host ""
    Write-Host "Example:" -ForegroundColor Yellow
    Write-Host "  .\upload_to_github.ps1 -Version 1.3.0 -Token ghp_xxx -Repo username/CursorLauncher" -ForegroundColor White
    exit 0
}

if (-not $Version -or -not $Token -or -not $Repo) {
    Write-Host "ERROR: All parameters are required!" -ForegroundColor Red
    Write-Host "Use -Help for usage information" -ForegroundColor Yellow
    exit 1
}

Write-Host "========================================" -ForegroundColor Green
Write-Host "Uploading Cursor Launcher v$Version to GitHub" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Check if files exist
$archivePath = "release\CursorLauncher-v$Version.zip"
$exePath = "release\CursorLauncher.exe"
$setupPath = "release\CursorLauncher-Setup-v$Version.exe"

if (-not (Test-Path $archivePath)) {
    Write-Host "ERROR: Archive not found: $archivePath" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $exePath)) {
    Write-Host "ERROR: EXE file not found: $exePath" -ForegroundColor Red
    exit 1
}

Write-Host "Found files:" -ForegroundColor Yellow
Write-Host "✓ $archivePath" -ForegroundColor Green
Write-Host "✓ $exePath" -ForegroundColor Green
if (Test-Path $setupPath) {
    Write-Host "✓ $setupPath" -ForegroundColor Green
}

# Get release ID
Write-Host "Getting release information..." -ForegroundColor Yellow
$headers = @{
    "Authorization" = "token $Token"
    "Accept" = "application/vnd.github.v3+json"
}

$releaseUrl = "https://api.github.com/repos/$Repo/releases/tags/v$Version"
try {
    $release = Invoke-RestMethod -Uri $releaseUrl -Headers $headers -Method Get
    $releaseId = $release.id
    Write-Host "✓ Found release ID: $releaseId" -ForegroundColor Green
}
catch {
    Write-Host "ERROR: Release v$Version not found!" -ForegroundColor Red
    Write-Host "Create the release first on GitHub" -ForegroundColor Yellow
    exit 1
}

# Upload files
$filesToUpload = @($archivePath, $exePath)
if (Test-Path $setupPath) {
    $filesToUpload += $setupPath
}

foreach ($file in $filesToUpload) {
    $fileName = Split-Path $file -Leaf
    Write-Host "Uploading $fileName..." -ForegroundColor Yellow
    
    $uploadUrl = "https://uploads.github.com/repos/$Repo/releases/$releaseId/assets?name=$fileName"
    
    try {
        $fileBytes = [System.IO.File]::ReadAllBytes($file)
        $response = Invoke-RestMethod -Uri $uploadUrl -Headers $headers -Method Post -Body $fileBytes -ContentType "application/octet-stream"
        Write-Host "✓ Uploaded: $fileName" -ForegroundColor Green
    }
    catch {
        Write-Host "✗ Failed to upload: $fileName" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Upload completed!" -ForegroundColor Green
Write-Host "Check your GitHub release: https://github.com/$Repo/releases/tag/v$Version" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green 