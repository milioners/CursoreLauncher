import os
import json
import importlib.util
import inspect
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import tkinter as tk
import customtkinter as ctk

class PluginInterface(ABC):
    """Базовый интерфейс для всех плагинов"""
    
    @abstractmethod
    def get_name(self) -> str:
        """Возвращает название плагина"""
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        """Возвращает версию плагина"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Возвращает описание плагина"""
        pass
    
    @abstractmethod
    def get_author(self) -> str:
        """Возвращает автора плагина"""
        pass
    
    @abstractmethod
    def initialize(self, launcher_instance) -> bool:
        """Инициализация плагина"""
        pass
    
    @abstractmethod
    def cleanup(self) -> bool:
        """Очистка ресурсов плагина"""
        pass

class MenuPluginInterface(PluginInterface):
    """Интерфейс для плагинов, добавляющих пункты меню"""
    
    @abstractmethod
    def get_menu_items(self) -> List[Dict[str, Any]]:
        """Возвращает список пунктов меню для добавления"""
        pass

class ToolbarPluginInterface(PluginInterface):
    """Интерфейс для плагинов, добавляющих кнопки в панель инструментов"""
    
    @abstractmethod
    def get_toolbar_buttons(self) -> List[Dict[str, Any]]:
        """Возвращает список кнопок для панели инструментов"""
        pass

class ContextMenuPluginInterface(PluginInterface):
    """Интерфейс для плагинов, добавляющих контекстное меню"""
    
    @abstractmethod
    def get_context_menu_items(self, context: str) -> List[Dict[str, Any]]:
        """Возвращает пункты контекстного меню для заданного контекста"""
        pass

class EventPluginInterface(PluginInterface):
    """Интерфейс для плагинов, реагирующих на события"""
    
    @abstractmethod
    def on_program_launched(self, program: Dict[str, Any]) -> None:
        """Вызывается при запуске программы"""
        pass
    
    @abstractmethod
    def on_program_added(self, program: Dict[str, Any]) -> None:
        """Вызывается при добавлении программы"""
        pass
    
    @abstractmethod
    def on_program_removed(self, program: Dict[str, Any]) -> None:
        """Вызывается при удалении программы"""
        pass

class PluginManager:
    """Менеджер плагинов"""
    
    def __init__(self, launcher_instance):
        self.launcher = launcher_instance
        self.plugins: Dict[str, PluginInterface] = {}
        self.plugins_dir = "plugins"
        self.plugins_config_file = "plugins_config.json"
        self.enabled_plugins = self.load_plugins_config()
        
        # Создаем папку для плагинов, если её нет
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir)
    
    def load_plugins_config(self) -> List[str]:
        """Загрузка конфигурации плагинов"""
        if os.path.exists(self.plugins_config_file):
            try:
                with open(self.plugins_config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get('enabled_plugins', [])
            except Exception as e:
                print(f"Ошибка загрузки конфигурации плагинов: {e}")
        return []
    
    def save_plugins_config(self):
        """Сохранение конфигурации плагинов"""
        config = {
            'enabled_plugins': list(self.plugins.keys())
        }
        try:
            with open(self.plugins_config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения конфигурации плагинов: {e}")
    
    def discover_plugins(self) -> List[str]:
        """Поиск доступных плагинов"""
        plugin_files = []
        if os.path.exists(self.plugins_dir):
            for file in os.listdir(self.plugins_dir):
                if file.endswith('.py') and not file.startswith('__'):
                    plugin_files.append(file)
        return plugin_files
    
    def load_plugin(self, plugin_file: str) -> Optional[PluginInterface]:
        """Загрузка плагина из файла"""
        try:
            plugin_path = os.path.join(self.plugins_dir, plugin_file)
            spec = importlib.util.spec_from_file_location("plugin", plugin_path)
            if spec is None or spec.loader is None:
                print(f"Не удалось создать спецификацию для плагина {plugin_file}")
                return None
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Ищем класс плагина в модуле
            for name, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, PluginInterface)
                    and obj is not PluginInterface
                    and not inspect.isabstract(obj)
                ):
                    return obj()
            
            print(f"Плагин {plugin_file} не содержит валидного класса плагина")
            return None
            
        except Exception as e:
            print(f"Ошибка загрузки плагина {plugin_file}: {e}")
            return None
    
    def initialize_plugins(self):
        """Инициализация всех плагинов"""
        plugin_files = self.discover_plugins()
        
        for plugin_file in plugin_files:
            plugin = self.load_plugin(plugin_file)
            if plugin:
                plugin_name = plugin.get_name()
                if plugin_name in self.enabled_plugins:
                    if plugin.initialize(self.launcher):
                        self.plugins[plugin_name] = plugin
                        print(f"Плагин {plugin_name} успешно загружен")
                    else:
                        print(f"Ошибка инициализации плагина {plugin_name}")
    
    def get_menu_items(self) -> List[Dict[str, Any]]:
        """Получение всех пунктов меню от плагинов"""
        menu_items = []
        for plugin in self.plugins.values():
            if isinstance(plugin, MenuPluginInterface):
                menu_items.extend(plugin.get_menu_items())
        return menu_items
    
    def get_toolbar_buttons(self) -> List[Dict[str, Any]]:
        """Получение всех кнопок панели инструментов от плагинов"""
        toolbar_buttons = []
        for plugin in self.plugins.values():
            if isinstance(plugin, ToolbarPluginInterface):
                toolbar_buttons.extend(plugin.get_toolbar_buttons())
        return toolbar_buttons
    
    def get_context_menu_items(self, context: str) -> List[Dict[str, Any]]:
        """Получение пунктов контекстного меню от плагинов"""
        context_items = []
        for plugin in self.plugins.values():
            if isinstance(plugin, ContextMenuPluginInterface):
                context_items.extend(plugin.get_context_menu_items(context))
        return context_items
    
    def on_program_launched(self, program: Dict[str, Any]):
        """Уведомление плагинов о запуске программы"""
        for plugin in self.plugins.values():
            if isinstance(plugin, EventPluginInterface):
                try:
                    plugin.on_program_launched(program)
                except Exception as e:
                    print(f"Ошибка в плагине {plugin.get_name()}: {e}")
    
    def on_program_added(self, program: Dict[str, Any]):
        """Уведомление плагинов о добавлении программы"""
        for plugin in self.plugins.values():
            if isinstance(plugin, EventPluginInterface):
                try:
                    plugin.on_program_added(program)
                except Exception as e:
                    print(f"Ошибка в плагине {plugin.get_name()}: {e}")
    
    def on_program_removed(self, program: Dict[str, Any]):
        """Уведомление плагинов об удалении программы"""
        for plugin in self.plugins.values():
            if isinstance(plugin, EventPluginInterface):
                try:
                    plugin.on_program_removed(program)
                except Exception as e:
                    print(f"Ошибка в плагине {plugin.get_name()}: {e}")
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """Включение плагина"""
        if plugin_name not in self.enabled_plugins:
            self.enabled_plugins.append(plugin_name)
            self.save_plugins_config()
            return True
        return False
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """Отключение плагина"""
        if plugin_name in self.enabled_plugins:
            self.enabled_plugins.remove(plugin_name)
            if plugin_name in self.plugins:
                self.plugins[plugin_name].cleanup()
                del self.plugins[plugin_name]
            self.save_plugins_config()
            return True
        return False
    
    def get_plugin_info(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """Получение информации о плагине"""
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
            return {
                'name': plugin.get_name(),
                'version': plugin.get_version(),
                'description': plugin.get_description(),
                'author': plugin.get_author(),
                'enabled': True
            }
        return None
    
    def get_all_plugins_info(self) -> List[Dict[str, Any]]:
        """Получение информации о всех плагинах"""
        plugins_info = []
        
        # Информация о загруженных плагинах
        for plugin_name in self.plugins:
            info = self.get_plugin_info(plugin_name)
            if info:
                plugins_info.append(info)
        
        # Информация о доступных, но не загруженных плагинах
        plugin_files = self.discover_plugins()
        for plugin_file in plugin_files:
            plugin = self.load_plugin(plugin_file)
            if plugin:
                plugin_name = plugin.get_name()
                if plugin_name not in self.plugins:
                    plugins_info.append({
                        'name': plugin_name,
                        'version': plugin.get_version(),
                        'description': plugin.get_description(),
                        'author': plugin.get_author(),
                        'enabled': False
                    })
        
        return plugins_info
    
    def cleanup(self):
        """Очистка всех плагинов"""
        for plugin in self.plugins.values():
            try:
                plugin.cleanup()
            except Exception as e:
                print(f"Ошибка очистки плагина {plugin.get_name()}: {e}")
        self.plugins.clear() 