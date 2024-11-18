import tkinter as tk
from tkinter import messagebox
import numpy as np
from entropy_math import calc_entropies  # Импортируем функцию расчета энтропии

# Инициализация n_A и d значениями по умолчанию
n_A = 0
d = 0

def create_entries(n, rows, entry_list, grid_row, label_text):
    """Функция для создания динамических полей ввода с n ячейками в каждой строке."""
    for entry in entry_list:
        entry.destroy()
    entry_list.clear()

    for i in range(rows):
        if i == 0:
            label = tk.Label(root, text=label_text)
            label.grid(row=grid_row + i, column=0, padx=5, pady=5, sticky="w")

        for j in range(n):
            entry = tk.Entry(root, width=8)
            entry.grid(row=grid_row + i, column=j + 1, padx=1, pady=1, sticky="w")
            entry_list.append(entry)

def calculate():
    """Производит расчет энтропии и выводит все значения и массивы в отдельном окне."""
    try:
        p_A, p_B, p_A_given_B, p_B_given_A, p_joint = None, None, None, None, None
        
        if method_var.get() == 1:  # Метод 1: заданы p(A) и p(B|A)
            p_A = np.array([float(entry.get()) for entry in entry_A])
            p_B_given_A = np.array([[float(entry.get()) for entry in entry_B_given_A[i:i+d]] 
                                    for i in range(0, len(entry_B_given_A), d)])

            if len(p_A) != n_A:
                raise ValueError(f"Ошибка: число элементов p(A) должно быть равно {n_A}.")
            if p_B_given_A.shape != (n_A, d):
                raise ValueError(f"Ошибка: размеры p(B|A) должны быть ({n_A}, {d}).")

            H_A, H_B, H_AB, H_A_given_B, H_B_given_A, I_AB, p_joint, p_A_given_B, p_B_given_A = \
                calc_entropies(p_A=p_A, p_B_given_A=p_B_given_A)

        elif method_var.get() == 2:  # Метод 2: заданы p(B) и p(A|B)
            p_B = np.array([float(entry.get()) for entry in entry_B])
            p_A_given_B = np.array([[float(entry.get()) for entry in entry_A_given_B[i:i+n_A]] 
                                     for i in range(0, len(entry_A_given_B), n_A)])

            if len(p_B) != d:
                raise ValueError(f"Ошибка: число элементов p(B) должно быть равно {d}.")
            if p_A_given_B.shape != (d, n_A):
                raise ValueError(f"Ошибка: размеры p(A|B) должны быть ({d}, {n_A}).")

            H_A, H_B, H_AB, H_A_given_B, H_B_given_A, I_AB, p_joint, p_A_given_B, p_B_given_A = \
                calc_entropies(p_B=p_B, p_A_given_B=p_A_given_B)

        elif method_var.get() == 3:  # Метод 3: задана совместная вероятность p(A,B)
            p_joint = np.array([[float(entry.get()) for entry in entry_joint[i:i+d]] 
                                 for i in range(0, len(entry_joint), d)])

            if p_joint.shape != (n_A, d):
                raise ValueError(f"Ошибка: размеры p(A,B) должны быть ({n_A}, {d}).")

            # Расчет p(B)
            p_B = np.sum(p_joint, axis=0)  # Суммируем по строкам для получения p(B)

            # Расчет p(A|B)
            p_A_given_B = p_joint / p_B  # Делим элементы p(A,B) на p(B)

            # Расчет p(A)
            p_A = np.sum(p_joint, axis=1)  # Суммируем по столбцам для получения p(A)

            # Расчет p(B|A)
            p_B_given_A = p_joint / p_A[:, np.newaxis]  # Делим элементы p(A,B) на p(A)

            H_A, H_B, H_AB, H_A_given_B, H_B_given_A, I_AB, p_joint, p_A_given_B, p_B_given_A = \
                calc_entropies(p_joint=p_joint)

        # Создаем окно результатов
        result_window = tk.Toplevel(root)
        result_window.title("Результаты расчета")

        result_text = (f"H(A): {H_A:.4f}\n"
                       f"H(B): {H_B:.4f}\n"
                       f"H(A|B): {H_A_given_B:.4f}\n"
                       f"H(B|A): {H_B_given_A:.4f}\n"
                       f"H(AB): {H_AB:.4f}\n"
                       f"I(AB): {I_AB:.4f}\n\n"
                       f"p(A): {np.array2string(p_A, precision=4) if p_A is not None else 'N/A'}\n"
                       f"p(B): {np.array2string(p_B, precision=4) if p_B is not None else 'N/A'}\n"
                       f"p(A|B): {np.array2string(p_A_given_B, precision=4) if p_A_given_B is not None else 'N/A'}\n"
                       f"p(B|A): {np.array2string(p_B_given_A, precision=4) if p_B_given_A is not None else 'N/A'}\n"
                       f"p(A,B): {np.array2string(p_joint, precision=4) if p_joint is not None else 'N/A'}\n")

        result_label = tk.Label(result_window, text=result_text, justify=tk.LEFT)
        result_label.pack(padx=10, pady=10)

    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при расчете: {e}")

# Остальная часть GUI остается без изменений


def confirm_values():
    """Подтверждаем количество элементов и вызываем обновление интерфейса."""
    try:
        global n_A, d
        n_A = int(entry_n_A.get() or 0)
        d = int(entry_d.get() or 0)

        if n_A <= 0 or d <= 0:
            raise ValueError("Введите положительное количество элементов для A и B")

        update_ui()

    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные положительные числа для количества элементов n и d")

def update_ui():
    """Обновляем интерфейс в зависимости от выбранного метода"""
    if n_A <= 0 or d <= 0:
        return  # Пропускаем обновление, если значения не заданы

    # Скрываем все поля ввода для обновления
    for widget in root.grid_slaves():
        if int(widget.grid_info()["row"]) > 2:
            widget.grid_forget()

    # Создание полей ввода в зависимости от выбранного метода
    if method_var.get() == 1:
        create_entries(d, n_A, entry_B_given_A, 4, "p(B|A):")
        create_entries(n_A, 1, entry_A, 3, "p(A):")

    elif method_var.get() == 2:
        create_entries(d, n_A, entry_A_given_B, 4, "p(A|B):")
        create_entries(d, 1, entry_B, 3, "p(B):")

    elif method_var.get() == 3:
        create_entries(d, n_A, entry_joint, 3, "p(A,B):")

    # Кнопка для расчета
    tk.Button(root, text="Рассчитать", command=calculate).grid(row=6, column=0, columnspan=4, padx=5, pady=10, sticky="w")

# Создаем главное окно
root = tk.Tk()
root.title("Энтропия Шеннона")
root.geometry('1920x1080')

# Инициализация переменной для выбора метода
method_var = tk.IntVar(value=1)

# Ввод количества элементов
tk.Label(root, text="Количество элементов в A (n):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_n_A = tk.Entry(root)
entry_n_A.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(root, text="Количество элементов в B (d):").grid(row=0, column=2, padx=5, pady=5, sticky="w")
entry_d = tk.Entry(root)
entry_d.grid(row=0, column=3, padx=5, pady=5, sticky="w")

# Кнопка подтверждения для ввода значений n и d
tk.Button(root, text="Подтвердить", command=confirm_values).grid(row=0, column=4, padx=5, pady=5, sticky="w")

# Метки и радио-кнопки для выбора метода
tk.Label(root, text="Выберите метод расчета:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
tk.Radiobutton(root, text="p(A) и p(B|A)", variable=method_var, value=1, command=update_ui).grid(row=1, column=1, padx=5, pady=5, sticky="w")
tk.Radiobutton(root, text="p(B) и p(A|B)", variable=method_var, value=2, command=update_ui).grid(row=1, column=2, padx=5, pady=5, sticky="w")
tk.Radiobutton(root, text="p(A,B)", variable=method_var, value=3, command=update_ui).grid(row=1, column=3, padx=5, pady=5, sticky="w")

# Создание списков для хранения полей ввода
entry_A = []
entry_B_given_A = []
entry_B = []
entry_A_given_B = []
entry_joint = []

root.mainloop()
