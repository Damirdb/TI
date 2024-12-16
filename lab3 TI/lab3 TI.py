import tkinter as tk
from tkinter import messagebox

def calculate_parity_bits(data_length):
    r = 0
    while (2**r < data_length + r + 1):
        r += 1
    return r

def generate_hamming_code(data):
    m = len(data)
    r = calculate_parity_bits(m)
    n = m + r
    hamming_code = ['0'] * n

    # Заполнение информационных битов
    j = 0
    for i in range(1, n + 1):
        if not (i & (i - 1)) == 0:  # Если не степень двойки
            hamming_code[i - 1] = data[j]
            j += 1

    # Расчет проверочных битов
    for i in range(r):
        parity_index = 2**i - 1
        parity = 0
        for j in range(1, n + 1):
            if j & (2**i) and j != (2**i):
                parity ^= int(hamming_code[j - 1])
        hamming_code[parity_index] = str(parity)

    return ''.join(hamming_code)

def detect_and_correct_error(hamming_code):
    n = len(hamming_code)
    r = calculate_parity_bits(n)
    error_position = 0

    # Определение позиции ошибки
    for i in range(r):
        parity = 0
        for j in range(1, n + 1):
            if j & (2**i):
                parity ^= int(hamming_code[j - 1])
        if parity != 0:
            error_position += 2**i

    if error_position:
        # Исправляем ошибку
        error_index = error_position - 1
        hamming_code = list(hamming_code)
        hamming_code[error_index] = '1' if hamming_code[error_index] == '0' else '0'
        hamming_code = ''.join(hamming_code)
    
    return error_position, hamming_code

def calculate_hamming():
    data = data_entry.get()
    if not data.isdigit():
        messagebox.showerror("Ошибка", "Введите двоичную последовательность (например, 1011).")
        return
    hamming_code = generate_hamming_code(data)
    result_label.config(text=f"Код Хэмминга: {hamming_code}")

def check_and_correct():
    received_code = error_entry.get()
    if not received_code.isdigit():
        messagebox.showerror("Ошибка", "Введите двоичную последовательность кода Хэмминга.")
        return
    error_position, corrected_code = detect_and_correct_error(received_code)
    if error_position:
        result_label.config(text=f"Ошибка в позиции: {error_position}. Исправленный код: {corrected_code}")
    else:
        result_label.config(text=f"Ошибок не обнаружено. Код: {corrected_code}")

# Создание окна
root = tk.Tk()
root.title("Код Хэмминга")

# Ввод данных
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(pady=10)

# Для расчета кода Хэмминга
data_label = tk.Label(frame, text="Введите двочиную последовательность:")
data_label.grid(row=0, column=0, sticky="w")
data_entry = tk.Entry(frame, width=20)
data_entry.grid(row=0, column=1, padx=10)
data_button = tk.Button(frame, text="Рассчитать код Хэмминга", command=calculate_hamming)
data_button.grid(row=0, column=2, padx=10)

# Для проверки и исправления кода Хэмминга
error_label = tk.Label(frame, text="Введите код Хэмминга с ошибкой:")
error_label.grid(row=1, column=0, sticky="w")
error_entry = tk.Entry(frame, width=20)
error_entry.grid(row=1, column=1, padx=10)
error_button = tk.Button(frame, text="Проверить и исправить", command=check_and_correct)
error_button.grid(row=1, column=2, padx=10)

# Результат
result_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
result_label.pack(pady=10)

# Запуск приложения
root.mainloop()