# Установка кодировки UTF-8 для корректного отображения русского текста
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

param(
    [string]$Version = "1.1.1"
)

Write-Host "========================================" -ForegroundColor Green
Write-Host "Сборка Cursor Launcher v$Version" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Очистка предыдущих сборок
Write-Host "Очистка предыдущих сборок..." -ForegroundColor Yellow
if (Test-Path "dist") { Remove-Item "dist" -Recurse -Force }
if (Test-Path "build") { Remove-Item "build" -Recurse -Force }
if (Test-Path "launcher.spec") { Remove-Item "launcher.spec" -Force }

# Сборка .exe файла
Write-Host "Сборка .exe файла..." -ForegroundColor Yellow
pyinstaller --onefile --noconsole --name="CursorLauncher" launcher.py

# Проверка успешности сборки
if (-not (Test-Path "dist\CursorLauncher.exe")) {
    Write-Host "ОШИБКА: Сборка не удалась!" -ForegroundColor Red
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

Write-Host "Сборка завершена успешно!" -ForegroundColor Green

# Создание папки для релиза
if (-not (Test-Path "release")) { New-Item -ItemType Directory -Name "release" }

# Копирование файлов в папку релиза
Write-Host "Подготовка файлов для релиза..." -ForegroundColor Yellow
Copy-Item "dist\CursorLauncher.exe" "release\"
Copy-Item "README.md" "release\" -ErrorAction SilentlyContinue
Copy-Item "USER_GUIDE.md" "release\" -ErrorAction SilentlyContinue
Copy-Item "CHANGELOG.md" "release\" -ErrorAction SilentlyContinue

# Создание архива
$archiveName = "CursorLauncher-v$Version.zip"
Write-Host "Создание архива $archiveName..." -ForegroundColor Yellow
Set-Location "release"
Compress-Archive -Path "CursorLauncher.exe", "README.md", "USER_GUIDE.md", "CHANGELOG.md" -DestinationPath $archiveName -Force
Set-Location ".."

Write-Host "========================================" -ForegroundColor Green
Write-Host "Готово! Архив для релиза создан:" -ForegroundColor Green
Write-Host "release\$archiveName" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Следующие шаги:" -ForegroundColor Yellow
Write-Host "1. Загрузите архив на GitHub в разделе Releases" -ForegroundColor White
Write-Host "2. Создайте новый релиз с тегом v$Version" -ForegroundColor White
Write-Host "3. Добавьте описание изменений" -ForegroundColor White
Write-Host ""

# Создание Git тега
$createTag = Read-Host "Создать Git тег v$Version? (y/n)"
if ($createTag -eq "y" -or $createTag -eq "Y") {
    git add .
    git commit -m "Release v$Version"
    git tag "v$Version"
    git push
    git push --tags
    Write-Host "Git тег v$Version создан и отправлен на GitHub!" -ForegroundColor Green
}

Read-Host "Нажмите Enter для выхода" 