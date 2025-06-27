# Быстрый старт: Загрузка файлов в GitHub релиз

## 🚀 Самый простой способ (Рекомендуется)

### 1. Соберите релиз
```cmd
.\build_release.bat --version 1.3.0
```

### 2. Создайте релиз на GitHub
1. Перейдите в ваш репозиторий
2. Нажмите **"Releases"** → **"Create a new release"**
3. Заполните:
   - **Tag version**: `v1.3.0`
   - **Release title**: `Cursor Launcher v1.3.0`
   - **Description**: Добавьте описание изменений
4. **НЕ публикуйте** пока!

### 3. Загрузите файлы
1. В разделе **"Attach binaries"** перетащите:
   - `release\CursorLauncher-v1.3.0.zip`
   - `release\CursorLauncher.exe` (опционально)
2. Нажмите **"Publish release"**

## 🔧 Автоматический способ

### 1. Создайте GitHub Token
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. **Generate new token** → **Generate new token (classic)**
3. Выберите `repo` (полный доступ)
4. Скопируйте токен (начинается с `ghp_`)

### 2. Загрузите файлы автоматически
```cmd
# Сначала соберите
.\build_release.bat --version 1.3.0

# Затем загрузите (замените на ваши данные)
.\upload_to_github.bat --version 1.3.0 --token ghp_your_token_here --repo username/CursorLauncher
```

## 📋 Что загружается

### Обязательно
- `CursorLauncher-v1.3.0.zip` - основной архив со всем

### Опционально
- `CursorLauncher.exe` - исполняемый файл отдельно
- `CursorLauncher-Setup-v1.3.0.exe` - установщик (если создали)

## ⚡ Быстрая команда

```cmd
# Все в одной строке
.\build_release.bat --version 1.3.0 && .\upload_to_github.bat --version 1.3.0 --token YOUR_TOKEN --repo YOUR_REPO
```

## 🔐 Безопасность токена

### Временное хранение
```cmd
set GITHUB_TOKEN=ghp_your_token_here
.\upload_to_github.bat --version 1.3.0 --token %GITHUB_TOKEN% --repo username/CursorLauncher
```

### Постоянное хранение
```cmd
setx GITHUB_TOKEN "ghp_your_token_here"
```

## 🚨 Частые проблемы

### "Release not found"
- Создайте релиз на GitHub перед загрузкой
- Проверьте правильность тега (`v1.3.0`)

### "Authentication failed"
- Проверьте токен (начинается с `ghp_`)
- Убедитесь, что токен имеет права `repo`

### "File not found"
- Запустите сборку: `.\build_release.bat --version 1.3.0`
- Проверьте папку `release\`

## 📊 Проверка результата

После загрузки:
1. Перейдите на страницу релиза
2. Убедитесь, что файлы загружены
3. Проверьте ссылки для скачивания
4. Посмотрите статистику загрузок

## 🎯 Готово!

Теперь пользователи могут скачать ваш Cursor Launcher прямо с GitHub! 🎉 