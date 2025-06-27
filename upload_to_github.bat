@echo off
setlocal enabledelayedexpansion

REM Upload script for GitHub releases
if "%~1"=="--help" (
    echo Usage: upload_to_github.bat [parameters]
    echo.
    echo Parameters:
    echo   --version ^<version^>        Version to upload (e.g., 1.3.0)
    echo   --token ^<token^>            GitHub Personal Access Token
    echo   --repo ^<repo^>              Repository name (owner/repo)
    echo   --help                       Show this help
    echo.
    echo Example:
    echo   upload_to_github.bat --version 1.3.0 --token ghp_xxx --repo username/CursorLauncher
    exit /b 0
)

REM Parse parameters
set "VERSION="
set "TOKEN="
set "REPO="

:parse_args
if "%~1"=="" goto :main
if /i "%~1"=="--version" (
    set "VERSION=%~2"
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="--token" (
    set "TOKEN=%~2"
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="--repo" (
    set "REPO=%~2"
    shift
    shift
    goto :parse_args
)
shift
goto :parse_args

:main
if not defined VERSION (
    echo ERROR: Version is required!
    echo Use --help for usage information
    exit /b 1
)

if not defined TOKEN (
    echo ERROR: Token is required!
    echo Use --help for usage information
    exit /b 1
)

if not defined REPO (
    echo ERROR: Repository is required!
    echo Use --help for usage information
    exit /b 1
)

echo ========================================
echo Uploading Cursor Launcher v%VERSION% to GitHub
echo ========================================

REM Check if files exist
set "ARCHIVE_PATH=release\CursorLauncher-v%VERSION%.zip"
set "EXE_PATH=release\CursorLauncher.exe"
set "SETUP_PATH=release\CursorLauncher-Setup-v%VERSION%.exe"

if not exist "%ARCHIVE_PATH%" (
    echo ERROR: Archive not found: %ARCHIVE_PATH%
    exit /b 1
)

if not exist "%EXE_PATH%" (
    echo ERROR: EXE file not found: %EXE_PATH%
    exit /b 1
)

echo Found files:
echo ✓ %ARCHIVE_PATH%
echo ✓ %EXE_PATH%
if exist "%SETUP_PATH%" (
    echo ✓ %SETUP_PATH%
)

echo.
echo IMPORTANT: This script requires PowerShell to be available.
echo Make sure you have created the release on GitHub first!
echo.
echo Files to upload:
echo - %ARCHIVE_PATH%
echo - %EXE_PATH%
if exist "%SETUP_PATH%" (
    echo - %SETUP_PATH%
)
echo.

set /p "CONFIRM=Continue with upload? (y/n): "
if /i not "!CONFIRM!"=="y" (
    echo Upload cancelled.
    exit /b 0
)

echo.
echo Starting upload...
echo Note: This will use PowerShell for the actual upload.
echo.

REM Call PowerShell script
powershell -ExecutionPolicy Bypass -Command "& { .\upload_to_github.ps1 -Version '%VERSION%' -Token '%TOKEN%' -Repo '%REPO%' }"

if errorlevel 1 (
    echo.
    echo Upload failed! Check the error messages above.
    echo.
    echo Troubleshooting:
    echo 1. Make sure the release exists on GitHub
    echo 2. Check your token permissions
    echo 3. Verify the repository name
    echo 4. Ensure PowerShell is available
) else (
    echo.
    echo ========================================
    echo Upload completed successfully!
    echo Check your GitHub release: https://github.com/%REPO%/releases/tag/v%VERSION%
    echo ========================================
)

pause 