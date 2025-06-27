import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import json
import os
import subprocess
import threading
import time
from datetime import datetime
import customtkinter as ctk
from PIL import Image, ImageTk
import re
import webbrowser

# Добавляем импорты для работы с иконками
ICON_SUPPORT = True  # Всегда включена поддержка иконок

# Константы для системы обновлений
CURRENT_VERSION = "1.0.0"
UPDATE_CHECK_URL = "https://api.github.com/repos/milioners/MyLauncher/releases/latest"
GITHUB_RELEASES_URL = "https://github.com/milioners/MyLauncher/releases"

class AddProgramWindow:
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        
        # Создание окна
        self.window = ctk.CTkToplevel(parent)
        self.window.title("➕ Добавить программу")
        self.window.geometry("700x650")
        self.window.resizable(False, False)
        
        # Настройка модального окна
        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_set()
        
        # Центрирование окна
        self.center_window()
        
        # Переменные
        self.program_name = tk.StringVar()
        self.program_path = tk.StringVar()
        self.program_description = tk.StringVar()
        self.program_category = tk.StringVar(value="Общие")
        
        # Создание интерфейса
        self.create_widgets()
        
        # Фокус на первое поле
        self.name_entry.focus()
        
    def center_window(self):
        """Центрирование окна"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Главный контейнер с современным дизайном
        main_container = ctk.CTkFrame(self.window, fg_color="#1a1a1a")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Заголовок
        header_frame = ctk.CTkFrame(main_container, fg_color="#2d2d2d", corner_radius=10)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="➕ Добавить новую программу",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FFD700"
        )
        title_label.pack(pady=20)
        
        # Основная форма
        form_container = ctk.CTkScrollableFrame(main_container, fg_color="#2d2d2d", corner_radius=10)
        form_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Название программы
        name_frame = ctk.CTkFrame(form_container, fg_color="#3d3d3d", corner_radius=8)
        name_frame.pack(fill="x", padx=20, pady=10)
        
        name_label = ctk.CTkLabel(
            name_frame,
            text="📝 Название программы",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF"
        )
        name_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        self.name_entry = ctk.CTkEntry(
            name_frame,
            textvariable=self.program_name,
            placeholder_text="Введите название программы...",
            font=ctk.CTkFont(size=14),
            height=45,
            fg_color="#4d4d4d",
            border_color="#5d5d5d",
            corner_radius=8
        )
        self.name_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        # Путь к программе
        path_frame = ctk.CTkFrame(form_container, fg_color="#3d3d3d", corner_radius=8)
        path_frame.pack(fill="x", padx=20, pady=10)
        
        path_label = ctk.CTkLabel(
            path_frame,
            text="📁 Путь к исполняемому файлу",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF"
        )
        path_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        path_input_frame = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_input_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.path_entry = ctk.CTkEntry(
            path_input_frame,
            textvariable=self.program_path,
            placeholder_text="Выберите .exe файл...",
            font=ctk.CTkFont(size=14),
            height=45,
            fg_color="#4d4d4d",
            border_color="#5d5d5d",
            corner_radius=8
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_button = ctk.CTkButton(
            path_input_frame,
            text="📂 Обзор",
            command=self.browse_file,
            font=ctk.CTkFont(size=12, weight="bold"),
            width=100,
            height=45,
            fg_color="#2196F3",
            hover_color="#1976D2",
            corner_radius=8
        )
        browse_button.pack(side="right")
        
        # Описание программы
        desc_frame = ctk.CTkFrame(form_container, fg_color="#3d3d3d", corner_radius=8)
        desc_frame.pack(fill="x", padx=20, pady=10)
        
        desc_label = ctk.CTkLabel(
            desc_frame,
            text="📄 Описание (необязательно)",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF"
        )
        desc_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        self.desc_textbox = ctk.CTkTextbox(
            desc_frame,
            height=80,
            font=ctk.CTkFont(size=12),
            fg_color="#4d4d4d",
            border_color="#5d5d5d",
            corner_radius=8
        )
        self.desc_textbox.pack(fill="x", padx=20, pady=(0, 15))
        
        # Категория
        category_frame = ctk.CTkFrame(form_container, fg_color="#3d3d3d", corner_radius=8)
        category_frame.pack(fill="x", padx=20, pady=10)
        
        category_label = ctk.CTkLabel(
            category_frame,
            text="🏷️ Категория",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF"
        )
        category_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        categories = ["Общие", "Игры", "Работа", "Мультимедиа", "Интернет", "Утилиты", "Разработка"]
        self.category_menu = ctk.CTkOptionMenu(
            category_frame,
            values=categories,
            variable=self.program_category,
            font=ctk.CTkFont(size=14),
            height=45,
            fg_color="#4d4d4d",
            button_color="#5d5d5d",
            button_hover_color="#6d6d6d",
            corner_radius=8
        )
        self.category_menu.pack(fill="x", padx=20, pady=(0, 15))
        
        # Кнопки внизу окна
        self.create_bottom_buttons(main_container)
        
    def create_bottom_buttons(self, parent):
        """Создание кнопок внизу окна"""
        # Создаем отдельный фрейм для кнопок вне прокручиваемой области
        buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20, side="bottom")
        
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="❌ Отмена",
            command=self.cancel,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            fg_color="#F44336",
            hover_color="#D32F2F",
            corner_radius=22
        )
        cancel_button.pack(side="left", padx=(0, 10), expand=True)
        
        add_button = ctk.CTkButton(
            buttons_frame,
            text="✅ Добавить программу",
            command=self.add_program,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            fg_color="#4CAF50",
            hover_color="#45a049",
            corner_radius=22
        )
        add_button.pack(side="right", padx=(10, 0), expand=True)
        
    def browse_file(self):
        """Выбор файла"""
        file_path = filedialog.askopenfilename(
            title="Выберите исполняемый файл",
            filetypes=[
                ("Исполняемые файлы", "*.exe"),
                ("Все файлы", "*.*")
            ]
        )
        
        if file_path:
            self.program_path.set(file_path)
            # Автоматическое заполнение названия из имени файла
            if not self.program_name.get():
                filename = os.path.splitext(os.path.basename(file_path))[0]
                self.program_name.set(filename)
    
    def add_program(self):
        """Добавление программы"""
        name = self.program_name.get().strip()
        path = self.program_path.get().strip()
        description = self.desc_textbox.get("1.0", "end-1c").strip()
        category = self.program_category.get()
        
        # Валидация
        if not name:
            messagebox.showerror("Ошибка", "Введите название программы!")
            self.name_entry.focus()
            return
            
        if not path:
            messagebox.showerror("Ошибка", "Выберите путь к программе!")
            return
            
        if not os.path.exists(path):
            messagebox.showerror("Ошибка", "Указанный файл не существует!")
            return
        
        # Создание объекта программы
        new_program = {
            'name': name,
            'path': path,
            'description': description,
            'category': category,
            'date_added': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Вызов callback функции
        self.callback(new_program)
        self.window.destroy()
    
    def cancel(self):
        """Отмена добавления"""
        self.window.destroy()

class SettingsWindow:
    def __init__(self, parent, current_settings, callback):
        self.parent = parent
        self.current_settings = current_settings
        self.callback = callback
        
        # Создание окна
        self.window = ctk.CTkToplevel(parent)
        self.window.title("⚙️ Настройки")
        self.window.geometry("750x700")
        self.window.resizable(False, False)
        
        # Настройка модального окна
        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_set()
        
        # Центрирование окна
        self.center_window()
        
        # Переменные настроек
        self.auto_start = tk.BooleanVar(value=current_settings.get('auto_start', False))
        self.minimize_to_tray = tk.BooleanVar(value=current_settings.get('minimize_to_tray', True))
        self.show_notifications = tk.BooleanVar(value=current_settings.get('show_notifications', True))
        self.theme_mode = tk.StringVar(value=current_settings.get('theme_mode', 'dark'))
        self.window_size = tk.StringVar(value=current_settings.get('window_size', '1000x700'))
        
        # Новые настройки персонализации
        self.tile_size = tk.StringVar(value=current_settings.get('tile_size', 'medium'))
        self.color_scheme = tk.StringVar(value=current_settings.get('color_scheme', 'blue'))
        self.columns_count = tk.StringVar(value=current_settings.get('columns_count', '3'))
        self.show_statistics = tk.BooleanVar(value=current_settings.get('show_statistics', True))
        self.track_usage = tk.BooleanVar(value=current_settings.get('track_usage', True))
        
        # Создание интерфейса
        self.create_widgets()
        
        # Привязка событий для применения настроек в реальном времени
        self.theme_mode.trace("w", self.apply_theme)
        self.window_size.trace("w", self.apply_window_size)
        
    def center_window(self):
        """Центрирование окна"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        
    def apply_theme(self, *args):
        """Применение темы в реальном времени"""
        theme = self.theme_mode.get()
        if theme == "system":
            ctk.set_appearance_mode("system")
        else:
            ctk.set_appearance_mode(theme)
        
    def apply_window_size(self, *args):
        """Применение размера окна в реальном времени"""
        size = self.window_size.get()
        if size and "x" in size:
            try:
                width, height = map(int, size.split("x"))
                self.parent.geometry(f"{width}x{height}")
                # Центрирование главного окна
                self.parent.update_idletasks()
                x = (self.parent.winfo_screenwidth() // 2) - (width // 2)
                y = (self.parent.winfo_screenheight() // 2) - (height // 2)
                self.parent.geometry(f"{width}x{height}+{x}+{y}")
            except ValueError:
                pass
    
    def on_size_change(self, choice):
        """Обработчик изменения размера окна"""
        if choice and "x" in choice:
            try:
                width, height = map(int, choice.split("x"))
                self.parent.geometry(f"{width}x{height}")
                # Центрирование главного окна
                self.parent.update_idletasks()
                x = (self.parent.winfo_screenwidth() // 2) - (width // 2)
                y = (self.parent.winfo_screenheight() // 2) - (height // 2)
                self.parent.geometry(f"{width}x{height}+{x}+{y}")
            except ValueError:
                pass
    
    def on_tile_size_change(self, choice):
        """Обработчик изменения размера плиток"""
        # Применяем изменения к главному окну
        if hasattr(self.parent, 'apply_tile_size'):
            self.parent.apply_tile_size(choice)
    
    def on_color_scheme_change(self, choice):
        """Обработчик изменения цветовой схемы"""
        # Применяем изменения к главному окну
        if hasattr(self.parent, 'apply_color_scheme'):
            self.parent.apply_color_scheme(choice)
    
    def on_columns_change(self, choice):
        """Обработчик изменения количества колонок"""
        # Применяем изменения к главному окну
        if hasattr(self.parent, 'apply_columns_count'):
            self.parent.apply_columns_count(int(choice))
    
    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Главный контейнер с современным дизайном
        main_frame = ctk.CTkFrame(self.window, fg_color="#1a1a1a")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Заголовок
        header_frame = ctk.CTkFrame(main_frame, fg_color="#2d2d2d", corner_radius=10)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="⚙️ Настройки приложения",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FFD700"
        )
        title_label.pack(pady=20)
        
        # Создание вкладок
        self.tabview = ctk.CTkTabview(main_frame, fg_color="#2d2d2d", corner_radius=10)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Добавление вкладок
        self.tabview.add("Общие")
        self.tabview.add("Интерфейс")
        self.tabview.add("Персонализация")
        self.tabview.add("Уведомления")
        self.tabview.add("Обновления")
        self.tabview.add("О программе")
        
        # Создание содержимого вкладок
        self.create_general_tab(self.tabview.tab("Общие"))
        self.create_interface_tab(self.tabview.tab("Интерфейс"))
        self.create_personalization_tab(self.tabview.tab("Персонализация"))
        self.create_notifications_tab(self.tabview.tab("Уведомления"))
        self.create_updates_tab(self.tabview.tab("Обновления"))
        self.create_about_tab(self.tabview.tab("О программе"))
        
        # Кнопки внизу окна
        self.create_bottom_buttons(main_frame)
        
    def create_bottom_buttons(self, parent):
        """Создание кнопок внизу окна"""
        buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20, side="bottom")
        
        # Кнопка отмены
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="❌ Отмена",
            command=self.cancel,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            fg_color="#F44336",
            hover_color="#D32F2F",
            corner_radius=22
        )
        cancel_button.pack(side="left", padx=(0, 10), expand=True)
        
        # Кнопка сохранения
        save_button = ctk.CTkButton(
            buttons_frame,
            text="✅ Сохранить настройки",
            command=self.save_settings,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            fg_color="#4CAF50",
            hover_color="#45a049",
            corner_radius=22
        )
        save_button.pack(side="right", padx=(10, 0), expand=True)
        
    def create_general_tab(self, parent):
        """Создание вкладки общих настроек"""
        # Автозапуск
        auto_start_frame = ctk.CTkFrame(parent)
        auto_start_frame.pack(fill="x", padx=20, pady=10)
        
        auto_start_label = ctk.CTkLabel(
            auto_start_frame,
            text="🚀 Автозапуск при старте системы",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        auto_start_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        auto_start_desc = ctk.CTkLabel(
            auto_start_frame,
            text="Лаунчер будет автоматически запускаться при включении компьютера",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        auto_start_desc.pack(anchor="w", padx=20, pady=(0, 15))
        
        auto_start_switch = ctk.CTkSwitch(
            auto_start_frame,
            text="Включить автозапуск",
            variable=self.auto_start,
            font=ctk.CTkFont(size=14)
        )
        auto_start_switch.pack(anchor="w", padx=20, pady=(0, 15))
        
        # Сворачивание в трей
        tray_frame = ctk.CTkFrame(parent)
        tray_frame.pack(fill="x", padx=20, pady=10)
        
        tray_label = ctk.CTkLabel(
            tray_frame,
            text="📱 Сворачивание в системный трей",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        tray_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        tray_desc = ctk.CTkLabel(
            tray_frame,
            text="При закрытии окна лаунчер будет сворачиваться в трей",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        tray_desc.pack(anchor="w", padx=20, pady=(0, 15))
        
        tray_switch = ctk.CTkSwitch(
            tray_frame,
            text="Включить сворачивание в трей",
            variable=self.minimize_to_tray,
            font=ctk.CTkFont(size=14)
        )
        tray_switch.pack(anchor="w", padx=20, pady=(0, 15))
        
    def create_interface_tab(self, parent):
        """Создание вкладки настроек интерфейса"""
        # Тема оформления
        theme_frame = ctk.CTkFrame(parent)
        theme_frame.pack(fill="x", padx=20, pady=10)
        
        theme_label = ctk.CTkLabel(
            theme_frame,
            text="🎨 Тема оформления",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        theme_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        theme_desc = ctk.CTkLabel(
            theme_frame,
            text="Выберите тему оформления интерфейса",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        theme_desc.pack(anchor="w", padx=20, pady=(0, 10))
        
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["dark", "light", "system"],
            variable=self.theme_mode,
            font=ctk.CTkFont(size=14),
            height=40,
            command=self.on_theme_change
        )
        theme_menu.pack(anchor="w", padx=20, pady=(0, 15))
        
        # Размер окна
        size_frame = ctk.CTkFrame(parent)
        size_frame.pack(fill="x", padx=20, pady=10)
        
        size_label = ctk.CTkLabel(
            size_frame,
            text="📐 Размер окна по умолчанию",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        size_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        size_desc = ctk.CTkLabel(
            size_frame,
            text="Выберите размер главного окна лаунчера",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        size_desc.pack(anchor="w", padx=20, pady=(0, 10))
        
        size_menu = ctk.CTkOptionMenu(
            size_frame,
            values=["800x600", "1000x700", "1200x800", "1400x900"],
            variable=self.window_size,
            font=ctk.CTkFont(size=14),
            height=40,
            command=self.on_size_change
        )
        size_menu.pack(anchor="w", padx=20, pady=(0, 15))
        
    def create_personalization_tab(self, parent):
        # Используем прокручиваемый контейнер
        scroll_frame = ctk.CTkScrollableFrame(parent)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Далее все элементы добавляем в scroll_frame, а не в parent
        tile_frame = ctk.CTkFrame(scroll_frame)
        tile_frame.pack(fill="x", padx=20, pady=10)
        
        tile_label = ctk.CTkLabel(
            tile_frame,
            text="📏 Размер плиток программ",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        tile_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        tile_desc = ctk.CTkLabel(
            tile_frame,
            text="Выберите размер плиток для отображения программ",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        tile_desc.pack(anchor="w", padx=20, pady=(0, 10))
        
        tile_menu = ctk.CTkOptionMenu(
            tile_frame,
            values=["small", "medium", "large"],
            variable=self.tile_size,
            font=ctk.CTkFont(size=14),
            height=40,
            command=self.on_tile_size_change
        )
        tile_menu.pack(anchor="w", padx=20, pady=(0, 15))
        
        # Цветовая схема
        color_frame = ctk.CTkFrame(scroll_frame)
        color_frame.pack(fill="x", padx=20, pady=10)
        
        color_label = ctk.CTkLabel(
            color_frame,
            text="🎨 Цветовая схема",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        color_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        color_desc = ctk.CTkLabel(
            color_frame,
            text="Выберите цветовую схему интерфейса",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        color_desc.pack(anchor="w", padx=20, pady=(0, 10))
        
        color_menu = ctk.CTkOptionMenu(
            color_frame,
            values=["blue", "green", "purple", "orange", "red"],
            variable=self.color_scheme,
            font=ctk.CTkFont(size=14),
            height=40,
            command=self.on_color_scheme_change
        )
        color_menu.pack(anchor="w", padx=20, pady=(0, 15))
        
        # Количество колонок
        columns_frame = ctk.CTkFrame(scroll_frame)
        columns_frame.pack(fill="x", padx=20, pady=10)
        
        columns_label = ctk.CTkLabel(
            columns_frame,
            text="📐 Количество колонок",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        columns_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        columns_desc = ctk.CTkLabel(
            columns_frame,
            text="Выберите количество колонок в сетке программ",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        columns_desc.pack(anchor="w", padx=20, pady=(0, 10))
        
        columns_menu = ctk.CTkOptionMenu(
            columns_frame,
            values=["2", "3", "4", "5"],
            variable=self.columns_count,
            font=ctk.CTkFont(size=14),
            height=40,
            command=self.on_columns_change
        )
        columns_menu.pack(anchor="w", padx=20, pady=(0, 15))
        
        # Статистика использования
        stats_frame = ctk.CTkFrame(scroll_frame)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        stats_label = ctk.CTkLabel(
            stats_frame,
            text="📊 Статистика использования",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        stats_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        stats_desc = ctk.CTkLabel(
            stats_frame,
            text="Настройки отслеживания использования программ",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        stats_desc.pack(anchor="w", padx=20, pady=(0, 15))
        
        # Переключатели статистики
        track_switch = ctk.CTkSwitch(
            stats_frame,
            text="Отслеживать использование программ",
            variable=self.track_usage,
            font=ctk.CTkFont(size=14)
        )
        track_switch.pack(anchor="w", padx=20, pady=(0, 10))
        
        show_stats_switch = ctk.CTkSwitch(
            stats_frame,
            text="Показывать статистику в интерфейсе",
            variable=self.show_statistics,
            font=ctk.CTkFont(size=14)
        )
        show_stats_switch.pack(anchor="w", padx=20, pady=(0, 15))
        
    def on_theme_change(self, choice):
        """Обработчик изменения темы"""
        if choice == "system":
            ctk.set_appearance_mode("system")
        else:
            ctk.set_appearance_mode(choice)
    
    def create_notifications_tab(self, parent):
        """Создание вкладки настроек уведомлений"""
        # Уведомления
        notif_frame = ctk.CTkFrame(parent)
        notif_frame.pack(fill="x", padx=20, pady=10)
        
        notif_label = ctk.CTkLabel(
            notif_frame,
            text="🔔 Уведомления",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        notif_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        notif_desc = ctk.CTkLabel(
            notif_frame,
            text="Показывать уведомления о запуске программ и других событиях",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        notif_desc.pack(anchor="w", padx=20, pady=(0, 15))
        
        notif_switch = ctk.CTkSwitch(
            notif_frame,
            text="Включить уведомления",
            variable=self.show_notifications,
            font=ctk.CTkFont(size=14)
        )
        notif_switch.pack(anchor="w", padx=20, pady=(0, 15))
        
    def create_about_tab(self, parent):
        """Создание вкладки о программе"""
        # Информация о программе
        info_frame = ctk.CTkFrame(parent)
        info_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Логотип
        logo_label = ctk.CTkLabel(
            info_frame,
            text="🚀",
            font=ctk.CTkFont(size=48)
        )
        logo_label.pack(pady=(30, 10))
        
        # Название
        name_label = ctk.CTkLabel(
            info_frame,
            text="Современный Лаунчер Программ",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        name_label.pack(pady=(0, 5))
        
        # Версия
        version_label = ctk.CTkLabel(
            info_frame,
            text="Версия 2.0",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        version_label.pack(pady=(0, 20))
        
        # Описание
        desc_text = """
        Современный лаунчер для быстрого запуска программ
        с улучшенным пользовательским интерфейсом.
        
        Возможности:
        • Добавление и управление программами
        • Поиск и фильтрация
        • Современный дизайн
        • Настройки и персонализация
        • Уведомления и автозапуск
        
        Разработано с использованием Python и CustomTkinter
        """
        
        desc_label = ctk.CTkLabel(
            info_frame,
            text=desc_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        desc_label.pack(pady=20)
        
        # Кнопки
        buttons_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        # Кнопки действий
        action_buttons = [
            ("📧 Поддержка", "#4169E1"),
            ("🌐 Веб-сайт", "#2E8B57"),
            ("📖 Документация", "#FF8C00")
        ]
        
        for text, color in action_buttons:
            if text == "📖 Документация":
                btn = ctk.CTkButton(
                    buttons_frame,
                    text=text,
                    font=ctk.CTkFont(size=12),
                    height=35,
                    fg_color=color,
                    hover_color=color,
                    command=lambda: DocumentationWindow(self.window)
                )
            else:
                btn = ctk.CTkButton(
                    buttons_frame,
                    text=text,
                    font=ctk.CTkFont(size=12),
                    height=35,
                    fg_color=color,
                    hover_color=color
                )
            btn.pack(side="left", padx=5, expand=True)
    
    def save_settings(self):
        """Сохранение настроек"""
        settings = {
            'auto_start': self.auto_start.get(),
            'minimize_to_tray': self.minimize_to_tray.get(),
            'show_notifications': self.show_notifications.get(),
            'theme_mode': self.theme_mode.get(),
            'window_size': self.window_size.get(),
            'tile_size': self.tile_size.get(),
            'color_scheme': self.color_scheme.get(),
            'columns_count': self.columns_count.get(),
            'show_statistics': self.show_statistics.get(),
            'track_usage': self.track_usage.get(),
            'check_updates': self.check_updates_var.get()
        }
        
        # Применяем настройки к главному окну
        self.apply_settings_to_main_window(settings)
        
        # Вызываем callback для сохранения
        self.callback(settings)
        
        # Показываем сообщение об успешном сохранении
        messagebox.showinfo(
            "Успех",
            "Настройки успешно сохранены! ✅"
        )
        
        self.window.destroy()
    
    def apply_settings_to_main_window(self, settings):
        """Применение настроек к главному окну"""
        # Применяем тему
        theme = settings.get('theme_mode', 'dark')
        if theme == "system":
            ctk.set_appearance_mode("system")
        else:
            ctk.set_appearance_mode(theme)
        
        # Применяем размер окна
        size = settings.get('window_size', '1000x700')
        if size and "x" in size:
            try:
                width, height = map(int, size.split("x"))
                self.parent.geometry(f"{width}x{height}")
                # Центрирование главного окна
                self.center_window()
            except ValueError:
                pass
    
    def cancel(self):
        """Отмена изменений и закрытие окна"""
        self.window.destroy()
    
    # Автоматический запуск с Windows
    def create_updates_tab(self, parent):
        """Создание вкладки настроек обновлений"""
        # Прокручиваемый контейнер
        scrollable_frame = ctk.CTkScrollableFrame(parent, fg_color="#2d2d2d", corner_radius=10)
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Заголовок
        title_label = ctk.CTkLabel(
            scrollable_frame,
            text="🔄 Настройки обновлений",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FFD700"
        )
        title_label.pack(pady=(0, 20))
        
        # Информация о версии
        version_frame = ctk.CTkFrame(scrollable_frame, fg_color="#3d3d3d", corner_radius=8)
        version_frame.pack(fill="x", padx=20, pady=10)
        
        version_label = ctk.CTkLabel(
            version_frame,
            text=f"Текущая версия: {CURRENT_VERSION}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF"
        )
        version_label.pack(pady=15)
        
        # Настройки обновлений
        updates_frame = ctk.CTkFrame(scrollable_frame, fg_color="#3d3d3d", corner_radius=8)
        updates_frame.pack(fill="x", padx=20, pady=10)
        
        # Автоматическая проверка обновлений
        check_updates_var = tk.BooleanVar(value=self.current_settings.get('check_updates', True))
        
        check_updates_switch = ctk.CTkSwitch(
            updates_frame,
            text="Автоматически проверять обновления при запуске",
            variable=check_updates_var,
            font=ctk.CTkFont(size=14),
            fg_color="#4CAF50",
            progress_color="#45a049"
        )
        check_updates_switch.pack(pady=15, padx=20)
        
        # Кнопка проверки обновлений
        check_button = ctk.CTkButton(
            updates_frame,
            text="🔍 Проверить обновления сейчас",
            command=self.check_updates_now,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="#2196F3",
            hover_color="#1976D2",
            corner_radius=20
        )
        check_button.pack(pady=15, padx=20)
        
        # Сохранение переменной
        self.check_updates_var = check_updates_var
    
    def check_updates_now(self):
        """Проверка обновлений прямо сейчас"""
        # Создаем временный UpdateManager для проверки
        update_manager = UpdateManager(self.window)
        update_manager.check_for_updates(silent=False)

class EditProgramWindow:
    def __init__(self, parent, program, callback):
        self.parent = parent
        self.program = program
        self.callback = callback
        
        # Создание окна
        self.window = ctk.CTkToplevel(parent)
        self.window.title("✏️ Редактировать программу")
        self.window.geometry("700x700")
        self.window.resizable(False, False)
        
        # Настройка модального окна
        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_set()
        
        # Центрирование окна
        self.center_window()
        
        # Переменные
        self.program_name = tk.StringVar(value=program.get('name', ''))
        self.program_path = tk.StringVar(value=program.get('path', ''))
        self.program_description = tk.StringVar(value=program.get('description', ''))
        self.program_category = tk.StringVar(value=program.get('category', 'Общие'))
        
        # Создание интерфейса
        self.create_widgets()
        
        # Фокус на первое поле
        self.name_entry.focus()
        
    def center_window(self):
        """Центрирование окна"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Главный контейнер с современным дизайном
        main_container = ctk.CTkFrame(self.window, fg_color="#1a1a1a")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Заголовок
        header_frame = ctk.CTkFrame(main_container, fg_color="#2d2d2d", corner_radius=10)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="✏️ Редактировать программу",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FFD700"
        )
        title_label.pack(pady=20)
        
        # Основная форма
        form_container = ctk.CTkScrollableFrame(main_container, fg_color="#2d2d2d", corner_radius=10)
        form_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Название программы
        name_frame = ctk.CTkFrame(form_container, fg_color="#3d3d3d", corner_radius=8)
        name_frame.pack(fill="x", padx=20, pady=10)
        
        name_label = ctk.CTkLabel(
            name_frame,
            text="📝 Название программы",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF"
        )
        name_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        self.name_entry = ctk.CTkEntry(
            name_frame,
            textvariable=self.program_name,
            placeholder_text="Введите название программы...",
            font=ctk.CTkFont(size=14),
            height=45,
            fg_color="#4d4d4d",
            border_color="#5d5d5d",
            corner_radius=8
        )
        self.name_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        # Путь к программе
        path_frame = ctk.CTkFrame(form_container, fg_color="#3d3d3d", corner_radius=8)
        path_frame.pack(fill="x", padx=20, pady=10)
        
        path_label = ctk.CTkLabel(
            path_frame,
            text="📁 Путь к исполняемому файлу",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF"
        )
        path_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        path_input_frame = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_input_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.path_entry = ctk.CTkEntry(
            path_input_frame,
            textvariable=self.program_path,
            placeholder_text="Выберите .exe файл...",
            font=ctk.CTkFont(size=14),
            height=45,
            fg_color="#4d4d4d",
            border_color="#5d5d5d",
            corner_radius=8
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_button = ctk.CTkButton(
            path_input_frame,
            text="📂 Обзор",
            command=self.browse_file,
            font=ctk.CTkFont(size=12, weight="bold"),
            width=100,
            height=45,
            fg_color="#2196F3",
            hover_color="#1976D2",
            corner_radius=8
        )
        browse_button.pack(side="right")
        
        # Описание программы
        desc_frame = ctk.CTkFrame(form_container, fg_color="#3d3d3d", corner_radius=8)
        desc_frame.pack(fill="x", padx=20, pady=10)
        
        desc_label = ctk.CTkLabel(
            desc_frame,
            text="📄 Описание (необязательно)",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF"
        )
        desc_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        self.desc_textbox = ctk.CTkTextbox(
            desc_frame,
            height=80,
            font=ctk.CTkFont(size=12),
            fg_color="#4d4d4d",
            border_color="#5d5d5d",
            corner_radius=8
        )
        self.desc_textbox.pack(fill="x", padx=20, pady=(0, 15))
        
        # Вставляем существующее описание
        if self.program.get('description'):
            self.desc_textbox.insert("1.0", self.program.get('description'))
        
        # Категория
        category_frame = ctk.CTkFrame(form_container, fg_color="#3d3d3d", corner_radius=8)
        category_frame.pack(fill="x", padx=20, pady=10)
        
        category_label = ctk.CTkLabel(
            category_frame,
            text="🏷️ Категория",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF"
        )
        category_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        categories = ["Общие", "Игры", "Работа", "Мультимедиа", "Интернет", "Утилиты", "Разработка"]
        self.category_menu = ctk.CTkOptionMenu(
            category_frame,
            values=categories,
            variable=self.program_category,
            font=ctk.CTkFont(size=14),
            height=45,
            fg_color="#4d4d4d",
            button_color="#5d5d5d",
            button_hover_color="#6d6d6d",
            corner_radius=8
        )
        self.category_menu.pack(fill="x", padx=20, pady=(0, 15))
        
        # Кнопки внизу окна
        self.create_bottom_buttons(main_container)
        
    def create_bottom_buttons(self, parent):
        """Создание кнопок внизу окна"""
        # Создаем отдельный фрейм для кнопок вне прокручиваемой области
        buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20, side="bottom")
        
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="❌ Отмена",
            command=self.cancel,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            fg_color="#F44336",
            hover_color="#D32F2F",
            corner_radius=22
        )
        cancel_button.pack(side="left", padx=(0, 10), expand=True)
        
        save_button = ctk.CTkButton(
            buttons_frame,
            text="✅ Сохранить изменения",
            command=self.save_changes,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            fg_color="#4CAF50",
            hover_color="#45a049",
            corner_radius=22
        )
        save_button.pack(side="right", padx=(10, 0), expand=True)
        
    def browse_file(self):
        """Выбор файла"""
        file_path = filedialog.askopenfilename(
            title="Выберите исполняемый файл",
            filetypes=[
                ("Исполняемые файлы", "*.exe"),
                ("Все файлы", "*.*")
            ]
        )
        
        if file_path:
            self.program_path.set(file_path)
            # Автоматическое заполнение названия из имени файла
            if not self.program_name.get():
                filename = os.path.splitext(os.path.basename(file_path))[0]
                self.program_name.set(filename)
    
    def save_changes(self):
        """Сохранение изменений"""
        name = self.program_name.get().strip()
        path = self.program_path.get().strip()
        description = self.desc_textbox.get("1.0", "end-1c").strip()
        category = self.program_category.get()
        
        # Валидация
        if not name:
            messagebox.showerror("Ошибка", "Введите название программы!")
            self.name_entry.focus()
            return
            
        if not path:
            messagebox.showerror("Ошибка", "Выберите путь к программе!")
            return
            
        if not os.path.exists(path):
            messagebox.showerror("Ошибка", "Указанный файл не существует!")
            return
        
        # Обновление объекта программы
        updated_program = {
            'name': name,
            'path': path,
            'description': description,
            'category': category,
            'date_modified': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Сохраняем оригинальные поля, если они есть
        if 'date_added' in self.program:
            updated_program['date_added'] = self.program['date_added']
        
        # Вызов callback функции
        self.callback(updated_program)
        self.window.destroy()
    
    def cancel(self):
        """Отмена изменений"""
        self.window.destroy()

def get_program_icon(path):
    """Получение иконки программы из исполняемого файла"""
    try:
        # Простая реализация - создаем иконку на основе расширения файла
        file_ext = os.path.splitext(path)[1].lower()
        
        # Создаем цветную иконку в зависимости от типа файла
        if file_ext == '.exe':
            color = (70, 130, 180)  # Синий
        elif file_ext == '.msi':
            color = (255, 140, 0)   # Оранжевый
        elif file_ext == '.lnk':
            color = (255, 215, 0)   # Золотой
        else:
            color = (128, 128, 128) # Серый
        
        # Создаем простое изображение
        img = Image.new('RGBA', (32, 32), color + (255,))
        
        # Добавляем простой узор
        for i in range(8, 24):
            for j in range(8, 24):
                if (i + j) % 2 == 0:
                    img.putpixel((i, j), (255, 255, 255, 100))
        
        return ImageTk.PhotoImage(img)
            
    except Exception as e:
        print(f"Ошибка при создании иконки для {path}: {e}")
        return None
    
    return None

def create_default_icon():
    """Создание стандартной иконки"""
    try:
        # Создаем простую иконку
        img = Image.new('RGBA', (32, 32), (70, 130, 180, 255))
        return ImageTk.PhotoImage(img)
    except:
        return None

class ModernProgramLauncher:
    def __init__(self):
        # Загрузка настроек перед настройкой темы
        self.settings_file = "settings.json"
        self.settings = self.load_settings()
        
        # Настройка темы из сохраненных настроек
        theme_mode = self.settings.get('theme_mode', 'dark')
        if theme_mode == "system":
            ctk.set_appearance_mode("system")
        else:
            ctk.set_appearance_mode(theme_mode)
        ctk.set_default_color_theme("blue")
        
        # Создание главного окна
        self.root = ctk.CTk()
        self.root.title("🚀 Современный Лаунчер Программ")
        
        # Применение размера окна из настроек
        window_size = self.settings.get('window_size', '1000x700')
        self.root.geometry(window_size)
        self.root.resizable(True, True)
        
        # Центрирование окна
        self.center_window()
        
        # Файлы для хранения данных
        self.programs_file = "programs.json"
        self.programs = self.load_programs()
        
        # Система отслеживания использования
        self.usage_file = "usage_stats.json"
        self.usage_stats = self.load_usage_stats()
        self.active_programs = {}  # Словарь для отслеживания активных программ
        
        # Переменные для поиска
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_programs)
        
        # Создание интерфейса
        self.create_widgets()
        
        # Запуск анимации загрузки
        self.loading_animation()
        
        # Запуск фонового отслеживания использования
        if self.settings.get('track_usage', True):
            self.start_usage_tracking()
        
        # Инициализация системы обновлений
        self.update_manager = UpdateManager(self.root)
        
        # Проверка обновлений при запуске (тихая проверка)
        if self.settings.get('check_updates', True):
            self.update_manager.check_for_updates(silent=True)
    
    def center_window(self):
        """Центрирование окна на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def loading_animation(self):
        """Анимация загрузки"""
        def animate():
            dots = ["", ".", "..", "..."]
            for i in range(4):
                self.root.title(f"🚀 Современный Лаунчер Программ {dots[i]}")
                time.sleep(0.2)
            self.root.title("🚀 Современный Лаунчер Программ")
        
        threading.Thread(target=animate, daemon=True).start()
        
    def load_programs(self):
        """Загрузка списка программ из файла"""
        if os.path.exists(self.programs_file):
            try:
                with open(self.programs_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_programs(self):
        """Сохранение списка программ в файл"""
        with open(self.programs_file, 'w', encoding='utf-8') as f:
            json.dump(self.programs, f, ensure_ascii=False, indent=2)
    
    def load_settings(self):
        """Загрузка настроек"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.get_default_settings()
        return self.get_default_settings()
    
    def save_settings(self, settings):
        """Сохранение настроек"""
        self.settings = settings
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        
        # Применяем новые настройки к главному окну
        self.apply_settings(settings)
    
    def apply_settings(self, settings):
        """Применение настроек к главному окну"""
        # Применяем тему
        theme = settings.get('theme_mode', 'dark')
        if theme == "system":
            ctk.set_appearance_mode("system")
        else:
            ctk.set_appearance_mode(theme)
        
        # Применяем размер окна
        size = settings.get('window_size', '1000x700')
        if size and "x" in size:
            try:
                width, height = map(int, size.split("x"))
                self.root.geometry(f"{width}x{height}")
                # Центрирование главного окна
                self.center_window()
            except ValueError:
                pass
    
    def get_default_settings(self):
        """Получение настроек по умолчанию"""
        return {
            'auto_start': False,
            'minimize_to_tray': True,
            'show_notifications': True,
            'theme_mode': 'dark',
            'window_size': '1000x700',
            'check_updates': True
        }
    
    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Главный контейнер с градиентным эффектом
        main_container = ctk.CTkFrame(self.root, fg_color="#1a1a1a", corner_radius=0)
        main_container.pack(fill="both", expand=True)
        
        # Верхняя панель с заголовком и поиском
        self.create_modern_header(main_container)
        
        # Основная область с программами
        self.create_modern_programs_area(main_container)
        
        # Нижняя панель с кнопками управления
        self.create_modern_footer(main_container)
        
        # Обновление списка программ
        self.update_program_cards()
        
    def create_modern_header(self, parent):
        """Создание современной верхней панели"""
        # Верхняя панель с градиентом
        header_frame = ctk.CTkFrame(parent, fg_color="#2d2d2d", corner_radius=0, height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Контейнер для содержимого заголовка
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=30, pady=15)
        
        # Левая часть - логотип и название
        left_section = ctk.CTkFrame(header_content, fg_color="transparent")
        left_section.pack(side="left", fill="y")
        
        # Логотип и название
        logo_frame = ctk.CTkFrame(left_section, fg_color="transparent")
        logo_frame.pack(side="left")
        
        logo_label = ctk.CTkLabel(
            logo_frame,
            text="🚀",
            font=ctk.CTkFont(size=32),
            text_color="#FFD700"
        )
        logo_label.pack(side="left", padx=(0, 10))
        
        title_label = ctk.CTkLabel(
            logo_frame,
            text="Cursor Launcher",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FFFFFF"
        )
        title_label.pack(side="left")
        
        # Центральная часть - поиск
        center_section = ctk.CTkFrame(header_content, fg_color="transparent")
        center_section.pack(side="left", fill="x", expand=True, padx=30)
        
        # Поле поиска с иконкой
        search_frame = ctk.CTkFrame(center_section, fg_color="#3d3d3d", corner_radius=25, height=45)
        search_frame.pack(fill="x", padx=20)
        search_frame.pack_propagate(False)
        
        search_icon = ctk.CTkLabel(
            search_frame,
            text="🔍",
            font=ctk.CTkFont(size=16),
            text_color="#888888"
        )
        search_icon.pack(side="left", padx=(15, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Поиск программ...",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            border_width=0,
            height=45
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 15))
        self.search_entry.bind('<KeyRelease>', self.filter_programs)
        
        # Правая часть - кнопки и статистика
        right_section = ctk.CTkFrame(header_content, fg_color="transparent")
        right_section.pack(side="right", fill="y")
        
        # Кнопка добавления программы
        add_button = ctk.CTkButton(
            right_section,
            text="➕ Добавить",
            command=self.show_add_program_window,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            width=120,
            fg_color="#4CAF50",
            hover_color="#45a049",
            corner_radius=22
        )
        add_button.pack(side="right", padx=(10, 0))
        
        # Статистика
        self.stats_label = ctk.CTkLabel(
            right_section,
            text="📊 0 программ",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#87CEEB"
        )
        self.stats_label.pack(side="right", padx=10)
    
    def create_modern_programs_area(self, parent):
        """Создание современной области с программами"""
        # Основной контейнер с прокруткой
        programs_container = ctk.CTkScrollableFrame(
            parent, 
            fg_color="#1a1a1a",
            corner_radius=0
        )
        programs_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Сетка для плиток программ
        self.programs_grid = ctk.CTkFrame(programs_container, fg_color="transparent")
        self.programs_grid.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Настройка весов колонок для равномерного распределения
        self.programs_grid.grid_columnconfigure(0, weight=1)
        self.programs_grid.grid_columnconfigure(1, weight=1)
        self.programs_grid.grid_columnconfigure(2, weight=1)
        
    def create_modern_footer(self, parent):
        """Создание современной нижней панели"""
        # Нижняя панель
        footer_frame = ctk.CTkFrame(parent, fg_color="#2d2d2d", corner_radius=0, height=60)
        footer_frame.pack(fill="x", side="bottom", padx=0, pady=0)
        footer_frame.pack_propagate(False)
        
        # Контейнер для содержимого футера
        footer_content = ctk.CTkFrame(footer_frame, fg_color="transparent")
        footer_content.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Левая часть - информация о системе
        left_footer = ctk.CTkFrame(footer_content, fg_color="transparent")
        left_footer.pack(side="left", fill="y")
        
        system_info = ctk.CTkLabel(
            left_footer,
            text="💻 Windows 10/11 • Python 3.8+",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        system_info.pack(side="left")
        
        # Правая часть - кнопки управления
        right_footer = ctk.CTkFrame(footer_content, fg_color="transparent")
        right_footer.pack(side="right", fill="y")
        
        # Кнопка статистики
        stats_button = ctk.CTkButton(
            right_footer,
            text="📊 Статистика",
            command=self.show_statistics_window,
            font=ctk.CTkFont(size=12, weight="bold"),
            height=35,
            width=100,
            fg_color="#2196F3",
            hover_color="#1976D2",
            corner_radius=17
        )
        stats_button.pack(side="right", padx=5)
        
        # Кнопка обновлений
        update_button = ctk.CTkButton(
            right_footer,
            text="🔄 Обновления",
            command=self.show_update_info,
            font=ctk.CTkFont(size=12, weight="bold"),
            height=35,
            width=100,
            fg_color="#FF9800",
            hover_color="#F57C00",
            corner_radius=17
        )
        update_button.pack(side="right", padx=5)
        
        # Кнопка настроек
        settings_button = ctk.CTkButton(
            right_footer,
            text="⚙️ Настройки",
            command=self.show_settings_window,
            font=ctk.CTkFont(size=12, weight="bold"),
            height=35,
            width=100,
            fg_color="#9C27B0",
            hover_color="#7B1FA2",
            corner_radius=17
        )
        settings_button.pack(side="right", padx=5)
    
    def show_add_program_window(self):
        """Показать окно добавления программы"""
        AddProgramWindow(self.root, self.add_program_callback)
    
    def add_program_callback(self, new_program):
        """Callback для добавления программы"""
        # Проверка на дубликаты
        if any(p['name'] == new_program['name'] for p in self.programs):
            messagebox.showerror(
                "Ошибка",
                "Программа с таким названием уже существует!"
            )
            return
        
        self.programs.append(new_program)
        self.save_programs()
        self.update_program_cards()
        
        if self.settings.get('show_notifications', True):
            messagebox.showinfo(
                "Успех",
                f"Программа '{new_program['name']}' успешно добавлена! 🎉"
            )
    
    def show_statistics_window(self):
        """Показать окно статистики"""
        StatisticsWindow(self.root, self.programs, self.usage_stats, self.active_programs)
        
    def show_settings_window(self):
        """Показать окно настроек"""
        SettingsWindow(self.root, self.settings, self.save_settings)
    
    def filter_programs(self, event=None):
        """Фильтрация программ по поисковому запросу"""
        self.update_program_cards()
        
    def get_filtered_programs(self):
        """Получение отфильтрованных программ"""
        search_term = self.search_var.get().lower()
        if not search_term:
            return self.programs
        
        filtered_programs = [
            prog for prog in self.programs 
            if search_term in prog['name'].lower() or search_term in prog['path'].lower()
        ]
        
        return filtered_programs

    def update_program_cards(self):
        """Обновление плиток программ"""
        # Очищаем существующие плитки
        for widget in self.programs_grid.winfo_children():
            widget.destroy()
        
        # Получаем отфильтрованные программы
        filtered_programs = self.get_filtered_programs()
        
        if not filtered_programs:
            # Показываем сообщение об отсутствии программ
            no_programs_label = ctk.CTkLabel(
                self.programs_grid,
                text="🔍 Программы не найдены\nПопробуйте изменить поисковый запрос",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color="#888888"
            )
            no_programs_label.grid(row=0, column=0, columnspan=3, pady=50)
            return
        
        # Настройка сетки
        columns = int(self.settings.get('columns_count', 3))
        
        # Настраиваем колонки сетки
        for i in range(columns):
            self.programs_grid.grid_columnconfigure(i, weight=1)
        
        # Создаем плитки программ
        for i, program in enumerate(filtered_programs):
            row = i // columns
            col = i % columns
            self.create_program_tile(program, row, col)
        
        print(f"Обновлено плиток программ: {len(filtered_programs)}")
        
        # Запускаем анимацию результатов поиска
        if self.search_var.get().strip():
            self.animate_search_results()
    
    def create_program_tile(self, program, row, col):
        """Создание плитки программы"""
        # Создание фрейма плитки
        tile_frame = ctk.CTkFrame(
            self.programs_grid,
            fg_color="#2d2d2d",
            corner_radius=15,
            border_width=2,
            border_color="#404040"
        )
        tile_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Анимация появления плитки
        self.animate_tile_appearance(tile_frame, delay=row + col)
        
        # Контейнер для содержимого
        content_frame = ctk.CTkFrame(tile_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Иконка программы
        icon_label = ctk.CTkLabel(
            content_frame,
            text=self.get_program_icon(program),
            font=ctk.CTkFont(size=48),
            text_color="#FFD700"
        )
        icon_label.pack(pady=(0, 10))
        
        # Название программы
        name_label = ctk.CTkLabel(
            content_frame,
            text=program['name'],
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF",
            wraplength=150
        )
        name_label.pack(pady=(0, 5))
        
        # Категория
        category_label = ctk.CTkLabel(
            content_frame,
            text=f"📁 {program.get('category', 'Без категории')}",
            font=ctk.CTkFont(size=12),
            text_color="#87CEEB"
        )
        category_label.pack(pady=(0, 15))
        
        # Кнопки управления
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        # Кнопка запуска
        launch_button = ctk.CTkButton(
            buttons_frame,
            text="🚀 Запустить",
            command=lambda: self.launch_program_with_animation(program, tile_frame),
            font=ctk.CTkFont(size=12, weight="bold"),
            height=35,
            fg_color="#4CAF50",
            hover_color="#45a049",
            corner_radius=10
        )
        launch_button.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # Кнопка редактирования
        edit_button = ctk.CTkButton(
            buttons_frame,
            text="✏️",
            command=lambda: EditProgramWindow(self.root, program, lambda updated_prog: self.update_program_callback(updated_prog, self.programs.index(program))),
            font=ctk.CTkFont(size=12, weight="bold"),
            width=35,
            height=35,
            fg_color="#2196F3",
            hover_color="#1976D2",
            corner_radius=10
        )
        edit_button.pack(side="right", padx=(5, 0))
        
        # Кнопка удаления
        delete_button = ctk.CTkButton(
            buttons_frame,
            text="🗑️",
            command=lambda: self.delete_program(program),
            font=ctk.CTkFont(size=12, weight="bold"),
            width=35,
            height=35,
            fg_color="#F44336",
            hover_color="#D32F2F",
            corner_radius=10
        )
        delete_button.pack(side="right")
        
        # Добавляем эффект наведения
        def on_enter(event):
            # Проверяем, что событие пришло от плитки или её содержимого
            widget = event.widget
            while widget and widget != tile_frame:
                widget = widget.master
            if widget == tile_frame:
                tile_frame.configure(border_color="#FFD700", fg_color="#3d3d3d")
        
        def on_leave(event):
            # Проверяем, что курсор действительно покинул плитку
            x, y = event.widget.winfo_pointerxy()
            widget_under_cursor = event.widget.winfo_containing(x, y)
            
            # Проверяем, находится ли курсор над плиткой или её содержимым
            is_over_tile = False
            while widget_under_cursor:
                if widget_under_cursor == tile_frame:
                    is_over_tile = True
                    break
                widget_under_cursor = widget_under_cursor.master
            
            if not is_over_tile:
                tile_frame.configure(border_color="#404040", fg_color="#2d2d2d")
        
        # Привязываем события ко всем дочерним элементам
        tile_frame.bind("<Enter>", on_enter)
        tile_frame.bind("<Leave>", on_leave)
        
        # Также привязываем к содержимому
        content_frame.bind("<Enter>", on_enter)
        content_frame.bind("<Leave>", on_leave)
        
        return tile_frame
    
    def launch_program_with_animation(self, program, tile_frame):
        """Запуск программы с анимацией"""
        # Запускаем анимацию
        self.animate_program_launch(tile_frame)
        
        # Запускаем программу
        self.launch_program(program)
    
    def edit_program(self, program):
        """Редактирование программы через меню"""
        if not self.programs:
            messagebox.showwarning("Предупреждение", "Список программ пуст! 📭")
            return
        
        # Создание списка названий программ
        program_names = [p['name'] for p in self.programs]
        
        # Диалог выбора программы для редактирования
        selected = simpledialog.askstring(
            "Редактирование программы",
            f"Введите название программы для редактирования:\n{', '.join(program_names)}"
        )
        
        if selected:
            # Поиск программы
            for i, p in enumerate(self.programs):
                if p['name'] == selected:
                    EditProgramWindow(self.root, program, lambda updated_prog: self.update_program_callback(updated_prog, i))
                    return
            
            messagebox.showerror("Ошибка", f"Программа '{selected}' не найдена! ❌")
    
    def launch_program(self, program):
        """Запуск программы"""
        try:
            # Проверка существования файла
            if not os.path.exists(program['path']):
                messagebox.showerror(
                    "Ошибка",
                    f"Файл '{program['path']}' не найден! ❌"
                )
                return
            
            # Запуск программы
            subprocess.Popen([program['path']])
            
            # Записываем статистику использования
            if self.settings.get('track_usage', True):
                self.record_program_launch(program)
            
            if self.settings.get('show_notifications', True):
                messagebox.showinfo(
                    "Успех",
                    f"Программа '{program['name']}' запущена! 🚀"
                )
            
        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                f"Не удалось запустить программу: {str(e)} ❌"
            )
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

    def get_program_icon(self, program):
        """Получение иконки программы"""
        # Определяем иконку по расширению файла
        path = program.get('path', '')
        if not path:
            return "⚡"
        
        # Получаем расширение файла
        _, ext = os.path.splitext(path.lower())
        
        # Словарь иконок по расширениям
        icon_map = {
            '.exe': '⚡',
            '.msi': '📦',
            '.lnk': '🔗',
            '.bat': '🖥️',
            '.cmd': '🖥️',
            '.ps1': '💻',
            '.py': '🐍',
            '.js': '📜',
            '.html': '🌐',
            '.txt': '📄',
            '.doc': '📝',
            '.docx': '📝',
            '.pdf': '📕',
            '.jpg': '🖼️',
            '.jpeg': '🖼️',
            '.png': '🖼️',
            '.gif': '🖼️',
            '.mp3': '🎵',
            '.mp4': '🎬',
            '.avi': '🎬',
            '.mkv': '🎬',
            '.zip': '📦',
            '.rar': '📦',
            '.7z': '📦',
            '.iso': '💿'
        }
        
        # Возвращаем иконку или значок по умолчанию
        return icon_map.get(ext, '📄')
    
    def delete_program(self, program):
        """Удаление программы"""
        # Подтверждение удаления
        confirm = messagebox.askyesno(
            "Подтверждение",
            f"Вы уверены, что хотите удалить программу '{program['name']}'?"
        )
        
        if confirm:
            # Находим и удаляем программу
            for i, p in enumerate(self.programs):
                if p['name'] == program['name'] and p['path'] == program['path']:
                    del self.programs[i]
                    self.save_programs()
                    self.update_program_cards()
                    
                    if self.settings.get('show_notifications', True):
                        messagebox.showinfo(
                            "Успех",
                            f"Программа '{program['name']}' удалена! 🗑️"
                        )
                    return
            
            messagebox.showerror("Ошибка", f"Программа '{program['name']}' не найдена!")
    
    def update_program_callback(self, updated_program, index):
        """Callback для обновления программы"""
        # Проверка на дубликаты (кроме текущей программы)
        for i, p in enumerate(self.programs):
            if i != index and p['name'] == updated_program['name']:
                messagebox.showerror(
                    "Ошибка",
                    "Программа с таким названием уже существует!"
                )
                return
        
        # Обновляем программу
        self.programs[index] = updated_program
        self.save_programs()
        self.update_program_cards()
        
        if self.settings.get('show_notifications', True):
            messagebox.showinfo(
                "Успех",
                f"Программа '{updated_program['name']}' обновлена! ✏️"
            )
    
    def load_usage_stats(self):
        """Загрузка статистики использования"""
        if os.path.exists(self.usage_file):
            try:
                with open(self.usage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.get_default_usage_stats()
        return self.get_default_usage_stats()
    
    def save_usage_stats(self):
        """Сохранение статистики использования"""
        with open(self.usage_file, 'w', encoding='utf-8') as f:
            json.dump(self.usage_stats, f, ensure_ascii=False, indent=2)
    
    def get_default_usage_stats(self):
        """Получение статистики по умолчанию"""
        return {
            'programs': {},
            'total_launches': 0,
            'total_time': 0,
            'last_used': None,
            'daily_stats': {},
            'weekly_stats': {}
        }
    
    def start_usage_tracking(self):
        """Запуск отслеживания использования"""
        def track_usage():
            while True:
                try:
                    # Проверяем активные программы каждые 30 секунд
                    time.sleep(30)
                    self.update_usage_stats()
                except Exception as e:
                    print(f"Ошибка в отслеживании использования: {e}")
        
        # Запускаем в отдельном потоке
        tracking_thread = threading.Thread(target=track_usage, daemon=True)
        tracking_thread.start()
    
    def update_usage_stats(self):
        """Обновление статистики использования"""
        current_time = time.time()
        today = time.strftime("%Y-%m-%d")
        
        # Обновляем время для активных программ
        for program_name, start_time in self.active_programs.items():
            if program_name in self.usage_stats['programs']:
                elapsed_time = current_time - start_time
                self.usage_stats['programs'][program_name]['total_time'] += elapsed_time
                self.active_programs[program_name] = current_time
        
        # Обновляем дневную статистику
        if today not in self.usage_stats['daily_stats']:
            self.usage_stats['daily_stats'][today] = {
                'launches': 0,
                'total_time': 0,
                'programs_used': []
            }
        
        # Сохраняем статистику
        self.save_usage_stats()
    
    def record_program_launch(self, program):
        """Запись запуска программы"""
        program_name = program['name']
        current_time = time.time()
        today = time.strftime("%Y-%m-%d")
        
        # Инициализируем статистику программы, если её нет
        if program_name not in self.usage_stats['programs']:
            self.usage_stats['programs'][program_name] = {
                'launches': 0,
                'total_time': 0,
                'last_used': None,
                'first_used': None
            }
        
        # Обновляем статистику
        self.usage_stats['programs'][program_name]['launches'] += 1
        self.usage_stats['programs'][program_name]['last_used'] = current_time
        
        if not self.usage_stats['programs'][program_name]['first_used']:
            self.usage_stats['programs'][program_name]['first_used'] = current_time
        
        # Обновляем общую статистику
        self.usage_stats['total_launches'] += 1
        self.usage_stats['last_used'] = current_time
        
        # Обновляем дневную статистику
        if today not in self.usage_stats['daily_stats']:
            self.usage_stats['daily_stats'][today] = {
                'launches': 0,
                'total_time': 0,
                'programs_used': []
            }
        
        self.usage_stats['daily_stats'][today]['launches'] += 1
        # Добавляем только если такого имени ещё нет
        if program_name not in self.usage_stats['daily_stats'][today]['programs_used']:
            self.usage_stats['daily_stats'][today]['programs_used'].append(program_name)
        
        # Отмечаем программу как активную
        self.active_programs[program_name] = current_time
        
        # Сохраняем статистику
        self.save_usage_stats()
    
    def stop_program_tracking(self, program_name):
        """Остановка отслеживания программы"""
        if program_name in self.active_programs:
            start_time = self.active_programs[program_name]
            elapsed_time = time.time() - start_time
            
            # Обновляем время использования
            if program_name in self.usage_stats['programs']:
                self.usage_stats['programs'][program_name]['total_time'] += elapsed_time
            
            # Удаляем из активных
            del self.active_programs[program_name]
            
            # Сохраняем статистику
            self.save_usage_stats()

    def get_program_icon_pil(self, path):
        """Получение иконки программы в формате PIL Image"""
        try:
            # Простая реализация - создаем иконку на основе расширения файла
            file_ext = os.path.splitext(path)[1].lower()
            
            # Создаем цветную иконку в зависимости от типа файла
            if file_ext == '.exe':
                color = (70, 130, 180)  # Синий
            elif file_ext == '.msi':
                color = (255, 140, 0)   # Оранжевый
            elif file_ext == '.lnk':
                color = (255, 215, 0)   # Золотой
            else:
                color = (128, 128, 128) # Серый
            
            # Создаем простое изображение
            img = Image.new('RGBA', (32, 32), color + (255,))
            
            # Добавляем простой узор
            for i in range(8, 24):
                for j in range(8, 24):
                    if (i + j) % 2 == 0:
                        img.putpixel((i, j), (255, 255, 255, 100))
            
            return img
                
        except Exception as e:
            print(f"Ошибка при создании иконки для {path}: {e}")
            return None
        
        return None

    def animate_tile_appearance(self, tile_frame, delay=0):
        """Анимация появления плитки"""
        # Начинаем с прозрачности 0
        tile_frame.configure(fg_color="#1a1a1a")
        
        # Счетчик для анимации
        self.tile_animation_step = 0
        
        def animate_step():
            if self.tile_animation_step < 10:
                alpha = self.tile_animation_step / 10.0
                color = f"#{int(45 * alpha):02x}{int(45 * alpha):02x}{int(45 * alpha):02x}"
                tile_frame.configure(fg_color=color)
                self.tile_animation_step += 1
                self.root.after(20, animate_step)
            else:
                # Финальный цвет
                tile_frame.configure(fg_color="#2d2d2d")
        
        # Запускаем анимацию с задержкой
        self.root.after(delay * 100, animate_step)
    
    def animate_button_hover(self, button, original_color, hover_color):
        """Анимация наведения на кнопку"""
        def animate_hover():
            # Плавное изменение цвета
            for i in range(10):
                alpha = i / 10.0
                # Интерполяция между цветами
                r1, g1, b1 = int(original_color[1:3], 16), int(original_color[3:5], 16), int(original_color[5:7], 16)
                r2, g2, b2 = int(hover_color[1:3], 16), int(hover_color[3:5], 16), int(hover_color[5:7], 16)
                
                r = int(r1 + (r2 - r1) * alpha)
                g = int(g1 + (g2 - g1) * alpha)
                b = int(b1 + (b2 - b1) * alpha)
                
                color = f"#{r:02x}{g:02x}{b:02x}"
                button.configure(fg_color=color)
                time.sleep(0.01)
        
        animation_thread = threading.Thread(target=animate_hover, daemon=True)
        animation_thread.start()
    
    def animate_program_launch(self, tile_frame):
        """Анимация запуска программы"""
        # Сохраняем оригинальный цвет
        original_color = tile_frame.cget("fg_color")
        
        # Счетчик для анимации
        self.launch_animation_step = 0
        
        def animate_step():
            if self.launch_animation_step < 6:
                # Простая анимация цвета - мигание зеленым
                if self.launch_animation_step % 2 == 0:
                    tile_frame.configure(fg_color="#4CAF50")  # Зеленый
                else:
                    tile_frame.configure(fg_color=original_color)  # Оригинальный
                self.launch_animation_step += 1
                self.root.after(150, animate_step)
            else:
                # Возвращаем оригинальный цвет
                tile_frame.configure(fg_color=original_color)
        
        # Запускаем анимацию
        animate_step()
    
    def animate_search_results(self):
        """Анимация результатов поиска"""
        # Получаем все плитки
        tiles = [child for child in self.programs_grid.winfo_children() 
                if isinstance(child, ctk.CTkFrame)]
        
        # Анимация появления с задержкой
        for i, tile in enumerate(tiles):
            self.root.after(i * 50, lambda t=tile, d=i: self.animate_tile_appearance(t, d))

    def check_updates(self):
        """Проверка обновлений"""
        self.update_manager.check_for_updates(silent=False)
    
    def show_update_info(self):
        """Показать информацию об обновлениях"""
        self.update_manager.show_update_info()
    
    def show_update_settings(self):
        """Показать настройки обновлений"""
        # Создаем простое окно настроек обновлений
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("🔄 Настройки обновлений")
        settings_window.geometry("500x400")
        settings_window.resizable(False, False)
        
        # Настройка модального окна
        settings_window.transient(self.root)
        settings_window.grab_set()
        settings_window.focus_set()
        
        # Центрирование окна
        settings_window.update_idletasks()
        width = settings_window.winfo_width()
        height = settings_window.winfo_height()
        x = (settings_window.winfo_screenwidth() // 2) - (width // 2)
        y = (settings_window.winfo_screenheight() // 2) - (height // 2)
        settings_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Главный контейнер
        main_frame = ctk.CTkFrame(settings_window, fg_color="#1a1a1a")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Заголовок
        title_label = ctk.CTkLabel(
            main_frame,
            text="🔄 Настройки обновлений",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FFD700"
        )
        title_label.pack(pady=20)
        
        # Информация о версии
        version_frame = ctk.CTkFrame(main_frame, fg_color="#2d2d2d", corner_radius=10)
        version_frame.pack(fill="x", padx=20, pady=10)
        
        version_label = ctk.CTkLabel(
            version_frame,
            text=f"Текущая версия: {CURRENT_VERSION}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF"
        )
        version_label.pack(pady=15)
        
        # Настройки
        settings_frame = ctk.CTkFrame(main_frame, fg_color="#2d2d2d", corner_radius=10)
        settings_frame.pack(fill="x", padx=20, pady=10)
        
        # Автоматическая проверка обновлений
        auto_check_var = tk.BooleanVar(value=self.settings.get('check_updates', True))
        
        auto_check_switch = ctk.CTkSwitch(
            settings_frame,
            text="Автоматически проверять обновления при запуске",
            variable=auto_check_var,
            font=ctk.CTkFont(size=14),
            fg_color="#4CAF50",
            progress_color="#45a049"
        )
        auto_check_switch.pack(pady=15, padx=20)
        
        # Кнопки
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        check_button = ctk.CTkButton(
            buttons_frame,
            text="🔍 Проверить обновления",
            command=self.check_updates,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="#2196F3",
            hover_color="#1976D2",
            corner_radius=20
        )
        check_button.pack(side="left", padx=(0, 10), expand=True)
        
        save_button = ctk.CTkButton(
            buttons_frame,
            text="💾 Сохранить",
            command=lambda: self.save_update_settings(auto_check_var.get(), settings_window),
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="#4CAF50",
            hover_color="#45a049",
            corner_radius=20
        )
        save_button.pack(side="right", padx=(10, 0), expand=True)
    
    def save_update_settings(self, auto_check, window):
        """Сохранение настроек обновлений"""
        self.settings['check_updates'] = auto_check
        self.save_settings(self.settings)
        
        messagebox.showinfo(
            "✅ Сохранено",
            "Настройки обновлений сохранены!"
        )
        window.destroy()

class DocumentationWindow:
    def __init__(self, parent):
        self.parent = parent
        self.expanded = {}
        self.content_frames = {}
        
        # Создаем окно документации
        self.window = tk.Toplevel(parent)
        self.window.title("📚 Документация - Cursor Launcher")
        self.window.geometry("900x700")
        self.window.configure(bg="#1E1E1E")
        self.window.resizable(True, True)
        
        # Центрируем окно
        self.center_window()
        
        # Создаем главный контейнер с градиентным фоном
        main_container = tk.Frame(self.window, bg="#1E1E1E", relief="flat", bd=0)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Заголовок с красивым оформлением
        title_frame = tk.Frame(main_container, bg="#1E1E1E", relief="flat", bd=0)
        title_frame.pack(fill="x", pady=(0, 20))
        
        # Иконка и заголовок
        title_label = tk.Label(
            title_frame,
            text="📚 ДОКУМЕНТАЦИЯ",
            font=("Segoe UI", 24, "bold"),
            fg="#FFD700",
            bg="#1E1E1E"
        )
        title_label.pack()
        
        # Подзаголовок
        subtitle_label = tk.Label(
            title_frame,
            text="Полное руководство по использованию Cursor Launcher",
            font=("Segoe UI", 12),
            fg="#CCCCCC",
            bg="#1E1E1E"
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Разделитель
        separator = tk.Frame(title_frame, height=2, bg="#FF8C00")
        separator.pack(fill="x", pady=15)
        
        # Создаем прокручиваемую область
        canvas = tk.Canvas(main_container, bg="#1E1E1E", highlightthickness=0, relief="flat")
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1E1E1E", relief="flat", bd=0)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Упаковка элементов прокрутки
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Привязка прокрутки к колесу мыши
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Содержимое документации
        self.sections = {
            "🎯 Управление программами": [
                ("➕ Добавление программ", "① Нажмите кнопку '➕ Добавить программу' в верхней панели\n② Заполните обязательные поля: название и путь к .exe файлу\n③ Добавьте описание и категорию по желанию\n④ Нажмите 'Сохранить' для добавления программы"),
                ("✏️ Редактирование программ", "① На каждой плитке программы есть кнопка '✏️ Изменить'\n② Измените любые параметры программы\n③ Нажмите 'Сохранить' для применения изменений"),
                ("🗑️ Удаление программ", "① На каждой плитке программы есть кнопка '🗑️ Удалить'\n② Подтвердите удаление в диалоговом окне\n③ Программа удаляется только из списка, файл остается на диске"),
                ("▶️ Запуск программ", "① Нажмите кнопку '▶️ Запустить' на плитке программы\n② Статус ✅ показывает, что файл доступен\n③ Статус ❌ показывает, что файл не найден")
            ],
            "🔍 Поиск и фильтрация": [
                ("🔍 Поиск программ", "① Используйте поле '🔍 Поиск программ...' в верхней панели\n② Поиск работает по названию и пути к файлу\n③ Результаты обновляются мгновенно при вводе\n④ Поиск не чувствителен к регистру"),
                ("📊 Фильтрация", "① Автоматическая фильтрация при вводе текста\n② Поддерживается частичное совпадение\n③ Отображаются только подходящие программы\n④ Очистите поле поиска для показа всех программ")
            ],
            "⚙️ Настройки приложения": [
                ("🔧 Общие настройки", "① Нажмите кнопку '⚙️ Настройки' в нижней панели\n② Вкладка 'Общие': автозапуск, язык, размер окна\n③ Вкладка 'Интерфейс': тема, размер плиток\n④ Вкладка 'Уведомления': звуки, всплывающие окна"),
                ("🚀 Автозапуск", "① В настройках включите 'Автозапуск при старте системы'\n② Лаунчер будет автоматически запускаться при включении компьютера\n③ Можно отключить в любой момент через настройки"),
                ("🎨 Внешний вид", "① Выберите тему: темная, светлая или системная\n② Настройте размер окна: 800x600, 1000x700, 1200x800, 1400x900\n③ Изменения применяются мгновенно")
            ],
            "🎨 Интерфейс": [
                ("📱 Верхняя панель", "✦ Заголовок приложения\n✦ Поле поиска программ\n✦ Кнопка добавления программы\n✦ Счетчик количества программ"),
                ("📋 Область программ", "✦ Плитки программ в сетке 3x3\n✦ Каждая плитка содержит:\n  - Иконку программы\n  - Название программы\n  - Категорию (если указана)\n  - Статус доступности\n  - Кнопки управления"),
                ("⚙️ Нижняя панель", "✦ Кнопка настроек\n✦ Информация о версии Windows\n✦ Статистика программ")
            ],
            "🔧 Решение проблем": [
                ("❌ Программа не запускается", "① Проверьте, что файл существует по указанному пути\n② Убедитесь, что у вас есть права на запуск файла\n③ Проверьте, не блокирует ли антивирус\n④ Убедитесь в правильности пути к файлу"),
                ("📋 Плитки не отображаются", "① Проверьте файл 'programs.json' в папке приложения\n② Перезапустите приложение\n③ Убедитесь в правах на чтение файла"),
                ("🔍 Поиск не работает", "① Убедитесь, что введен текст для поиска\n② Проверьте, что программы добавлены в список\n③ Поиск работает по названию и пути к файлу"),
                ("⚙️ Настройки не сохраняются", "① Проверьте файл 'settings.json' в папке приложения\n② Убедитесь в правах на запись в папку\n③ Перезапустите приложение")
            ],
            "💡 Советы и рекомендации": [
                ("📁 Организация программ", "✦ Используйте категории для группировки похожих программ\n✦ Добавляйте описания для лучшего понимания назначения\n✦ Используйте понятные названия программ"),
                ("🔍 Эффективный поиск", "✦ Используйте ключевые слова в названиях программ\n✦ Ищите по категориям\n✦ Поиск работает и по путям к файлам"),
                ("⚡ Производительность", "✦ Рекомендуется не более 50 программ для лучшей производительности\n✦ Размер файлов программ не влияет на скорость работы\n✦ Поиск работает быстро даже при большом количестве программ"),
                ("🛡️ Безопасность", "✦ Приложение проверяет существование файлов при добавлении\n✦ Удаление программы безопасно - файл остается на диске\n✦ Все данные сохраняются в локальных файлах")
            ]
        }
        
        # Создаем разделы документации
        for section_title, subsections in self.sections.items():
            # Контейнер для раздела
            section_container = tk.Frame(scrollable_frame, bg="#2A2A2A", relief="flat", bd=0)
            section_container.pack(fill="x", pady=(0, 15), padx=5)
            
            # Заголовок раздела с градиентным эффектом
            section_header = tk.Frame(section_container, bg="#3A3A3A", relief="flat", bd=0)
            section_header.pack(fill="x", pady=(10, 0), padx=10)
            
            # Кнопка-заголовок раздела
            section_btn = tk.Button(
                section_header,
                text=f"▶ {section_title}",
                font=("Segoe UI", 14, "bold"),
                fg="#FFFFFF",
                bg="#3A3A3A",
                activebackground="#4A4A4A",
                activeforeground="#FFD700",
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda s=section_title, c=section_container, b=None: self.toggle_section(c, b, s)
            )
            section_btn.pack(fill="x", pady=8, padx=15)
            
            # Сохраняем ссылку на кнопку для обновления текста
            section_btn.configure(command=lambda s=section_title, c=section_container, b=section_btn: self.toggle_section(c, b, s))
            
            # Создаем подразделы
            for subsection_title, content in subsections:
                # Контейнер для подраздела
                subsection_container = tk.Frame(section_container, bg="#2A2A2A", relief="flat", bd=0)
                subsection_container.pack(fill="x", pady=(5, 0), padx=15)
                
                # Кнопка подраздела
                subsection_btn = tk.Button(
                    subsection_container,
                    text=f"▶ {subsection_title}",
                    font=("Segoe UI", 12),
                    fg="#E0E0E0",
                    bg="#2A2A2A",
                    activebackground="#3A3A3A",
                    activeforeground="#FFD700",
                    relief="flat",
                    bd=0,
                    cursor="hand2",
                    command=lambda c=subsection_container, b=None, t=subsection_title, cont=content: self.toggle(c, b, cont, t)
                )
                subsection_btn.pack(fill="x", pady=4, padx=10)
                
                # Сохраняем ссылку на кнопку
                subsection_btn.configure(command=lambda c=subsection_container, b=subsection_btn, t=subsection_title, cont=content: self.toggle(c, b, cont, t))
        
        # Кнопка закрытия внизу
        close_frame = tk.Frame(main_container, bg="#1E1E1E", relief="flat", bd=0)
        close_frame.pack(fill="x", pady=(20, 0))
        
        close_btn = tk.Button(
            close_frame,
            text="✖ Закрыть",
            font=("Segoe UI", 12, "bold"),
            fg="#FFFFFF",
            bg="#FF6B6B",
            activebackground="#FF5252",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.window.destroy
        )
        close_btn.pack(pady=10)
        
        # Фокус на окно
        self.window.focus_set()
        self.window.grab_set()  # Модальное окно

    def center_window(self):
        """Центрирование окна"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def toggle_section(self, container, btn, title):
        """Переключение состояния раздела"""
        # Пока что просто заглушка, можно расширить функциональность
        pass

    def toggle(self, container, btn, content, title):
        """Переключение состояния подраздела"""
        if self.expanded.get(btn, False):
            # Сворачиваем
            for widget in container.winfo_children():
                if isinstance(widget, tk.Frame) and widget in self.content_frames:
                    widget.destroy()
                    del self.content_frames[widget]
            btn.configure(text=f"▶ {title}")
            self.expanded[btn] = False
        else:
            # Разворачиваем
            # Создаем контейнер для содержимого
            content_frame = tk.Frame(container, bg="#3A3A3A", relief="flat", bd=0)
            content_frame.pack(fill="x", pady=(3, 0), padx=3)
            self.content_frames[content_frame] = True
            
            # Создаем текстовый виджет
            text_widget = tk.Text(
                content_frame,
                wrap="word",
                font=("Segoe UI", 11),
                bg="#3A3A3A",
                fg="#FFFFFF",
                relief="flat",
                padx=10,
                pady=6,
                spacing1=2,
                spacing2=1,
                spacing3=2,
                selectbackground="#FF8C00",
                selectforeground="#FFFFFF",
                insertbackground="#FFD700",
                state="normal",
                height=0
            )
            text_widget.pack(fill="x", padx=6, pady=4)
            
            # Вставляем содержимое
            text_widget.insert("1.0", content)
            
            # Настраиваем теги
            text_widget.tag_configure("step", foreground="#FFD700", font=("Segoe UI", 11, "bold"))
            text_widget.tag_configure("bullet", foreground="#87CEEB", font=("Segoe UI", 11))
            text_widget.tag_configure("highlight", foreground="#98FB98", font=("Segoe UI", 11, "bold"))
            text_widget.tag_configure("warning", foreground="#FF6B6B", font=("Segoe UI", 11, "bold"))
            
            # Применяем форматирование к тексту
            self.format_text_content(text_widget, content)
            
            # Автоматически подстраиваем высоту текстового виджета
            self.auto_resize_text_widget(text_widget)
            text_widget.configure(state="disabled")
            
            btn.configure(text=f"▼ {title}")
            self.expanded[btn] = True

    def format_text_content(self, text_widget, content):
        """Применение цветового форматирования к тексту"""
        lines = content.split('\n')
        current_line = 1
        
        for line in lines:
            if line.strip():
                if line.startswith("①") or line.startswith("②") or line.startswith("③") or line.startswith("④"):
                    start = f"{current_line}.0"
                    end = f"{current_line}.{len(line)}"
                    text_widget.tag_add("step", start, end)
                elif line.startswith("✦"):
                    start = f"{current_line}.0"
                    end = f"{current_line}.{len(line)}"
                    text_widget.tag_add("bullet", start, end)
                elif "✅" in line or "❌" in line:
                    start = f"{current_line}.0"
                    end = f"{current_line}.{len(line)}"
                    text_widget.tag_add("highlight", start, end)
                elif "проверьте" in line.lower() or "убедитесь" in line.lower():
                    start = f"{current_line}.0"
                    end = f"{current_line}.{len(line)}"
                    text_widget.tag_add("warning", start, end)
            current_line += 1

    def auto_resize_text_widget(self, text_widget):
        """Автоматическая настройка высоты текстового виджета под содержимое"""
        line_count = int(text_widget.index("end-1c").split('.')[0])
        height = min(max(line_count, 3), 15)
        text_widget.configure(height=height)
        
class StatisticsWindow:
    def __init__(self, parent, programs, usage_stats=None, active_programs=None):
        self.parent = parent
        self.programs = programs
        self.usage_stats = usage_stats or {}
        self.active_programs = active_programs or {}
        
        # Создание окна
        self.window = ctk.CTkToplevel(parent)
        self.window.title("📊 Расширенная статистика")
        self.window.geometry("900x700")
        self.window.resizable(False, False)
        
        # Настройка модального окна
        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_set()
        
        # Центрирование окна
        self.center_window()
        
        # Создание интерфейса
        self.create_widgets()
        
    def center_window(self):
        """Центрирование окна"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        
    def format_time(self, seconds):
        """Форматирование времени"""
        if seconds < 60:
            return f"{int(seconds)} сек"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            return f"{minutes} мин"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}ч {minutes}м"
        
    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Главный контейнер
        main_frame = ctk.CTkFrame(self.window, fg_color="#1a1a1a")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Заголовок
        header_frame = ctk.CTkFrame(main_frame, fg_color="#2d2d2d", corner_radius=10)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📊 Расширенная статистика использования",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FFD700"
        )
        title_label.pack(pady=20)
        
        # Основная статистика
        stats_frame = ctk.CTkFrame(main_frame, fg_color="#2d2d2d", corner_radius=10)
        stats_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Прокручиваемая область
        scroll_frame = ctk.CTkScrollableFrame(stats_frame)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Общая статистика
        general_stats = ctk.CTkFrame(scroll_frame, fg_color="#3d3d3d", corner_radius=10)
        general_stats.pack(fill="x", pady=10)
        
        general_title = ctk.CTkLabel(
            general_stats,
            text="📈 Общая статистика",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFFFFF"
        )
        general_title.pack(pady=(15, 10))
        
        # Количество программ
        total_programs = len(self.programs)
        total_label = ctk.CTkLabel(
            general_stats,
            text=f"Всего программ: {total_programs}",
            font=ctk.CTkFont(size=14),
            text_color="#87CEEB"
        )
        total_label.pack(pady=5)
        
        # Доступные программы
        available_programs = sum(1 for p in self.programs if os.path.exists(p['path']))
        available_label = ctk.CTkLabel(
            general_stats,
            text=f"Доступных программ: {available_programs}",
            font=ctk.CTkFont(size=14),
            text_color="#4CAF50"
        )
        available_label.pack(pady=5)
        
        # Недоступные программы
        unavailable_programs = total_programs - available_programs
        unavailable_label = ctk.CTkLabel(
            general_stats,
            text=f"Недоступных программ: {unavailable_programs}",
            font=ctk.CTkFont(size=14),
            text_color="#F44336"
        )
        unavailable_label.pack(pady=5)
        
        # Статистика использования
        if self.usage_stats:
            usage_stats_frame = ctk.CTkFrame(scroll_frame, fg_color="#3d3d3d", corner_radius=10)
            usage_stats_frame.pack(fill="x", pady=10)
            
            usage_title = ctk.CTkLabel(
                usage_stats_frame,
                text="🚀 Статистика использования",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color="#FFFFFF"
            )
            usage_title.pack(pady=(15, 10))
            
            # Общие запуски
            total_launches = self.usage_stats.get('total_launches', 0)
            total_launches_label = ctk.CTkLabel(
                usage_stats_frame,
                text=f"Всего запусков: {total_launches}",
                font=ctk.CTkFont(size=14),
                text_color="#FFD700"
            )
            total_launches_label.pack(pady=5)
            
            # Общее время использования
            total_time = self.usage_stats.get('total_time', 0)
            total_time_label = ctk.CTkLabel(
                usage_stats_frame,
                text=f"Общее время использования: {self.format_time(total_time)}",
                font=ctk.CTkFont(size=14),
                text_color="#FFD700"
            )
            total_time_label.pack(pady=5)
            
            # Активные программы
            active_count = len(self.active_programs)
            active_label = ctk.CTkLabel(
                usage_stats_frame,
                text=f"Сейчас активно: {active_count} программ",
                font=ctk.CTkFont(size=14),
                text_color="#4CAF50"
            )
            active_label.pack(pady=5)
        
        # Топ программ по использованию
        if self.usage_stats and self.usage_stats.get('programs'):
            top_programs_frame = ctk.CTkFrame(scroll_frame, fg_color="#3d3d3d", corner_radius=10)
            top_programs_frame.pack(fill="x", pady=10)
            
            top_title = ctk.CTkLabel(
                top_programs_frame,
                text="🏆 Топ программ по использованию",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color="#FFFFFF"
            )
            top_title.pack(pady=(15, 10))
            
            # Сортируем программы по количеству запусков
            sorted_programs = sorted(
                self.usage_stats['programs'].items(),
                key=lambda x: x[1]['launches'],
                reverse=True
            )[:10]  # Топ 10
            
            for i, (program_name, stats) in enumerate(sorted_programs, 1):
                launches = stats['launches']
                usage_time = self.format_time(stats['total_time'])
                
                program_label = ctk.CTkLabel(
                    top_programs_frame,
                    text=f"{i}. {program_name} - {launches} запусков ({usage_time})",
                    font=ctk.CTkFont(size=12),
                    text_color="#E0E0E0"
                )
                program_label.pack(pady=2, padx=20, anchor="w")
        
        # Статистика по категориям
        categories_stats = ctk.CTkFrame(scroll_frame, fg_color="#3d3d3d", corner_radius=10)
        categories_stats.pack(fill="x", pady=10)
        
        categories_title = ctk.CTkLabel(
            categories_stats,
            text="🏷️ Статистика по категориям",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFFFFF"
        )
        categories_title.pack(pady=(15, 10))
        
        # Подсчет программ по категориям
        categories = {}
        for program in self.programs:
            category = program.get('category', 'Без категории')
            categories[category] = categories.get(category, 0) + 1
        
        for category, count in categories.items():
            category_label = ctk.CTkLabel(
                categories_stats,
                text=f"{category}: {count} программ",
                font=ctk.CTkFont(size=14),
                text_color="#E0E0E0"
            )
            category_label.pack(pady=2)
        
        # Дневная статистика
        if self.usage_stats and self.usage_stats.get('daily_stats'):
            daily_stats_frame = ctk.CTkFrame(scroll_frame, fg_color="#3d3d3d", corner_radius=10)
            daily_stats_frame.pack(fill="x", pady=10)
            
            daily_title = ctk.CTkLabel(
                daily_stats_frame,
                text="📅 Дневная статистика",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color="#FFFFFF"
            )
            daily_title.pack(pady=(15, 10))
            
            # Показываем статистику за последние 7 дней
            today = time.strftime("%Y-%m-%d")
            for i in range(7):
                date = time.strftime("%Y-%m-%d", time.localtime(time.time() - i * 24 * 3600))
                if date in self.usage_stats['daily_stats']:
                    day_stats = self.usage_stats['daily_stats'][date]
                    launches = day_stats['launches']
                    programs_used = len(day_stats['programs_used'])
                    
                    day_label = ctk.CTkLabel(
                        daily_stats_frame,
                        text=f"{date}: {launches} запусков, {programs_used} программ",
                        font=ctk.CTkFont(size=12),
                        text_color="#E0E0E0"
                    )
                    day_label.pack(pady=2, padx=20, anchor="w")
        
        # Кнопка закрытия
        close_button = ctk.CTkButton(
            main_frame,
            text="✖️ Закрыть",
            command=self.window.destroy,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="#F44336",
            hover_color="#D32F2F",
            corner_radius=20
        )
        close_button.pack(pady=20)

    def load_usage_stats(self):
        """Загрузка статистики использования"""
        usage_file = getattr(self, 'usage_file', None)
        if usage_file and os.path.exists(usage_file):
            try:
                with open(usage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Ошибка при загрузке статистики использования: {e}")
                return self.get_default_usage_stats()
        return self.get_default_usage_stats()
    
    def save_usage_stats(self):
        """Сохранение статистики использования"""
        usage_file = getattr(self, 'usage_file', None)
        if usage_file:
            try:
                with open(usage_file, 'w', encoding='utf-8') as f:
                    json.dump(self.usage_stats, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"Ошибка при сохранении статистики использования: {e}")

    def get_default_usage_stats(self):
        """Получение статистики по умолчанию"""
        return {
            'programs': {},
            'total_launches': 0,
            'total_time': 0,
            'last_used': None,
            'daily_stats': {},
            'weekly_stats': {}
        }
    
    def start_usage_tracking(self):
        """Запуск отслеживания использования"""
        def track_usage():
            while True:
                try:
                    # Проверяем активные программы каждые 30 секунд
                    time.sleep(30)
                    self.update_usage_stats()
                except Exception as e:
                    print(f"Ошибка в отслеживании использования: {e}")
        
        # Запускаем в отдельном потоке
        tracking_thread = threading.Thread(target=track_usage, daemon=True)
        tracking_thread.start()
    
    def update_usage_stats(self):
        """Обновление статистики использования"""
        current_time = time.time()
        today = time.strftime("%Y-%m-%d")
        
        # Обновляем время для активных программ
        for program_name, start_time in self.active_programs.items():
            if program_name in self.usage_stats['programs']:
                elapsed_time = current_time - start_time
                self.usage_stats['programs'][program_name]['total_time'] += elapsed_time
                self.active_programs[program_name] = current_time
        
        # Обновляем дневную статистику
        if today not in self.usage_stats['daily_stats']:
            self.usage_stats['daily_stats'][today] = {
                'launches': 0,
                'total_time': 0,
                'programs_used': []
            }
        
        # Сохраняем статистику
        self.save_usage_stats()
    
    def record_program_launch(self, program):
        """Запись запуска программы"""
        program_name = program['name']
        current_time = time.time()
        today = time.strftime("%Y-%m-%d")
        
        # Инициализируем статистику программы, если её нет
        if program_name not in self.usage_stats['programs']:
            self.usage_stats['programs'][program_name] = {
                'launches': 0,
                'total_time': 0,
                'last_used': None,
                'first_used': None
            }
        
        # Обновляем статистику
        self.usage_stats['programs'][program_name]['launches'] += 1
        self.usage_stats['programs'][program_name]['last_used'] = current_time
        
        if not self.usage_stats['programs'][program_name]['first_used']:
            self.usage_stats['programs'][program_name]['first_used'] = current_time
        
        # Обновляем общую статистику
        self.usage_stats['total_launches'] += 1
        self.usage_stats['last_used'] = current_time
        
        # Обновляем дневную статистику
        if today not in self.usage_stats['daily_stats']:
            self.usage_stats['daily_stats'][today] = {
                'launches': 0,
                'total_time': 0,
                'programs_used': []
            }
        
        self.usage_stats['daily_stats'][today]['launches'] += 1
        # Добавляем только если такого имени ещё нет
        if program_name not in self.usage_stats['daily_stats'][today]['programs_used']:
            self.usage_stats['daily_stats'][today]['programs_used'].append(program_name)
        
        # Отмечаем программу как активную
        self.active_programs[program_name] = current_time
        
        # Сохраняем статистику
        self.save_usage_stats()
    
    def stop_program_tracking(self, program_name):
        """Остановка отслеживания программы"""
        if program_name in self.active_programs:
            start_time = self.active_programs[program_name]
            elapsed_time = time.time() - start_time
            
            # Обновляем время использования
            if program_name in self.usage_stats['programs']:
                self.usage_stats['programs'][program_name]['total_time'] += elapsed_time
            
            # Удаляем из активных
            del self.active_programs[program_name]
            
            # Сохраняем статистику
            self.save_usage_stats()

    def get_program_icon_pil(self, path):
        """Получение иконки программы в формате PIL Image"""
        try:
            # Простая реализация - создаем иконку на основе расширения файла
            file_ext = os.path.splitext(path)[1].lower()
            
            # Создаем цветную иконку в зависимости от типа файла
            if file_ext == '.exe':
                color = (70, 130, 180)  # Синий
            elif file_ext == '.msi':
                color = (255, 140, 0)   # Оранжевый
            elif file_ext == '.lnk':
                color = (255, 215, 0)   # Золотой
            else:
                color = (128, 128, 128) # Серый
            
            # Создаем простое изображение
            img = Image.new('RGBA', (32, 32), color + (255,))
            
            # Добавляем простой узор
            for i in range(8, 24):
                for j in range(8, 24):
                    if (i + j) % 2 == 0:
                        img.putpixel((i, j), (255, 255, 255, 100))
            
            return img
                
        except Exception as e:
            print(f"Ошибка при создании иконки для {path}: {e}")
            return None
        
        return None

    def animate_tile_appearance(self, tile_frame, delay=0):
        """Анимация появления плитки"""
        # Начинаем с прозрачности 0
        tile_frame.configure(fg_color="#1a1a1a")
        
        # Счетчик для анимации
        self.tile_animation_step = 0
        
        def animate_step():
            if self.tile_animation_step < 10:
                alpha = self.tile_animation_step / 10.0
                color = f"#{int(45 * alpha):02x}{int(45 * alpha):02x}{int(45 * alpha):02x}"
                tile_frame.configure(fg_color=color)
                self.tile_animation_step += 1
                self.root.after(20, animate_step)
            else:
                # Финальный цвет
                tile_frame.configure(fg_color="#2d2d2d")
        
        # Запускаем анимацию с задержкой
        self.root.after(delay * 100, animate_step)
    
    def animate_button_hover(self, button, original_color, hover_color):
        """Анимация наведения на кнопку"""
        def animate_hover():
            # Плавное изменение цвета
            for i in range(10):
                alpha = i / 10.0
                # Интерполяция между цветами
                r1, g1, b1 = int(original_color[1:3], 16), int(original_color[3:5], 16), int(original_color[5:7], 16)
                r2, g2, b2 = int(hover_color[1:3], 16), int(hover_color[3:5], 16), int(hover_color[5:7], 16)
                
                r = int(r1 + (r2 - r1) * alpha)
                g = int(g1 + (g2 - g1) * alpha)
                b = int(b1 + (b2 - b1) * alpha)
                
                color = f"#{r:02x}{g:02x}{b:02x}"
                button.configure(fg_color=color)
                time.sleep(0.01)
        
        animation_thread = threading.Thread(target=animate_hover, daemon=True)
        animation_thread.start()
    
    def animate_program_launch(self, tile_frame):
        """Анимация запуска программы"""
        # Сохраняем оригинальный цвет
        original_color = tile_frame.cget("fg_color")
        
        # Счетчик для анимации
        self.launch_animation_step = 0
        
        def animate_step():
            if self.launch_animation_step < 6:
                # Простая анимация цвета - мигание зеленым
                if self.launch_animation_step % 2 == 0:
                    tile_frame.configure(fg_color="#4CAF50")  # Зеленый
                else:
                    tile_frame.configure(fg_color=original_color)  # Оригинальный
                self.launch_animation_step += 1
                self.root.after(150, animate_step)
            else:
                # Возвращаем оригинальный цвет
                tile_frame.configure(fg_color=original_color)
        
        # Запускаем анимацию
        animate_step()
    
    def animate_search_results(self):
        """Анимация результатов поиска"""
        # Получаем все плитки
        tiles = [child for child in self.programs_grid.winfo_children() 
                if isinstance(child, ctk.CTkFrame)]
        
        # Анимация появления с задержкой
        for i, tile in enumerate(tiles):
            self.root.after(i * 50, lambda t=tile, d=i: self.animate_tile_appearance(t, d))

class UpdateManager:
    def __init__(self, parent):
        self.parent = parent
        self.latest_version = None
        self.update_available = False
        self.update_info = {}
    
    def check_for_updates(self, silent=False):
        """Проверка наличия обновлений"""
        def check():
            try:
                # В реальном приложении здесь был бы запрос к API
                # Для демонстрации используем заглушку
                self.simulate_update_check()
                
                if self.update_available and not silent:
                    self.show_update_notification()
                    
            except Exception as e:
                if not silent:
                    print(f"Ошибка при проверке обновлений: {e}")
        
        # Запускаем проверку в отдельном потоке
        threading.Thread(target=check, daemon=True).start()
    
    def simulate_update_check(self):
        """Симуляция проверки обновлений (для демонстрации)"""
        # В реальном приложении здесь был бы HTTP запрос
        # Сейчас просто симулируем наличие обновления
        self.latest_version = "1.1.0"
        self.update_available = self.compare_versions(CURRENT_VERSION, self.latest_version) > 0
        
        if self.update_available:
            self.update_info = {
                'version': self.latest_version,
                'title': 'Новая версия Cursor Launcher',
                'description': 'Добавлены новые функции и исправлены ошибки',
                'download_url': GITHUB_RELEASES_URL
            }
    
    def compare_versions(self, current, latest):
        """Сравнение версий"""
        def version_to_tuple(version):
            return tuple(map(int, version.split('.')))
        
        current_tuple = version_to_tuple(current)
        latest_tuple = version_to_tuple(latest)
        
        if latest_tuple > current_tuple:
            return 1
        elif latest_tuple < current_tuple:
            return -1
        else:
            return 0
    
    def show_update_notification(self):
        """Показ уведомления об обновлении"""
        def show():
            result = messagebox.askyesno(
                "🔄 Доступно обновление",
                f"Доступна новая версия {self.latest_version}!\n\n"
                f"Текущая версия: {CURRENT_VERSION}\n"
                f"Новая версия: {self.latest_version}\n\n"
                f"Хотите скачать обновление?",
                icon='info'
            )
            
            if result:
                self.download_update()
        
        # Показываем в главном потоке
        self.parent.after(0, show)
    
    def download_update(self):
        """Скачивание обновления"""
        try:
            # Открываем страницу релизов в браузере
            webbrowser.open(self.update_info['download_url'])
            
            messagebox.showinfo(
                "📥 Скачивание",
                "Страница с обновлением открыта в браузере.\n"
                "Скачайте и установите новую версию вручную."
            )
            
        except Exception as e:
            messagebox.showerror(
                "❌ Ошибка",
                f"Не удалось открыть страницу обновления:\n{str(e)}"
            )
    
    def show_update_info(self):
        """Показать информацию об обновлениях"""
        info_text = f"Текущая версия: {CURRENT_VERSION}\n\n"
        
        if self.update_available:
            info_text += f"🆕 Доступна новая версия: {self.latest_version}\n"
            info_text += f"Описание: {self.update_info.get('description', 'Нет описания')}\n\n"
            info_text += "Нажмите 'Скачать' для получения обновления."
        else:
            info_text += "✅ У вас установлена последняя версия."
        
        result = messagebox.askyesno(
            "ℹ️ Информация об обновлениях",
            info_text + "\n\nПроверить обновления сейчас?"
        )
        
        if result:
            self.check_for_updates(silent=False)

if __name__ == "__main__": 
    app = ModernProgramLauncher()
    app.run() 