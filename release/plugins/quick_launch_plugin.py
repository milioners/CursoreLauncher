import os
import json
from typing import Dict, List, Any
import customtkinter as ctk
from tkinter import messagebox, simpledialog
from plugin_system import ToolbarPluginInterface, EventPluginInterface

class QuickLaunchPlugin(ToolbarPluginInterface, EventPluginInterface):
    """Плагин быстрого запуска - добавляет кнопки для часто используемых программ"""
    
    def __init__(self):
        self.launcher = None
        self.quick_launch_file = "quick_launch.json"
        self.quick_programs = self.load_quick_launch()
        self.max_quick_programs = 5
    
    def get_name(self) -> str:
        return "Quick Launch"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "Добавляет кнопки быстрого запуска для часто используемых программ"
    
    def get_author(self) -> str:
        return "Cursor Launcher Team"
    
    def initialize(self, launcher_instance) -> bool:
        self.launcher = launcher_instance
        return True
    
    def cleanup(self) -> bool:
        self.save_quick_launch()
        return True
    
    def load_quick_launch(self) -> List[str]:
        """Загрузка списка программ быстрого запуска"""
        if os.path.exists(self.quick_launch_file):
            try:
                with open(self.quick_launch_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Ошибка загрузки быстрого запуска: {e}")
        return []
    
    def save_quick_launch(self):
        """Сохранение списка программ быстрого запуска"""
        try:
            with open(self.quick_launch_file, 'w', encoding='utf-8') as f:
                json.dump(self.quick_programs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения быстрого запуска: {e}")
    
    def add_to_quick_launch(self, program_name: str):
        """Добавление программы в быстрый запуск"""
        if program_name not in self.quick_programs:
            self.quick_programs.append(program_name)
            # Ограничиваем количество программ
            if len(self.quick_programs) > self.max_quick_programs:
                self.quick_programs = self.quick_programs[-self.max_quick_programs:]
            self.save_quick_launch()
    
    def remove_from_quick_launch(self, program_name: str):
        """Удаление программы из быстрого запуска"""
        if program_name in self.quick_programs:
            self.quick_programs.remove(program_name)
            self.save_quick_launch()
    
    def get_toolbar_buttons(self) -> List[Dict[str, Any]]:
        """Получение кнопок для панели инструментов"""
        buttons = []
        
        if self.launcher and hasattr(self.launcher, 'programs'):
            for program_name in self.quick_programs:
                # Ищем программу в списке программ лаунчера
                program = None
                for prog in self.launcher.programs:
                    if prog['name'] == program_name:
                        program = prog
                        break
                
                if program:
                    buttons.append({
                        'text': f"🚀 {program_name}",
                        'command': lambda p=program: self.launch_program(p),
                        'tooltip': f"Быстрый запуск: {program_name}",
                        'icon': "🚀"
                    })
        
        # Кнопка управления быстрым запуском
        buttons.append({
            'text': "⚙️ Управление",
            'command': self.show_quick_launch_manager,
            'tooltip': "Управление быстрым запуском",
            'icon': "⚙️"
        })
        
        return buttons
    
    def launch_program(self, program):
        """Запуск программы"""
        if self.launcher and hasattr(self.launcher, 'launch_program'):
            self.launcher.launch_program(program)
    
    def show_quick_launch_manager(self):
        """Показать окно управления быстрым запуском"""
        if not self.launcher:
            return
        
        # Создаем окно управления
        manager_window = ctk.CTkToplevel(self.launcher.root)
        manager_window.title("Управление быстрым запуском")
        manager_window.geometry("400x500")
        manager_window.resizable(False, False)
        
        # Список программ быстрого запуска
        quick_frame = ctk.CTkFrame(manager_window)
        quick_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            quick_frame,
            text="🚀 Программы быстрого запуска",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Список программ
        for program_name in self.quick_programs:
            program_frame = ctk.CTkFrame(quick_frame)
            program_frame.pack(fill="x", padx=10, pady=5)
            
            name_label = ctk.CTkLabel(
                program_frame,
                text=program_name,
                font=ctk.CTkFont(size=14)
            )
            name_label.pack(side="left", padx=10, pady=5)
            
            remove_button = ctk.CTkButton(
                program_frame,
                text="🗑️",
                width=30,
                command=lambda name=program_name: self.remove_from_quick_launch(name)
            )
            remove_button.pack(side="right", padx=10, pady=5)
        
        # Кнопка добавления
        add_button = ctk.CTkButton(
            quick_frame,
            text="➕ Добавить программу",
            command=self.show_add_program_dialog
        )
        add_button.pack(pady=10)
    
    def show_add_program_dialog(self):
        """Показать диалог добавления программы"""
        if not self.launcher or not hasattr(self.launcher, 'programs'):
            return
        
        # Создаем список программ для выбора
        program_names = [prog['name'] for prog in self.launcher.programs 
                        if prog['name'] not in self.quick_programs]
        
        if not program_names:
            messagebox.showinfo("Информация", "Все программы уже добавлены в быстрый запуск!")
            return
        
        # Простой диалог выбора
        selected = simpledialog.askstring(
            "Добавить в быстрый запуск",
            f"Выберите программу для добавления:\n{', '.join(program_names)}"
        )
        
        if selected and selected in program_names:
            self.add_to_quick_launch(selected)
            messagebox.showinfo("Успех", f"Программа '{selected}' добавлена в быстрый запуск!")
    
    def on_program_launched(self, program: Dict[str, Any]) -> None:
        """При запуске программы добавляем её в быстрый запуск"""
        program_name = program.get('name', '')
        if program_name:
            self.add_to_quick_launch(program_name)
    
    def on_program_added(self, program: Dict[str, Any]) -> None:
        """При добавлении программы ничего не делаем"""
        pass
    
    def on_program_removed(self, program: Dict[str, Any]) -> None:
        """При удалении программы убираем её из быстрого запуска"""
        program_name = program.get('name', '')
        if program_name:
            self.remove_from_quick_launch(program_name) 