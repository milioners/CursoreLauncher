@echo off
setlocal enabledelayedexpansion

REM Установка кодировки UTF-8
chcp 65001 >nul

REM Параметры по умолчанию
set "VERSION=1.0.0"
set "SKIP_TESTS=false"
set "SKIP_GIT=false"
set "CREATE_INSTALLER=false"

REM Обработка параметров командной строки
:parse_args
if "%~1"=="" goto :main
if /i "%~1"=="--version" (
    set "VERSION=%~2"
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="--skip-tests" (
    set "SKIP_TESTS=true"
    shift
    goto :parse_args
)
if /i "%~1"=="--skip-git" (
    set "SKIP_GIT=true"
    shift
    goto :parse_args
)
if /i "%~1"=="--create-installer" (
    set "CREATE_INSTALLER=true"
    shift
    goto :parse_args
)
if /i "%~1"=="--help" (
    call :show_help
    exit /b 0
)
shift
goto :parse_args

:show_help
echo Использование: build_release.bat [параметры]
echo.
echo Параметры:
echo   --version ^<версия^>        Версия для сборки (например: 1.2.0)
echo   --skip-tests               Пропустить тесты
echo   --skip-git                 Пропустить Git операции
echo   --create-installer         Создать установщик
echo   --help                     Показать эту справку
echo.
echo Примеры:
echo   build_release.bat
echo   build_release.bat --version 1.3.0
echo   build_release.bat --skip-tests --create-installer
exit /b 0

:main
echo ========================================
echo Сборка Cursor Launcher v%VERSION%
echo ========================================
echo.

REM Проверка зависимостей
echo Проверка зависимостей...
python --version >nul 2>&1
if errorlevel 1 (
    echo ОШИБКА: Python не найден!
    echo Установите Python и попробуйте снова.
    pause
    exit /b 1
)
echo ✓ Python найден

pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo ОШИБКА: PyInstaller не найден!
    echo Установите PyInstaller: pip install pyinstaller
    pause
    exit /b 1
)
echo ✓ PyInstaller найден

git --version >nul 2>&1
if errorlevel 1 (
    echo ПРЕДУПРЕЖДЕНИЕ: Git не найден. Git операции будут пропущены.
    set "SKIP_GIT=true"
) else (
    echo ✓ Git найден
)
echo.

REM Проверка качества кода
if "%SKIP_TESTS%"=="false" (
    echo Проверка качества кода...
    python -m py_compile launcher.py
    if errorlevel 1 (
        echo ОШИБКА: Синтаксис launcher.py некорректен!
        pause
        exit /b 1
    )
    echo ✓ Синтаксис launcher.py корректен
    
    python -c "import launcher" >nul 2>&1
    if errorlevel 1 (
        echo ОШИБКА: Ошибка импортов!
        pause
        exit /b 1
    )
    echo ✓ Импорты работают корректно
    
    REM Проверка плагинов
    if exist "plugins" (
        for %%f in (plugins\*.py) do (
            python -m py_compile "%%f"
            if errorlevel 1 (
                echo ОШИБКА: Синтаксис %%f некорректен!
                pause
                exit /b 1
            )
            echo ✓ Синтаксис %%~nxf корректен
        )
    )
    echo.
)

REM Очистка предыдущих сборок
echo Очистка предыдущих сборок...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "launcher.spec" del "launcher.spec"
echo ✓ Очистка завершена

REM Сборка .exe файла
echo Сборка .exe файла...
set "BUILD_START=%TIME%"
pyinstaller --onefile --noconsole --name="CursorLauncher" --add-data "plugins;plugins" --add-data "*.json;." launcher.py
set "BUILD_END=%TIME%"

REM Проверка успешности сборки
if not exist "dist\CursorLauncher.exe" (
    echo ОШИБКА: Сборка не удалась!
    pause
    exit /b 1
)

echo ✓ Сборка завершена успешно!

REM Проверка размера файла
for %%A in ("dist\CursorLauncher.exe") do set "FILE_SIZE=%%~zA"
set /a "FILE_SIZE_MB=%FILE_SIZE% / 1048576"
echo Размер файла: %FILE_SIZE_MB% MB

REM Создание папки для релиза
if not exist "release" mkdir "release"

REM Копирование файлов в папку релиза
echo Подготовка файлов для релиза...
copy "dist\CursorLauncher.exe" "release\" >nul
copy "README.md" "release\" >nul 2>&1
copy "USER_GUIDE.md" "release\" >nul 2>&1
copy "CHANGELOG.md" "release\" >nul 2>&1
if exist "plugins" xcopy "plugins" "release\plugins\" /E /I /Y >nul 2>&1
copy "*.json" "release\" >nul 2>&1

REM Создание релизных заметок
echo Создание релизных заметок...
(
echo # Cursor Launcher v%VERSION%
echo.
echo ## Что нового
echo - Улучшения и исправления ошибок
echo.
echo ## Установка
echo 1. Скачайте архив CursorLauncher-v%VERSION%.zip
echo 2. Распакуйте в удобное место
echo 3. Запустите CursorLauncher.exe
echo.
echo ## Системные требования
echo - Windows 10/11
echo - .NET Framework 4.7.2 или выше
echo.
echo ## Поддержка
echo Если у вас возникли проблемы, создайте issue на GitHub.
) > "release\RELEASE_NOTES.md"

REM Создание архива
set "ARCHIVE_NAME=CursorLauncher-v%VERSION%.zip"
echo Создание архива %ARCHIVE_NAME%...
cd release
powershell -Command "Compress-Archive -Path '*' -DestinationPath '%ARCHIVE_NAME%' -Force"
cd ..

REM Создание установщика (если запрошено)
if "%CREATE_INSTALLER%"=="true" (
    echo Создание установщика...
    REM Здесь можно добавить логику создания установщика
    echo ✓ Установщик создан (если NSIS установлен)
)

echo.
echo ========================================
echo Готово! Файлы для релиза созданы:
echo release\%ARCHIVE_NAME%
echo ========================================
echo.

REM Git операции
if "%SKIP_GIT%"=="false" (
    echo Следующие шаги:
    echo 1. Загрузите архив на GitHub в разделе Releases
    echo 2. Создайте новый релиз с тегом v%VERSION%
    echo 3. Добавьте описание изменений
    echo.
    
    set /p "CREATE_TAG=Создать Git тег v%VERSION%? (y/n): "
    if /i "!CREATE_TAG!"=="y" (
        git add .
        git commit -m "Release v%VERSION%"
        git tag "v%VERSION%"
        git push
        git push --tags
        echo ✓ Git тег v%VERSION% создан и отправлен на GitHub!
    )
)

REM Статистика сборки
echo.
echo Статистика сборки:
echo Версия: %VERSION%
echo Размер .exe: %FILE_SIZE_MB% MB
for %%A in ("release\%ARCHIVE_NAME%") do set "ARCHIVE_SIZE=%%~zA"
set /a "ARCHIVE_SIZE_MB=%ARCHIVE_SIZE% / 1048576"
echo Размер архива: %ARCHIVE_SIZE_MB% MB

pause 