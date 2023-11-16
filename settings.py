import tkinter as tk
import os
import json
from converter import load_coefficients, save_coefficients

# Определите ваши начальные коэффициенты здесь
initial_coefficients = {
    "less100tr": 5,
    "less699tr": 4.6,
    "less1199tr": 4.3,
    "less1799tr": 4.1,
    "more1799tr": 4,
    "percenttr": 0.07,
    "less100ua": 3,
    "less699ua": 2.8,
    "less1199ua": 2.5,
    "less1799ua": 2.3,
    "more1799ua": 2,
    "percentua": 0.07
}

class SettingsWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        # Загружаем коэффициенты
        self.coefficients = load_coefficients()
        if self.coefficients is None:
            # Если файл не существует, создаем его с начальными значениями
            self.coefficients = initial_coefficients
            save_coefficients(self.coefficients)

        # Добавляем кнопки для выбора региона
        ua_button = tk.Button(self, text="Украинский регион", command=lambda: self.open_coefficients_window("ua"))
        tr_button = tk.Button(self, text="Турецкий регион", command=lambda: self.open_coefficients_window("tr"))

        ua_button.pack(pady=10)
        tr_button.pack(pady=10)

    def save_coefficients(self):
        # Создаем новый словарь для сохранения введенных значений
        new_coefficients = {}
        for price, entry in self.coefficients.items():
            coefficient = entry.get()
            new_coefficients[price] = coefficient

        # Сохраняем новые коэффициенты в файл
        save_coefficients(new_coefficients)

    def open_coefficients_window(self, region):
        # Создаем новое окно
        coefficients_window = tk.Toplevel(self)

        # Добавляем поля для ввода коэффициентов
        self.coefficients = {}
        for price in ["100", "699", "1199", "1799", "больше"]:
            label = tk.Label(coefficients_window, text=f"Коэффициент для игр дешевле {price}:")
            entry = tk.Entry(coefficients_window)
            # Вставляем текущее значение коэффициента в поле для ввода
            entry.insert(0, self.coefficients[f"less{price}{region}"])
            label.pack()
            entry.pack()
            self.coefficients[f"less{price}{region}"] = entry

        # Добавляем кнопку для сохранения коэффициентов
        save_button = tk.Button(coefficients_window, text="Сохранить", command=self.save_coefficients)
        save_button.pack(pady=10)
