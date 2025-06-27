# Улучшенные скрипты сборки Cursor Launcher

## Что нового

### PowerShell скрипт (`build_release.ps1`)
- ✅ Проверка зависимостей (Python, PyInstaller, Git)
- ✅ Автоматическое определение версии из Git тегов
- ✅ Проверка качества кода (синтаксис, импорты, плагины)
- ✅ Создание установщика с NSIS
- ✅ Генерация релизных заметок
- ✅ Статистика сборки (время, размеры)
- ✅ Параметры командной строки
- ✅ Цветной вывод с эмодзи

### Batch скрипт (`build_release.bat`)
- ✅ Те же функции, что и в PowerShell
- ✅ Совместимость с Windows CMD
- ✅ Параметры командной строки
- ✅ Проверка зависимостей

## Быстрый старт

### PowerShell (рекомендуется)
```powershell
# Разрешить выполнение скриптов (один раз)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Базовая сборка
.\build_release.ps1

# Сборка с параметрами
.\build_release.ps1 -Version "1.3.0" -CreateInstaller

# Справка
.\build_release.ps1 -Help
```

### Batch
```cmd
# Базовая сборка
.\build_release.bat

# Сборка с параметрами
.\build_release.bat --version 1.3.0 --create-installer

# Справка
.\build_release.bat --help
```

## Параметры

| PowerShell | Batch | Описание |
|------------|-------|----------|
| `-Version "1.3.0"` | `--version 1.3.0` | Указать версию |
| `-SkipTests` | `--skip-tests` | Пропустить тесты |
| `-SkipGit` | `--skip-git` | Пропустить Git операции |
| `-CreateInstaller` | `--create-installer` | Создать установщик |
| `-Help` | `--help` | Показать справку |

## Что проверяется

1. **Зависимости**: Python, PyInstaller, Git
2. **Качество кода**: синтаксис, импорты, плагины
3. **Сборка**: создание .exe с PyInstaller
4. **Релиз**: архив, заметки, установщик
5. **Git**: коммит, тег, push

## Создаваемые файлы

```
release/
├── CursorLauncher.exe
├── plugins/
├── *.json
├── README.md
├── USER_GUIDE.md
├── CHANGELOG.md
├── RELEASE_NOTES.md
└── CursorLauncher-v1.3.0.zip
```

## Установщик

Для создания установщика нужен NSIS:
1. Скачать с https://nsis.sourceforge.io/
2. Установить
3. Использовать параметр `-CreateInstaller`

## Примеры использования

```powershell
# Быстрая сборка для тестирования
.\build_release.ps1 -SkipTests -SkipGit

# Полная сборка с установщиком
.\build_release.ps1 -Version "1.3.0" -CreateInstaller

# Сборка для CI/CD
.\build_release.ps1 -Version $env:VERSION -SkipGit
```

## Устранение проблем

### PowerShell не выполняется
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### PyInstaller не найден
```bash
pip install pyinstaller
```

### NSIS не найден
- Установить NSIS с официального сайта
- Добавить в PATH или использовать полный путь

## Интеграция с CI/CD

```yaml
# GitHub Actions
- name: Build Release
  run: |
    .\build_release.ps1 -Version ${{ github.ref_name }} -SkipGit
```

```yaml
# GitLab CI
build_release:
  script:
    - ./build_release.ps1 -Version $CI_COMMIT_TAG -SkipGit
```

## Статистика

Скрипт выводит:
- Время сборки
- Размер .exe файла
- Размер архива
- Статус операций

## Поддержка

При проблемах:
1. Проверьте зависимости
2. Убедитесь в корректности кода
3. Проверьте права доступа
4. Используйте параметр `-Help` для справки 