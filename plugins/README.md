# Система плагинов Cursor Launcher

Эта папка содержит плагины для расширения функциональности Cursor Launcher.

## Доступные плагины

### 1. Quick Launch Plugin (`quick_launch_plugin.py`)
- **Описание**: Добавляет кнопки быстрого запуска для часто используемых программ
- **Функции**: 
  - Автоматическое добавление программ в быстрый запуск при их использовании
  - Управление списком быстрого запуска
  - Кнопки в панели инструментов

### 2. Export/Import Plugin (`export_import_plugin.py`)
- **Описание**: Экспорт и импорт списка программ в различных форматах
- **Функции**:
  - Экспорт в JSON, CSV, TXT
  - Импорт из JSON, CSV
  - Создание резервных копий
  - Пункты меню "Файл"

## Создание собственного плагина

### 1. Базовый интерфейс плагина

```python
from plugin_system import PluginInterface

class MyPlugin(PluginInterface):
    def get_name(self) -> str:
        return "Мой плагин"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "Описание моего плагина"
    
    def get_author(self) -> str:
        return "Ваше имя"
    
    def initialize(self, launcher_instance) -> bool:
        self.launcher = launcher_instance
        return True
    
    def cleanup(self) -> bool:
        return True
```

### 2. Типы плагинов

#### MenuPluginInterface
Добавляет пункты в меню:
```python
from plugin_system import MenuPluginInterface

class MenuPlugin(MenuPluginInterface):
    def get_menu_items(self) -> List[Dict[str, Any]]:
        return [
            {
                'parent': 'Файл',
                'text': 'Мой пункт',
                'command': self.my_function,
                'separator': False
            }
        ]
```

#### ToolbarPluginInterface
Добавляет кнопки в панель инструментов:
```python
from plugin_system import ToolbarPluginInterface

class ToolbarPlugin(ToolbarPluginInterface):
    def get_toolbar_buttons(self) -> List[Dict[str, Any]]:
        return [
            {
                'text': 'Моя кнопка',
                'command': self.my_function,
                'tooltip': 'Подсказка',
                'icon': '🚀'
            }
        ]
```

#### EventPluginInterface
Реагирует на события:
```python
from plugin_system import EventPluginInterface

class EventPlugin(EventPluginInterface):
    def on_program_launched(self, program: Dict[str, Any]) -> None:
        # Код при запуске программы
        pass
    
    def on_program_added(self, program: Dict[str, Any]) -> None:
        # Код при добавлении программы
        pass
    
    def on_program_removed(self, program: Dict[str, Any]) -> None:
        # Код при удалении программы
        pass
```

### 3. Доступ к лаунчеру

В методе `initialize()` вы получаете доступ к экземпляру лаунчера:
```python
def initialize(self, launcher_instance) -> bool:
    self.launcher = launcher_instance
    # Доступ к программам: self.launcher.programs
    # Доступ к настройкам: self.launcher.settings
    # Доступ к главному окну: self.launcher.root
    return True
```

### 4. Создание окон

```python
import customtkinter as ctk

def show_my_window(self):
    window = ctk.CTkToplevel(self.launcher.root)
    window.title("Мое окно")
    window.geometry("400x300")
    # ... остальной код окна
```

## Установка плагина

1. Создайте файл `.py` в папке `plugins/`
2. Реализуйте один или несколько интерфейсов плагинов
3. Добавьте название плагина в `plugins_config.json`
4. Перезапустите лаунчер

## Примеры использования

### Простой плагин-счетчик запусков

```python
import json
from plugin_system import EventPluginInterface

class LaunchCounterPlugin(EventPluginInterface):
    def __init__(self):
        self.counter_file = "launch_counter.json"
        self.counters = self.load_counters()
    
    def get_name(self) -> str:
        return "Launch Counter"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "Считает количество запусков каждой программы"
    
    def get_author(self) -> str:
        return "Developer"
    
    def initialize(self, launcher_instance) -> bool:
        self.launcher = launcher_instance
        return True
    
    def cleanup(self) -> bool:
        self.save_counters()
        return True
    
    def load_counters(self):
        try:
            with open(self.counter_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_counters(self):
        with open(self.counter_file, 'w') as f:
            json.dump(self.counters, f)
    
    def on_program_launched(self, program: Dict[str, Any]) -> None:
        name = program.get('name', 'Unknown')
        self.counters[name] = self.counters.get(name, 0) + 1
        self.save_counters()
```

## Лучшие практики

1. **Обработка ошибок**: Всегда оборачивайте критический код в try-except
2. **Ресурсы**: Освобождайте ресурсы в методе `cleanup()`
3. **Именование**: Используйте уникальные имена для файлов и классов
4. **Документация**: Добавляйте комментарии к коду
5. **Тестирование**: Тестируйте плагин перед публикацией

## Устранение неполадок

### Плагин не загружается
- Проверьте синтаксис Python
- Убедитесь, что класс наследуется от правильного интерфейса
- Проверьте, что название плагина добавлено в конфигурацию

### Ошибки в консоли
- Проверьте логи в консоли
- Убедитесь, что все импорты корректны
- Проверьте доступ к файлам и папкам

### Плагин не работает
- Проверьте метод `initialize()` - он должен возвращать `True`
- Убедитесь, что плагин правильно обрабатывает события
- Проверьте доступ к экземпляру лаунчера 