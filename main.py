import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import json
import os

# --- Настройки ---
DATA_FILE = 'tasks.json'

# Предопределенные задачи с типами
PREDEFINED_TASKS = [
    {"name": "Прочитать статью", "type": "учеба"},
    {"name": "Сделать зарядку", "type": "спорт"},
    {"name": "Разобрать почту", "type": "работа"},
    {"name": "Посмотреть обучающее видео", "type": "учеба"},
    {"name": "Погулять 30 минут", "type": "спорт"},
    {"name": "Написать отчет", "type": "работа"},
    {"name": "Выучить 10 новых слов", "type": "учеба"},
]

# --- Функции работы с данными ---
def load_tasks():
    """Загружает историю задач из JSON."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_tasks(tasks):
    """Сохраняет историю задач в JSON."""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
    except IOError as e:
        messagebox.showerror('Ошибка записи', f'Не удалось сохранить историю: {e}')

# --- Функции логики ---
def generate_task():
    """Генерирует случайную задачу и добавляет её в историю."""
    task = random.choice(PREDEFINED_TASKS)
    task_with_ts = {"name": task["name"], "type": task["type"], "timestamp": get_timestamp()}
    
    history.append(task_with_ts)
    save_tasks(history)
    update_history_table()
    
    result_label.config(text=f'Ваша задача: {task["name"]} ({task["type"]})')

def add_custom_task():
    """Добавляет новую задачу, введенную пользователем."""
    name = simpledialog.askstring("Новая задача", "Введите название задачи:")
    if not name or name.strip() == "":
        messagebox.showerror('Ошибка', 'Название задачи не может быть пустым')
        return
    
    type_ = simpledialog.askstring("Тип задачи", "Введите тип задачи (учеба, спорт, работа):")
    if not type_ or type_.strip() == "":
        messagebox.showerror('Ошибка', 'Тип задачи не может быть пустым')
        return

    task_with_ts = {"name": name.strip(), "type": type_.strip(), "timestamp": get_timestamp()}
    
    # Добавляем в предопределенный список для будущих генераций (опционально)
    PREDEFINED_TASKS.append({"name": name.strip(), "type": type_.strip()})
    
    history.append(task_with_ts)
    save_tasks(history)
    update_history_table()

def filter_tasks():
    """Фильтрует историю по выбранному типу."""
    selected_type = filter_var.get()
    
    if selected_type == 'Все':
        filtered = history
    else:
        filtered = [task for task in history if task["type"] == selected_type]
    
    update_history_table(filtered)

def get_timestamp():
    """Возвращает текущую дату и время в виде строки."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# --- Функции интерфейса ---
def update_history_table(tasks_list=None):
    """Обновляет таблицу истории."""
    if tasks_list is None:
        tasks_list = history
        
    for i in history_tree.get_children():
        history_tree.delete(i)
        
    for task in tasks_list:
        history_tree.insert('', 'end', values=(task["timestamp"], task["name"], task["type"]))

# --- Инициализация ---
root = tk.Tk()
root.title('Random Task Generator')
root.geometry('650x500')

# Загружаем историю при старте
history = load_tasks()

# Верхняя панель с кнопками
top_frame = ttk.Frame(root)
top_frame.pack(pady=10, fill='x')

gen_btn = ttk.Button(top_frame, text='Сгенерировать задачу', command=generate_task)
gen_btn.pack(side='left', padx=5)

add_btn = ttk.Button(top_frame, text='Добавить свою задачу', command=add_custom_task)
add_btn.pack(side='left', padx=5)

# Результат генерации
result_label = ttk.Label(root, text='Ваша задача появится здесь', font=('Arial', 12))
result_label.pack(pady=5)

# Фильтр по типу
filter_frame = ttk.Frame(root)
filter_frame.pack(pady=5, fill='x')

ttk.Label(filter_frame, text='Фильтр по типу:').pack(side='left')
filter_var = tk.StringVar(value='Все')
filter_options = ['Все'] + sorted(list(set([t['type'] for t in PREDEFINED_TASKS])))
filter_menu = ttk.OptionMenu(filter_frame, filter_var, *filter_options, command=lambda x: filter_tasks())
filter_menu.pack(side='left', padx=5)

# Таблица истории
cols = ('Дата и время', 'Задача', 'Тип')
history_tree = ttk.Treeview(root, columns=cols, show='headings')
for col in cols:
    history_tree.heading(col, text=col)
history_tree.column('Дата и время', width=150)
history_tree.column('Задача', width=300)
history_tree.column('Тип', width=100)
history_tree.pack(padx=10, pady=10, fill='both', expand=True)

# Обновляем таблицу при старте
update_history_table()

root.mainloop()
