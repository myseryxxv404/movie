import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Имя файла для сохранения данных
DATA_FILE = 'movies.json'

# Создаем главное окно
root = tk.Tk()
root.title("Movie Library")
root.geometry("800x600")

# Загружаем существующие данные, если есть
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        movies = json.load(f)
else:
    movies = []

# Функция сохранения данных
def save_data():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

# Функция добавления фильма
def add_movie():
    title = entry_title.get()
    genre = entry_genre.get()
    year = entry_year.get()
    rating = entry_rating.get()

    # Проверки
    if not title or not genre or not year or not rating:
        messagebox.showwarning("Ошибка", "Заполните все поля.")
        return
    if not year.isdigit():
        messagebox.showwarning("Ошибка", "Год должен быть числом.")
        return
    try:
        rating_value = float(rating)
    except ValueError:
        messagebox.showwarning("Ошибка", "Рейтинг должен быть числом.")
        return
    if not (0 <= rating_value <= 10):
        messagebox.showwarning("Ошибка", "Рейтинг должен быть от 0 до 10.")
        return

    # Добавление фильма
    movie = {
        'title': title,
        'genre': genre,
        'year': int(year),
        'rating': rating_value
    }
    movies.append(movie)
    update_table()
    save_data()

    # Очистить поля после добавления
    entry_title.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_rating.delete(0, tk.END)

# Создаем форму для ввода данных
form_frame = tk.Frame(root)
form_frame.pack(pady=10)

tk.Label(form_frame, text="Название").grid(row=0, column=0, padx=5, pady=2)
entry_title = tk.Entry(form_frame)
entry_title.grid(row=0, column=1, padx=5, pady=2)

tk.Label(form_frame, text="Жанр").grid(row=0, column=2, padx=5, pady=2)
entry_genre = tk.Entry(form_frame)
entry_genre.grid(row=0, column=3, padx=5, pady=2)

tk.Label(form_frame, text="Год").grid(row=1, column=0, padx=5, pady=2)
entry_year = tk.Entry(form_frame)
entry_year.grid(row=1, column=1, padx=5, pady=2)

tk.Label(form_frame, text="Рейтинг").grid(row=1, column=2, padx=5, pady=2)
entry_rating = tk.Entry(form_frame)
entry_rating.grid(row=1, column=3, padx=5, pady=2)

# Кнопка добавления
add_button = tk.Button(root, text="Добавить фильм", command=add_movie)
add_button.pack(pady=5)

# Фильтр для жанра и года
filter_frame = tk.Frame(root)
filter_frame.pack(pady=10)

tk.Label(filter_frame, text="Фильтр по жанру").grid(row=0, column=0, padx=5)
entry_filter_genre = tk.Entry(filter_frame)
entry_filter_genre.grid(row=0, column=1, padx=5)

tk.Label(filter_frame, text="по году").grid(row=0, column=2, padx=5)
entry_filter_year = tk.Entry(filter_frame)
entry_filter_year.grid(row=0, column=3, padx=5)

def apply_filters():
    genre_filter = entry_filter_genre.get().strip().lower()
    year_filter = entry_filter_year.get().strip()
    filtered = movies

    if genre_filter:
        filtered = [m for m in filtered if genre_filter in m['genre'].lower()]
    if year_filter:
        if year_filter.isdigit():
            filtered = [m for m in filtered if m['year'] == int(year_filter)]
        else:
            messagebox.showwarning("Ошибка", "Год фильтра должен быть числом.")
            return
    update_table(filtered)

def clear_filters():
    entry_filter_genre.delete(0, tk.END)
    entry_filter_year.delete(0, tk.END)
    update_table()

# Кнопки фильтрации
filter_buttons_frame = tk.Frame(root)
filter_buttons_frame.pack()

filter_btn = tk.Button(filter_buttons_frame, text="Применить фильтр", command=apply_filters)
filter_btn.pack(side=tk.LEFT, padx=5)

clear_filter_btn = tk.Button(filter_buttons_frame, text="Очистить фильтр", command=clear_filters)
clear_filter_btn.pack(side=tk.LEFT, padx=5)

# Таблица для отображения фильмов
columns = ('title', 'genre', 'year', 'rating')
tree = ttk.Treeview(root, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, width=150)

tree.pack(fill=tk.BOTH, expand=True, pady=10)

def update_table(filtered_movies=None):
    # Очистить таблицу
    for item in tree.get_children():
        tree.delete(item)
    data = filtered_movies if filtered_movies is not None else movies
    # Заполнить таблицу
    for m in data:
        tree.insert('', tk.END, values=(m['title'], m['genre'], m['year'], m['rating']))

# Изначальное заполнение таблицы
update_table()

# Запуск главного окна
root.mainloop()
