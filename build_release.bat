@echo off
echo ========================================
echo Сборка Cursor Launcher для релиза
echo ========================================

REM Очистка предыдущих сборок
echo Очистка предыдущих сборок...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "launcher.spec" del "launcher.spec"

REM Сборка .exe файла
echo Сборка .exe файла...
pyinstaller --onefile --noconsole --name="CursorLauncher" launcher.py

REM Проверка успешности сборки
if not exist "dist\CursorLauncher.exe" (
    echo ОШИБКА: Сборка не удалась!
    pause
    exit /b 1
)

echo Сборка завершена успешно!

REM Создание папки для релиза
if not exist "release" mkdir "release"

REM Копирование файлов в папку релиза
echo Подготовка файлов для релиза...
copy "dist\CursorLauncher.exe" "release\"
copy "README.md" "release\"
copy "USER_GUIDE.md" "release\"
copy "CHANGELOG.md" "release\"

REM Создание архива
echo Создание архива...
cd release
powershell -Command "Compress-Archive -Path 'CursorLauncher.exe', 'README.md', 'USER_GUIDE.md', 'CHANGELOG.md' -DestinationPath 'CursorLauncher-v1.1.0.zip' -Force"
cd ..

echo ========================================
echo Готово! Архив для релиза создан:
echo release\CursorLauncher-v1.1.0.zip
echo ========================================
echo.
echo Следующие шаги:
echo 1. Загрузите архив на GitHub в разделе Releases
echo 2. Создайте новый релиз с тегом v1.1.0
echo 3. Добавьте описание изменений
echo.
pause 