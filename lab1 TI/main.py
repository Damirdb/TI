import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from calculations import variant_1, variant_2, variant_3  

def create_matrix_inputs(rows, cols):
    # Создание полей ввода для матрицы с заданными размерами
    for widget in matrix_frame.winfo_children():
        widget.destroy()  

    global matrix_entries
    matrix_entries = []
    for i in range(rows):
        row_entries = []
        for j in range(cols):
            entry = ttk.Entry(matrix_frame, width=5, font=("Arial", 10), justify="center")
            entry.grid(row=i, column=j, padx=5, pady=5)
            row_entries.append(entry)
        matrix_entries.append(row_entries)

    choice = variant_combobox.current() + 1
    if choice == 1:
        update_vector_label("Введите ансамбль A:")
        create_vector_inputs(rows)
    elif choice == 2:
        update_vector_label("Введите ансамбль B:")
        create_vector_inputs(cols)
    else:
        update_vector_label("")
        hide_vector_frame()

    create_calculate_button()  
    result_label.pack_forget()  

def create_vector_inputs(size):
    # Создание полей ввода для вектора с заданным размером
    for widget in vector_frame.winfo_children():
        widget.destroy()  

    global vector_entries
    vector_entries = []
    for i in range(size):
        entry = ttk.Entry(vector_frame, width=5, font=("Arial", 10), justify="center")
        entry.grid(row=0, column=i, padx=5, pady=5)
        vector_entries.append(entry)

    label_vector.pack(side=tk.TOP, pady=5)  
    vector_frame.pack(side=tk.TOP, pady=5)  

def hide_vector_frame():
    label_vector.pack_forget()
    vector_frame.pack_forget()

def clear_matrix():
    for widget in matrix_frame.winfo_children():
        widget.destroy()

def create_calculate_button():
    # Создание кнопки 'Вычислить'.
    global button_calculate
    if button_calculate:
        button_calculate.destroy()
    button_calculate = ttk.Button(root, text="Вычислить", command=calculate, style="TButton")
    button_calculate.pack(side=tk.TOP, pady=15)  

def clear_results():
    result_text.set("")  

def update_vector_label(text):
    label_vector.config(text=text)

def calculate():
    # Выполнение вычислений в зависимости от выбранного варианта.
    choice = variant_combobox.current() + 1
    try:
        matrix = np.array([[float(entry.get()) for entry in row] for row in matrix_entries])

        if choice in [1, 2]:
            vector = np.array([float(entry.get()) for entry in vector_entries])
        else:
            vector = None

        if choice == 1:
            result = variant_1(matrix, vector)
            result_text.set(f"Результаты для варианта 1:\n{format_results(result)}")
        elif choice == 2:
            result = variant_2(matrix, vector)
            result_text.set(f"Результаты для варианта 2:\n{format_results(result)}")
        elif choice == 3:
            result = variant_3(matrix)
            result_text.set(f"Результаты для варианта 3:\n{format_results(result)}")

        result_label.pack(side=tk.TOP, pady=10)  
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def format_results(result):
    # Форматирование результата для вывода
    keys = [
        "P(A)",
        "P(B)",
        "H(A)",
        "H(B)",
        "H(A|B)",
        "H(B|A)",
        "H(AB)",
        "I(AB)",
        "Матрица P(A|B)",
        "Матрица P(B|A)",
        "Совместные вероятности P(AB)"
    ]
    
    formatted_result = []
    for key, value in zip(keys, result):
        if isinstance(value, np.ndarray):  
            formatted_value = np.array2string(value, precision=4, separator=', ', suppress_small=True)
            formatted_result.append(f"{key}:\n{formatted_value}")
        else:  
            formatted_result.append(f"{key}: {value:.4f}" if isinstance(value, (float, int)) else f"{key}:\n{value}")

    return '\n'.join(formatted_result)

# Создание основного окна
root = tk.Tk()
root.title("Вычисление энтропии и взаимной информации")

# Устанавливаем стиль для элементов
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("TLabel", font=("Arial", 10))
style.configure("TEntry", font=("Arial", 10))

def on_variant_change(event=None):
    # Смена варианта
    clear_results()  
    clear_matrix()  
    hide_vector_frame()  
    if button_calculate:
        button_calculate.destroy()

# Выпадающий список для выбора варианта
variant_label = ttk.Label(root, text="Выберите вариант:")
variant_label.pack(anchor=tk.W, pady=5)

variant_combobox = ttk.Combobox(root, values=[
    "Вариант 1: Ансамбль A и канальная матрица p(bj|ai)",
    "Вариант 2: Ансамбль B и канальная матрица p(ai|bj)",
    "Вариант 3: Матрица совместных вероятностей p(aibj)"
], state="readonly", font=("Arial", 10), width=50)
variant_combobox.bind("<<ComboboxSelected>>", on_variant_change)
variant_combobox.pack(pady=5)
variant_combobox.current(0)

# Поля для выбора размера матрицы
label_rows = ttk.Label(root, text="Введите количество строк матрицы:")
label_rows.pack(pady=5)  
entry_rows = ttk.Entry(root, width=5, font=("Arial", 10))
entry_rows.pack(pady=5)  

label_cols = ttk.Label(root, text="Введите количество столбцов матрицы:")
label_cols.pack(pady=5)  
entry_cols = ttk.Entry(root, width=5, font=("Arial", 10))
entry_cols.pack(pady=5)  

# Кнопка для создания матрицы
button_create_matrix = ttk.Button(root, text="Создать матрицу", 
    command=lambda: [clear_results(), create_matrix_inputs(int(entry_rows.get()), int(entry_cols.get()))])
button_create_matrix.pack(pady=15)  

# Фрейм для размещения полей ввода матрицы
matrix_frame = tk.Frame(root)
matrix_frame.pack(pady=10)

# Метка и фрейм для ввода вектора
label_vector = ttk.Label(root, text=" ")
label_vector.pack_forget()  
vector_frame = tk.Frame(root)
vector_frame.pack_forget()  

# Поле для отображения результата
result_text = tk.StringVar()
result_label = ttk.Label(root, textvariable=result_text, justify=tk.LEFT, font=("Arial", 10))

# Кнопка "Вычислить" (инициализация пустой переменной)
button_calculate = None

# Запуск основного цикла приложения
root.mainloop()
