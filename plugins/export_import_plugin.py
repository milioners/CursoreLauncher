import os
import json
import csv
from typing import Dict, List, Any
import customtkinter as ctk
from tkinter import messagebox, filedialog
from plugin_system import MenuPluginInterface, EventPluginInterface

class ExportImportPlugin(MenuPluginInterface, EventPluginInterface):
    """Плагин для экспорта и импорта списка программ"""
    
    def __init__(self):
        self.launcher = None
    
    def get_name(self) -> str:
        return "Export/Import"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "Экспорт и импорт списка программ в различных форматах"
    
    def get_author(self) -> str:
        return "Cursor Launcher Team"
    
    def initialize(self, launcher_instance) -> bool:
        self.launcher = launcher_instance
        return True
    
    def cleanup(self) -> bool:
        return True
    
    def get_menu_items(self) -> List[Dict[str, Any]]:
        """Получение пунктов меню"""
        return [
            {
                'parent': 'Файл',
                'text': '📤 Экспорт программ',
                'command': self.show_export_dialog,
                'separator': False
            },
            {
                'parent': 'Файл',
                'text': '📥 Импорт программ',
                'command': self.show_import_dialog,
                'separator': False
            },
            {
                'parent': 'Файл',
                'text': '📋 Резервная копия',
                'command': self.create_backup,
                'separator': True
            }
        ]
    
    def show_export_dialog(self):
        """Показать диалог экспорта"""
        if not self.launcher or not hasattr(self.launcher, 'programs'):
            messagebox.showerror("Ошибка", "Не удалось получить список программ!")
            return
        
        # Создаем окно выбора формата
        export_window = ctk.CTkToplevel(self.launcher.root)
        export_window.title("Экспорт программ")
        export_window.geometry("400x300")
        export_window.resizable(False, False)
        
        # Центрируем окно
        export_window.update_idletasks()
        width = export_window.winfo_width()
        height = export_window.winfo_height()
        x = (export_window.winfo_screenwidth() // 2) - (width // 2)
        y = (export_window.winfo_screenheight() // 2) - (height // 2)
        export_window.geometry(f"{width}x{height}+{x}+{y}")
        
        main_frame = ctk.CTkFrame(export_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="📤 Экспорт программ",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Выбор формата
        format_label = ctk.CTkLabel(
            main_frame,
            text="Выберите формат экспорта:",
            font=ctk.CTkFont(size=14)
        )
        format_label.pack(pady=5)
        
        format_var = ctk.StringVar(value="json")
        
        json_radio = ctk.CTkRadioButton(
            main_frame,
            text="JSON (рекомендуется)",
            variable=format_var,
            value="json"
        )
        json_radio.pack(pady=5)
        
        csv_radio = ctk.CTkRadioButton(
            main_frame,
            text="CSV (для Excel)",
            variable=format_var,
            value="csv"
        )
        csv_radio.pack(pady=5)
        
        txt_radio = ctk.CTkRadioButton(
            main_frame,
            text="TXT (простой список)",
            variable=format_var,
            value="txt"
        )
        txt_radio.pack(pady=5)
        
        # Кнопки
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=20)
        
        export_button = ctk.CTkButton(
            buttons_frame,
            text="📤 Экспортировать",
            command=lambda: self.export_programs(format_var.get(), export_window)
        )
        export_button.pack(side="left", padx=5)
        
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="❌ Отмена",
            command=export_window.destroy
        )
        cancel_button.pack(side="right", padx=5)
    
    def export_programs(self, format_type: str, window):
        """Экспорт программ в выбранном формате"""
        if not self.launcher or not hasattr(self.launcher, 'programs'):
            return
        
        # Выбираем файл для сохранения
        file_types = {
            "json": [("JSON файлы", "*.json"), ("Все файлы", "*.*")],
            "csv": [("CSV файлы", "*.csv"), ("Все файлы", "*.*")],
            "txt": [("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        }
        
        filename = filedialog.asksaveasfilename(
            title="Сохранить как",
            filetypes=file_types[format_type],
            defaultextension=f".{format_type}"
        )
        
        if not filename:
            return
        
        try:
            if format_type == "json":
                self.export_to_json(filename)
            elif format_type == "csv":
                self.export_to_csv(filename)
            elif format_type == "txt":
                self.export_to_txt(filename)
            
            messagebox.showinfo("Успех", f"Программы успешно экспортированы в {filename}")
            window.destroy()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при экспорте: {str(e)}")
    
    def export_to_json(self, filename: str):
        if not self.launcher or not hasattr(self.launcher, 'programs'):
            return
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.launcher.programs, f, ensure_ascii=False, indent=2)
    
    def export_to_csv(self, filename: str):
        if not self.launcher or not hasattr(self.launcher, 'programs'):
            return
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Название', 'Путь', 'Описание', 'Категория', 'Дата добавления'])
            for program in self.launcher.programs:
                writer.writerow([
                    program.get('name', ''),
                    program.get('path', ''),
                    program.get('description', ''),
                    program.get('category', ''),
                    program.get('date_added', '')
                ])
    
    def export_to_txt(self, filename: str):
        if not self.launcher or not hasattr(self.launcher, 'programs'):
            return
        with open(filename, 'w', encoding='utf-8') as f:
            for program in self.launcher.programs:
                f.write(f"Название: {program.get('name', '')}\n")
                f.write(f"Путь: {program.get('path', '')}\n")
                f.write(f"Описание: {program.get('description', '')}\n")
                f.write(f"Категория: {program.get('category', '')}\n")
                f.write(f"Дата добавления: {program.get('date_added', '')}\n")
                f.write("-" * 50 + "\n")
    
    def show_import_dialog(self):
        """Показать диалог импорта"""
        if not self.launcher:
            messagebox.showerror("Ошибка", "Лаунчер не инициализирован!")
            return
        
        # Выбираем файл для импорта
        filename = filedialog.askopenfilename(
            title="Выберите файл для импорта",
            filetypes=[
                ("JSON файлы", "*.json"),
                ("CSV файлы", "*.csv"),
                ("Текстовые файлы", "*.txt"),
                ("Все файлы", "*.*")
            ]
        )
        
        if not filename:
            return
        
        try:
            # Определяем формат по расширению
            ext = os.path.splitext(filename)[1].lower()
            
            if ext == '.json':
                self.import_from_json(filename)
            elif ext == '.csv':
                self.import_from_csv(filename)
            elif ext == '.txt':
                self.import_from_txt(filename)
            else:
                messagebox.showerror("Ошибка", "Неподдерживаемый формат файла!")
                return
            
            messagebox.showinfo("Успех", "Программы успешно импортированы!")
            
            # Обновляем интерфейс
            if hasattr(self.launcher, 'update_program_cards'):
                self.launcher.update_program_cards()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при импорте: {str(e)}")
    
    def import_from_json(self, filename: str):
        if not self.launcher or not hasattr(self.launcher, 'programs'):
            return
        with open(filename, 'r', encoding='utf-8') as f:
            imported_programs = json.load(f)
        for program in imported_programs:
            if not any(p['name'] == program['name'] for p in self.launcher.programs):
                self.launcher.programs.append(program)
        if hasattr(self.launcher, 'save_programs'):
            self.launcher.save_programs()
    
    def import_from_csv(self, filename: str):
        if not self.launcher or not hasattr(self.launcher, 'programs'):
            return
        imported_programs = []
        with open(filename, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                program = {
                    'name': row.get('Название', ''),
                    'path': row.get('Путь', ''),
                    'description': row.get('Описание', ''),
                    'category': row.get('Категория', 'Общие'),
                    'date_added': row.get('Дата добавления', '')
                }
                imported_programs.append(program)
        for program in imported_programs:
            if not any(p['name'] == program['name'] for p in self.launcher.programs):
                self.launcher.programs.append(program)
        if hasattr(self.launcher, 'save_programs'):
            self.launcher.save_programs()
    
    def import_from_txt(self, filename: str):
        """Импорт из TXT (базовая реализация)"""
        # Простая реализация - можно расширить
        messagebox.showinfo("Информация", "Импорт из TXT файлов пока не поддерживается")
    
    def create_backup(self):
        if not self.launcher or not hasattr(self.launcher, 'programs'):
            messagebox.showerror("Ошибка", "Не удалось создать резервную копию!")
            return
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = os.path.join(backup_dir, f"programs_backup_{timestamp}.json")
        try:
            with open(backup_filename, 'w', encoding='utf-8') as f:
                json.dump(self.launcher.programs, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Успех", f"Резервная копия создана: {backup_filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при создании резервной копии: {str(e)}")
    
    def on_program_launched(self, program: Dict[str, Any]) -> None:
        """При запуске программы ничего не делаем"""
        pass
    
    def on_program_added(self, program: Dict[str, Any]) -> None:
        """При добавлении программы ничего не делаем"""
        pass
    
    def on_program_removed(self, program: Dict[str, Any]) -> None:
        """При удалении программы ничего не делаем"""
        pass 