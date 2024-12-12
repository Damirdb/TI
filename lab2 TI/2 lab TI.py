import tkinter as tk
from tkinter import filedialog, ttk
import math
from collections import Counter

# Функция для расчёта частот символов
def calculate_frequencies(text):
    total_symbols = len(text)
    frequencies = Counter(text)
    frequencies = {char: (count, count / total_symbols) for char, count in frequencies.items()}
    frequencies = dict(sorted(frequencies.items(), key=lambda item: -item[1][1]))
    return frequencies

# Кодирование Шеннона-Фано
def generate_shannon_fano(frequencies):
    symbols = list(frequencies.keys())
    codes = {}
    shannon_fano_recursive(symbols, frequencies, "", codes)
    return codes

def shannon_fano_recursive(symbols, frequencies, prefix, codes):
    if len(symbols) == 1:
        codes[symbols[0]] = prefix
        return

    total = sum(frequencies[symbol][1] for symbol in symbols)
    left_sum = 0
    min_diff = float('inf')
    split_index = 0

    for i in range(len(symbols)):
        left_sum += frequencies[symbols[i]][1]
        right_sum = total - left_sum
        diff = abs(left_sum - right_sum)
        if diff < min_diff:
            min_diff = diff
            split_index = i + 1

    shannon_fano_recursive(symbols[:split_index], frequencies, prefix + "1", codes)
    shannon_fano_recursive(symbols[split_index:], frequencies, prefix + "0", codes)

# Структура узла для дерева Хаффмана
class HuffmanNode:
    def __init__(self, symbol=None, probability=0, left=None, right=None):
        self.symbol = symbol
        self.probability = probability
        self.left = left
        self.right = right

# Построение дерева Хаффмана
def build_huffman_tree(frequencies):
    nodes = [HuffmanNode(symbol, prob) for symbol, (_, prob) in frequencies.items()]
    while len(nodes) > 1:
        nodes.sort(key=lambda node: node.probability)
        left = nodes.pop(0)
        right = nodes.pop(0)
        new_node = HuffmanNode(probability=left.probability + right.probability, left=left, right=right)
        nodes.append(new_node)
    return nodes[0]

# Генерация кодов Хаффмана с инверсией
def generate_huffman_codes(node, code="", codes=None):
    if codes is None:
        codes = {}
    if node is None:
        return
    if node.symbol is not None:
        inverted_code = "".join('1' if bit == '0' else '0' for bit in code)
        codes[node.symbol] = inverted_code
    generate_huffman_codes(node.left, code + "1", codes)
    generate_huffman_codes(node.right, code + "0", codes)
    return codes

# Кодирование сообщения
def encode_message(text, codes):
    encoded = []
    missing_symbols = set()
    for char in text:
        if char in codes:
            encoded.append(codes[char])
        else:
            missing_symbols.add(char)
    if missing_symbols:
        print(f"Предупреждение: символы {missing_symbols} отсутствуют в кодах.")
    return ''.join(encoded)

# Расчет энтропии
def calculate_entropy(frequencies):
    return -sum(prob * math.log2(prob) for _, prob in frequencies.values())

# Расчет средней длины кода
def calculate_average_length(frequencies, codes):
    return sum(frequencies[char][1] * len(code) for char, code in codes.items())

# Расчет избыточности
def calculate_redundancy(frequencies, codes, entropy):
    avg_length = calculate_average_length(frequencies, codes)
    return (avg_length - entropy) / avg_length

# Функция для обработки сообщения
def process_text(input_text):
    # 1. Преобразуем весь текст в нижний регистр для кодирования
    input_text_lower = input_text.lower()

    # 2. Рассчитываем частоты символов на основе текста в нижнем регистре
    frequencies = calculate_frequencies(input_text_lower)

    # 3. Генерация кодов
    sf_codes = generate_shannon_fano(frequencies)
    huffman_tree = build_huffman_tree(frequencies)
    huffman_codes = generate_huffman_codes(huffman_tree)

    # Метрики
    entropy = calculate_entropy(frequencies)
    avg_length_sf = calculate_average_length(frequencies, sf_codes)
    avg_length_huffman = calculate_average_length(frequencies, huffman_codes)
    redundancy_sf = calculate_redundancy(frequencies, sf_codes, entropy)
    redundancy_huffman = calculate_redundancy(frequencies, huffman_codes, entropy)

    return frequencies, sf_codes, huffman_codes, entropy, avg_length_sf, avg_length_huffman, redundancy_sf, redundancy_huffman, input_text_lower

# Функция загрузки текста из файла
def load_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not file_path:
        return
    with open(file_path, "r", encoding="utf-8") as file:
        input_field.delete(0, "end")
        input_field.insert(0, file.read())

# Обновление таблицы
def update_table(frequencies, sf_codes, huffman_codes):
    results_table.delete(*results_table.get_children())
    for char, (count, prob) in frequencies.items():
        results_table.insert("", "end", values=(char, f"{prob:.4f}", sf_codes.get(char, ""), huffman_codes.get(char, "")))

# Обновление закодированных текстов
def update_encoded_text(input_text, sf_codes, huffman_codes):
    sf_encoded = encode_message(input_text, sf_codes)
    huffman_encoded = encode_message(input_text, huffman_codes)

    sf_encoded_label.config(text=f"Шеннон-Фано Кодированный текст: {sf_encoded}")
    huffman_encoded_label.config(text=f"Хаффман Кодированный текст: {huffman_encoded}")

# Функция расчета
def calculate():
    input_text = input_field.get()
    if not input_text:
        return

    (frequencies, sf_codes, huffman_codes, entropy, avg_length_sf,
     avg_length_huffman, redundancy_sf, redundancy_huffman, input_text_lower) = process_text(input_text)

    # Обновление таблицы
    update_table(frequencies, sf_codes, huffman_codes)

    # Обновление метрик
    entropy_label.config(text=f"H(Z): {entropy:.4f}")
    sf_avg_label.config(text=f"Lср (ШФ): {avg_length_sf:.4f}")
    huffman_avg_label.config(text=f"Lср (Х): {avg_length_huffman:.4f}")
    sf_redundancy_label.config(text=f"D (ШФ): {redundancy_sf:.4f}")
    huffman_redundancy_label.config(text=f"D (Х): {redundancy_huffman:.4f}")

    # Обновление закодированных текстов
    update_encoded_text(input_text_lower, sf_codes, huffman_codes)

# Создание окна
root = tk.Tk()
root.title("Шеннон-Фано и Хаффман Кодирование")
root.geometry("1200x700")

# Верхняя панель
top_frame = tk.Frame(root)
top_frame.pack(side="top", fill="x", padx=10, pady=5)

input_label = tk.Label(top_frame, text="Введите сообщение:")
input_label.pack(side="left", padx=5)

input_field = tk.Entry(top_frame, width=100)
input_field.pack(side="left", padx=5)

load_button = tk.Button(top_frame, text="Загрузить из файла", command=load_from_file)
load_button.pack(side="left", padx=5)

calculate_button = tk.Button(top_frame, text="Рассчитать", command=calculate)
calculate_button.pack(side="left", padx=5)

clear_button = tk.Button(top_frame, text="Очистить", command=lambda: input_field.delete(0, "end"))
clear_button.pack(side="left", padx=5)

# Таблица результатов
results_label = tk.Label(root, text="Результаты кодирования", font=("Arial", 12, "bold"))
results_label.pack(side="top", pady=5)

results_table = ttk.Treeview(root, columns=("symbol", "probability", "sf_code", "huffman_code"), show="headings", height=15)
results_table.heading("symbol", text="Символ")
results_table.heading("probability", text="Вероятность")
results_table.heading("sf_code", text="Код Ш-Ф")
results_table.heading("huffman_code", text="Код Хаффмана")
results_table.column("symbol", width=70, anchor="w")
results_table.column("probability", width=100, anchor="w")
results_table.column("sf_code", width=200, anchor="w")
results_table.column("huffman_code", width=200, anchor="w")
results_table.pack(side="top", fill="both", expand=True)

# Метрики
metrics_frame = tk.Frame(root)
metrics_frame.pack(side="top", fill="x", padx=10, pady=10)

entropy_label = tk.Label(metrics_frame, text="H(Z): -", font=("Arial", 10))
entropy_label.pack(side="left", padx=10)

sf_avg_label = tk.Label(metrics_frame, text="Lср (ШФ): -", font=("Arial", 10))
sf_avg_label.pack(side="left", padx=10)

sf_redundancy_label = tk.Label(metrics_frame, text="D (ШФ): -", font=("Arial", 10))
sf_redundancy_label.pack(side="left", padx=10)

huffman_avg_label = tk.Label(metrics_frame, text="Lср (Х): -", font=("Arial", 10))
huffman_avg_label.pack(side="left", padx=10)

huffman_redundancy_label = tk.Label(metrics_frame, text="D (Х): -", font=("Arial", 10))
huffman_redundancy_label.pack(side="left", padx=10)

# Закодированные тексты
encoded_text_frame = tk.Frame(root)
encoded_text_frame.pack(side="top", fill="x", padx=10, pady=10)

sf_encoded_label = tk.Label(encoded_text_frame, text="Шеннон-Фано Кодированный текст: -", wraplength=1000, justify="left")
sf_encoded_label.pack(side="top", fill="x", pady=5)

huffman_encoded_label = tk.Label(encoded_text_frame, text="Хаффман Кодированный текст: -", wraplength=1000, justify="left")
huffman_encoded_label.pack(side="top", fill="x", pady=5)

# Запуск приложения
root.mainloop()
