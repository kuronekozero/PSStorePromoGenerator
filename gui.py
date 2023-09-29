import tkinter as tk
from tkinter import ttk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PS Store Reseller App")
        self.geometry("500x400")

        # Создаем поля для ввода
        self.create_label_entry("Название:", "game_name")
        self.create_label_entry("Русский язык:", "russian_language")
        self.create_label_entry("Платформы:", "platforms")
        self.create_label_entry("Версия игры:", "game_version")
        self.create_label_entry("Цена:", "game_price")
        self.create_label_entry("Скидка:", "discount")

        # Создаем кнопку отправить
        submit_button = ttk.Button(self, text="Отправить", command=self.submit)
        submit_button.pack(pady=10)

    def create_label_entry(self, label_text, entry_var_name):
        # Создаем метку
        label = ttk.Label(self, text=label_text)
        label.pack(fill='x', padx=5, pady=5)

        # Создаем поле для ввода
        entry_var = tk.StringVar()
        setattr(self, entry_var_name, entry_var)
        entry = ttk.Entry(self, textvariable=entry_var)
        entry.pack(fill='x', padx=5)

    def submit(self):
        # Здесь вы можете добавить код для обработки данных и вызова функции редактирования изображений
        print("Данные отправлены")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
