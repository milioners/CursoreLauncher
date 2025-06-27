# Руководство по загрузке файлов в GitHub релиз

## 🚀 Способ 1: Через веб-интерфейс GitHub (Рекомендуется)

### Шаг 1: Создание релиза
1. Перейдите в ваш репозиторий на GitHub
2. Нажмите на вкладку **"Releases"** (или **"Релизы"**)
3. Нажмите **"Create a new release"** (или **"Создать новый релиз"**)

### Шаг 2: Настройка релиза
```
Tag version: v1.3.0
Release title: Cursor Launcher v1.3.0
Description: 
## Что нового
- Улучшения и исправления ошибок
- Добавлена поддержка плагинов
- Обновленный интерфейс

## Установка
1. Скачайте архив CursorLauncher-v1.3.0.zip
2. Распакуйте в удобное место
3. Запустите CursorLauncher.exe

## Системные требования
- Windows 10/11
- .NET Framework 4.7.2 или выше
```

### Шаг 3: Загрузка файлов
1. В разделе **"Attach binaries by dropping them here or selecting them"**
2. Перетащите файлы из папки `release/`:
   - `CursorLauncher-v1.3.0.zip` - основной архив
   - `CursorLauncher.exe` - исполняемый файл (опционально)
   - `CursorLauncher-Setup-v1.3.0.exe` - установщик (если создали)

### Шаг 4: Публикация
- Нажмите **"Publish release"** (или **"Опубликовать релиз"**)

## 🔧 Способ 2: Автоматическая загрузка через скрипт

### Шаг 1: Создание GitHub Token
1. Перейдите в **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Нажмите **"Generate new token"**
3. Выберите **"Generate new token (classic)"**
4. Установите права:
   - ✅ `repo` (полный доступ к репозиториям)
   - ✅ `write:packages` (если нужно)
5. Скопируйте токен (он показывается только один раз!)

### Шаг 2: Использование скрипта загрузки

```powershell
# Сначала соберите релиз
.\build_release.bat --version 1.3.0

# Затем загрузите файлы
.\upload_to_github.ps1 -Version 1.3.0 -Token "ghp_your_token_here" -Repo "username/CursorLauncher"
```

### Шаг 3: Создание релиза через API (если нужно)

Если релиз еще не создан, можно создать его автоматически:

```powershell
# Создание релиза через API
$headers = @{
    "Authorization" = "token ghp_your_token_here"
    "Accept" = "application/vnd.github.v3+json"
}

$releaseData = @{
    tag_name = "v1.3.0"
    name = "Cursor Launcher v1.3.0"
    body = "## Что нового`n- Улучшения и исправления ошибок`n- Добавлена поддержка плагинов"
    draft = $false
    prerelease = $false
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "https://api.github.com/repos/username/CursorLauncher/releases" -Headers $headers -Method Post -Body $releaseData
```

## 📋 Полный процесс создания релиза

### 1. Подготовка
```cmd
# Очистка и сборка
.\build_release.bat --version 1.3.0
```

### 2. Создание релиза на GitHub
- Через веб-интерфейс (рекомендуется)
- Или через API

### 3. Загрузка файлов
```powershell
# Автоматическая загрузка
.\upload_to_github.ps1 -Version 1.3.0 -Token "ghp_xxx" -Repo "username/CursorLauncher"
```

### 4. Проверка
- Перейдите на страницу релиза
- Убедитесь, что все файлы загружены
- Проверьте ссылки для скачивания

## 🔐 Безопасность токенов

### Хранение токена
```powershell
# Сохранение токена в переменной окружения
[Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "ghp_your_token_here", "User")

# Использование в скрипте
$token = [Environment]::GetEnvironmentVariable("GITHUB_TOKEN", "User")
```

### Файл конфигурации
Создайте файл `.env` (не добавляйте в Git):
```
GITHUB_TOKEN=ghp_your_token_here
GITHUB_REPO=username/CursorLauncher
```

## 📁 Структура файлов для загрузки

```
release/
├── CursorLauncher-v1.3.0.zip       # Основной архив (обязательно)
├── CursorLauncher.exe              # Исполняемый файл (опционально)
├── CursorLauncher-Setup-v1.3.0.exe # Установщик (опционально)
├── README.md                       # Документация
├── USER_GUIDE.md                   # Руководство пользователя
└── CHANGELOG.md                    # История изменений
```

## 🎯 Рекомендации

### Для пользователей
- **Основной архив** - содержит все необходимое
- **Исполняемый файл** - для быстрого доступа
- **Установщик** - для удобной установки

### Для разработчиков
- **Исходный код** - в репозитории
- **Документация** - в README и релизных заметках
- **Чейнджлог** - для отслеживания изменений

## 🚨 Устранение проблем

### Ошибка "Release not found"
- Создайте релиз на GitHub перед загрузкой файлов
- Проверьте правильность тега версии

### Ошибка "Authentication failed"
- Проверьте правильность токена
- Убедитесь, что токен имеет права `repo`

### Ошибка "File too large"
- GitHub имеет лимит 2GB на файл
- Используйте сжатие или разделите файлы

### Ошибка "Rate limit exceeded"
- GitHub API имеет лимиты
- Подождите или используйте веб-интерфейс

## 📊 Статистика загрузок

После загрузки вы можете отслеживать:
- Количество скачиваний каждого файла
- Популярность релизов
- Обратную связь пользователей

## 🔄 Автоматизация

### GitHub Actions
```yaml
name: Build and Release
on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build Release
        run: .\build_release.bat --version ${{ github.ref_name }}
      - name: Upload to Release
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./release/CursorLauncher-${{ github.ref_name }}.zip
          asset_name: CursorLauncher-${{ github.ref_name }}.zip
          asset_content_type: application/zip
```

Теперь у вас есть полное руководство по загрузке файлов в GitHub релиз! 🎉 