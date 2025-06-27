# Установка кодировки UTF-8 для корректного отображения русского текста
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

param(
    [string]$Version = "",
    [switch]$SkipTests,
    [switch]$SkipGit,
    [switch]$CreateInstaller,
    [switch]$Help
)

# Функция для отображения справки
function Show-Help {
    Write-Host "Использование: .\build_release.ps1 [параметры]" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Параметры:" -ForegroundColor Yellow
    Write-Host "  -Version <версия>        Версия для сборки (например: 1.2.0)" -ForegroundColor White
    Write-Host "  -SkipTests               Пропустить тесты" -ForegroundColor White
    Write-Host "  -SkipGit                 Пропустить Git операции" -ForegroundColor White
    Write-Host "  -CreateInstaller         Создать установщик" -ForegroundColor White
    Write-Host "  -Help                    Показать эту справку" -ForegroundColor White
    Write-Host ""
    Write-Host "Примеры:" -ForegroundColor Yellow
    Write-Host "  .\build_release.ps1" -ForegroundColor White
    Write-Host "  .\build_release.ps1 -Version 1.3.0" -ForegroundColor White
    Write-Host "  .\build_release.ps1 -SkipTests -CreateInstaller" -ForegroundColor White
}

if ($Help) {
    Show-Help
    exit 0
}

# Функция для проверки зависимостей
function Test-Dependencies {
    Write-Host "Проверка зависимостей..." -ForegroundColor Yellow
    
    $dependencies = @{
        "Python" = "python --version"
        "PyInstaller" = "pyinstaller --version"
        "Git" = "git --version"
    }
    
    $missing = @()
    
    foreach ($dep in $dependencies.GetEnumerator()) {
        try {
            $null = Invoke-Expression $dep.Value 2>$null
            Write-Host "✓ $($dep.Key)" -ForegroundColor Green
        }
        catch {
            Write-Host "✗ $($dep.Key) - не найден" -ForegroundColor Red
            $missing += $dep.Key
        }
    }
    
    if ($missing.Count -gt 0) {
        Write-Host ""
        Write-Host "Отсутствуют зависимости:" -ForegroundColor Red
        foreach ($dep in $missing) {
            Write-Host "  - $dep" -ForegroundColor Red
        }
        Write-Host ""
        Write-Host "Установите недостающие зависимости и попробуйте снова." -ForegroundColor Yellow
        exit 1
    }
}

# Функция для автоматического определения версии
function Get-Version {
    if ($Version -eq "") {
        # Попытка получить версию из Git тегов
        try {
            $latestTag = git describe --tags --abbrev=0 2>$null
            if ($latestTag) {
                $Version = $latestTag.TrimStart('v')
                Write-Host "Автоматически определена версия: $Version" -ForegroundColor Cyan
            } else {
                $Version = "1.0.0"
                Write-Host "Версия не найдена, используется: $Version" -ForegroundColor Yellow
            }
        }
        catch {
            $Version = "1.0.0"
            Write-Host "Версия не найдена, используется: $Version" -ForegroundColor Yellow
        }
    }
    return $Version
}

# Функция для проверки качества кода
function Test-CodeQuality {
    if ($SkipTests) {
        Write-Host "Проверка качества кода пропущена" -ForegroundColor Yellow
        return
    }
    
    Write-Host "Проверка качества кода..." -ForegroundColor Yellow
    
    # Проверка синтаксиса Python
    try {
        python -m py_compile launcher.py
        Write-Host "✓ Синтаксис launcher.py корректен" -ForegroundColor Green
    }
    catch {
        Write-Host "✗ Ошибка синтаксиса в launcher.py" -ForegroundColor Red
        exit 1
    }
    
    # Проверка импортов
    try {
        python -c "import launcher; print('✓ Импорты работают корректно')"
        Write-Host "✓ Импорты работают корректно" -ForegroundColor Green
    }
    catch {
        Write-Host "✗ Ошибка импортов" -ForegroundColor Red
        exit 1
    }
    
    # Проверка плагинов
    if (Test-Path "plugins") {
        $pluginFiles = Get-ChildItem "plugins" -Filter "*.py" | Where-Object { $_.Name -ne "__pycache__" }
        foreach ($plugin in $pluginFiles) {
            try {
                python -m py_compile $plugin.FullName
                Write-Host "✓ Синтаксис $($plugin.Name) корректен" -ForegroundColor Green
            }
            catch {
                Write-Host "✗ Ошибка синтаксиса в $($plugin.Name)" -ForegroundColor Red
                exit 1
            }
        }
    }
}

# Функция для создания установщика
function New-Installer {
    if (-not $CreateInstaller) {
        return
    }
    
    Write-Host "Создание установщика..." -ForegroundColor Yellow
    
    # Создание NSIS скрипта
    $nsisScript = @"
!include "MUI2.nsh"

Name "Cursor Launcher"
OutFile "CursorLauncher-Setup-v$Version.exe"
InstallDir "$PROGRAMFILES\CursorLauncher"
RequestExecutionLevel admin

!define MUI_ABORTWARNING
!define MUI_ICON "icon.ico"
!define MUI_UNICON "icon.ico"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "Russian"

Section "Cursor Launcher" SecMain
    SetOutPath "$INSTDIR"
    File "CursorLauncher.exe"
    File "README.md"
    File "USER_GUIDE.md"
    File "CHANGELOG.md"
    
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    
    CreateDirectory "$SMPROGRAMS\CursorLauncher"
    CreateShortCut "$SMPROGRAMS\CursorLauncher\Cursor Launcher.lnk" "$INSTDIR\CursorLauncher.exe"
    CreateShortCut "$SMPROGRAMS\CursorLauncher\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
    CreateShortCut "$DESKTOP\Cursor Launcher.lnk" "$INSTDIR\CursorLauncher.exe"
    
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CursorLauncher" "DisplayName" "Cursor Launcher"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CursorLauncher" "UninstallString" "$\"$INSTDIR\Uninstall.exe$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CursorLauncher" "DisplayIcon" "$INSTDIR\CursorLauncher.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CursorLauncher" "Publisher" "Cursor Launcher Team"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CursorLauncher" "DisplayVersion" "$Version"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CursorLauncher" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CursorLauncher" "NoRepair" 1
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\CursorLauncher.exe"
    Delete "$INSTDIR\README.md"
    Delete "$INSTDIR\USER_GUIDE.md"
    Delete "$INSTDIR\CHANGELOG.md"
    Delete "$INSTDIR\Uninstall.exe"
    
    RMDir "$INSTDIR"
    
    Delete "$SMPROGRAMS\CursorLauncher\Cursor Launcher.lnk"
    Delete "$SMPROGRAMS\CursorLauncher\Uninstall.lnk"
    RMDir "$SMPROGRAMS\CursorLauncher"
    Delete "$DESKTOP\Cursor Launcher.lnk"
    
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\CursorLauncher"
SectionEnd
"@
    
    $nsisScript | Out-File -FilePath "installer.nsi" -Encoding UTF8
    
    # Проверка наличия NSIS
    try {
        $null = Get-Command "makensis" -ErrorAction Stop
        & makensis installer.nsi
        if (Test-Path "CursorLauncher-Setup-v$Version.exe") {
            Copy-Item "CursorLauncher-Setup-v$Version.exe" "release\"
            Write-Host "✓ Установщик создан: CursorLauncher-Setup-v$Version.exe" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "✗ NSIS не найден. Установщик не создан." -ForegroundColor Yellow
        Write-Host "Установите NSIS для создания установщика." -ForegroundColor Yellow
    }
    
    # Очистка временных файлов
    if (Test-Path "installer.nsi") { Remove-Item "installer.nsi" -Force }
}

# Функция для создания релизных заметок
function New-ReleaseNotes {
    Write-Host "Создание релизных заметок..." -ForegroundColor Yellow
    
    $releaseNotes = @"
# Cursor Launcher v$Version

## Что нового
- Улучшения и исправления ошибок

## Установка
1. Скачайте архив CursorLauncher-v$Version.zip
2. Распакуйте в удобное место
3. Запустите CursorLauncher.exe

## Системные требования
- Windows 10/11
- .NET Framework 4.7.2 или выше

## Изменения
$(if (Test-Path "CHANGELOG.md") { Get-Content "CHANGELOG.md" | Select-Object -First 20 })

## Поддержка
Если у вас возникли проблемы, создайте issue на GitHub.
"@
    
    $releaseNotes | Out-File -FilePath "release\RELEASE_NOTES.md" -Encoding UTF8
}

# Основной процесс сборки
$Version = Get-Version

Write-Host "========================================" -ForegroundColor Green
Write-Host "Сборка Cursor Launcher v$Version" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Проверка зависимостей
Test-Dependencies
Write-Host ""

# Проверка качества кода
Test-CodeQuality
Write-Host ""

# Очистка предыдущих сборок
Write-Host "Очистка предыдущих сборок..." -ForegroundColor Yellow
if (Test-Path "dist") { Remove-Item "dist" -Recurse -Force }
if (Test-Path "build") { Remove-Item "build" -Recurse -Force }
if (Test-Path "launcher.spec") { Remove-Item "launcher.spec" -Force }
Write-Host "✓ Очистка завершена" -ForegroundColor Green

# Сборка .exe файла
Write-Host "Сборка .exe файла..." -ForegroundColor Yellow
$buildStart = Get-Date
pyinstaller --onefile --noconsole --name="CursorLauncher" --add-data "plugins;plugins" --add-data "*.json;." launcher.py
$buildEnd = Get-Date
$buildTime = $buildEnd - $buildStart

# Проверка успешности сборки
if (-not (Test-Path "dist\CursorLauncher.exe")) {
    Write-Host "ОШИБКА: Сборка не удалась!" -ForegroundColor Red
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

Write-Host "✓ Сборка завершена успешно! (Время: $($buildTime.TotalSeconds.ToString('F1')) сек)" -ForegroundColor Green

# Проверка размера файла
$fileSize = (Get-Item "dist\CursorLauncher.exe").Length
$fileSizeMB = [math]::Round($fileSize / 1MB, 2)
Write-Host "Размер файла: $fileSizeMB MB" -ForegroundColor Cyan

# Создание папки для релиза
if (-not (Test-Path "release")) { New-Item -ItemType Directory -Name "release" }

# Копирование файлов в папку релиза
Write-Host "Подготовка файлов для релиза..." -ForegroundColor Yellow
Copy-Item "dist\CursorLauncher.exe" "release\"
Copy-Item "README.md" "release\" -ErrorAction SilentlyContinue
Copy-Item "USER_GUIDE.md" "release\" -ErrorAction SilentlyContinue
Copy-Item "CHANGELOG.md" "release\" -ErrorAction SilentlyContinue
Copy-Item "plugins" "release\" -Recurse -ErrorAction SilentlyContinue
Copy-Item "*.json" "release\" -ErrorAction SilentlyContinue

# Создание релизных заметок
New-ReleaseNotes

# Создание архива
$archiveName = "CursorLauncher-v$Version.zip"
Write-Host "Создание архива $archiveName..." -ForegroundColor Yellow
Set-Location "release"
Compress-Archive -Path "*" -DestinationPath $archiveName -Force
Set-Location ".."

# Создание установщика
New-Installer

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Готово! Файлы для релиза созданы:" -ForegroundColor Green
Write-Host "release\$archiveName" -ForegroundColor Cyan
if ($CreateInstaller -and (Test-Path "release\CursorLauncher-Setup-v$Version.exe")) {
    Write-Host "release\CursorLauncher-Setup-v$Version.exe" -ForegroundColor Cyan
}
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Git операции
if (-not $SkipGit) {
    Write-Host "Следующие шаги:" -ForegroundColor Yellow
    Write-Host "1. Загрузите архив на GitHub в разделе Releases" -ForegroundColor White
    Write-Host "2. Создайте новый релиз с тегом v$Version" -ForegroundColor White
    Write-Host "3. Добавьте описание изменений" -ForegroundColor White
    Write-Host ""

    # Создание Git тега
    $createTag = Read-Host "Создать Git тег v$Version? (y/n)"
    if ($createTag -eq "y" -or $createTag -eq "Y") {
        try {
            git add .
            git commit -m "Release v$Version"
            git tag "v$Version"
            git push
            git push --tags
            Write-Host "✓ Git тег v$Version создан и отправлен на GitHub!" -ForegroundColor Green
        }
        catch {
            Write-Host "✗ Ошибка при работе с Git" -ForegroundColor Red
        }
    }
}

# Статистика сборки
Write-Host ""
Write-Host "Статистика сборки:" -ForegroundColor Cyan
Write-Host "Версия: $Version" -ForegroundColor White
Write-Host "Время сборки: $($buildTime.TotalSeconds.ToString('F1')) сек" -ForegroundColor White
Write-Host "Размер .exe: $fileSizeMB MB" -ForegroundColor White
Write-Host "Размер архива: $([math]::Round((Get-Item "release\$archiveName").Length / 1MB, 2)) MB" -ForegroundColor White

Read-Host "Нажмите Enter для выхода" 