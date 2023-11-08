import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from image_editor import *
from scraper import parse_game_info


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PS Store Reseller App")
        self.geometry("500x500")

        # Создаем поля для ввода
        self.create_label_entry("Ссылка:", "game_link")  # Добавляем новое поле для ввода ссылки

        # Создаем кнопку для парсинга
        parse_button = ttk.Button(self, text="Парсить", command=self.parse)  # Добавляем новую кнопку для парсинга
        parse_button.pack(pady=10)

        self.create_label_entry("Название:", "game_name")
        self.create_label_combobox("Русский язык:", "russian_language",
                                   ["РУССКИЕ СУБТИТРЫ", "ПОЛНОСТЬЮ НА РУССКОМ", "АНГЛИЙСКИЙ ЯЗЫК"])
        self.create_label_combobox("Платформы:", "platforms", ["PS4", "PS5", "PS4/PS5"])
        self.create_label_entry("Версия игры:", "game_version")
        self.create_label_entry("Цена:", "game_price")
        self.create_label_entry("Скидка:", "discount")

        # Создаем кнопку для выбора изображения
        self.image_path = tk.StringVar()
        choose_image_button = ttk.Button(self, text="Выбрать изображение", command=self.choose_image)
        choose_image_button.pack(pady=10)

        # Создаем кнопку отправить
        submit_button = ttk.Button(self, text="Отправить", command=self.submit)
        submit_button.pack(pady=10)

    def parse(self):
        # Получаем ссылку из поля для ввода
        game_link = self.game_link.get()

        # Парсим информацию с сайта
        game_name, platforms, price, discount = parse_game_info(game_link)

        # Заполняем поля для ввода
        self.game_name.set(game_name)
        self.platforms.set(platforms)
        self.game_price.set(price)
        self.discount.set(discount)  # Устанавливаем значение поля "Скидка"

    def create_label_entry(self, label_text, entry_var_name):
        # Создаем метку
        label = ttk.Label(self, text=label_text)
        label.pack(fill='x', padx=5, pady=5)

        # Создаем поле для ввода
        entry_var = tk.StringVar()
        setattr(self, entry_var_name, entry_var)
        entry = ttk.Entry(self, textvariable=entry_var)
        entry.pack(fill='x', padx=5)

    def create_label_combobox(self, label_text, combobox_var_name, values):
        # Создаем метку
        label = ttk.Label(self, text=label_text)
        label.pack(fill='x', padx=5, pady=5)

        # Создаем выпадающий список
        combobox_var = tk.StringVar()
        setattr(self, combobox_var_name, combobox_var)
        combobox = ttk.Combobox(self, textvariable=combobox_var, values=values)
        combobox.pack(fill='x', padx=5)

    def choose_image(self):
        # Открываем диалог выбора файла и сохраняем путь к выбранному файлу
        file_path = filedialog.askopenfilename()
        self.image_path.set(file_path)

    def submit(self):
        # Получаем данные из полей для ввода
        game_name = self.game_name.get()
        russian_language = self.russian_language.get()
        platforms = self.platforms.get()
        game_version = self.game_version.get()
        game_price = self.game_price.get()
        discount = self.discount.get()

        # Создаем экземпляр ImageEditor и добавляем текст на изображение
        editor = ImageEditor("newtemplate.png")

        editor.add_text(game_name, (240, 3450), "fonts/Montserrat-Regular.ttf", 250, "black")

        # Используем функцию add_gradient_text для добавления цены с градиентом
        editor.add_gradient_text(game_price, (230, 3800), "fonts/Montserrat-Bold.ttf", 750)

        editor.add_text(russian_language, (1020, 3310), "fonts/Montserrat-Bold.ttf", 110, "white")
        editor.add_text(platforms, (330, 3300), "fonts/Montserrat-Bold.ttf", 130, "white")
        editor.add_text(game_version, (240, 3750), "fonts/Montserrat-Bold.ttf", 130, "gray")

        # Load the discount square image
        discount_square = Image.open("square.png")

        # Resize the discount square image (replace 'new_width' and 'new_height' with your desired size)
        discount_square = discount_square.resize((1050, 1050))

        # Open the background image
        background = Image.open(self.image_path.get())

        # # Накладываем шаблон на выбранное изображение
        # background = Image.open(self.image_path.get())

        # Изменяем размер фонового изображения и обрезаем его до размера шаблона
        width_ratio = editor.image.width / background.width
        height_ratio = editor.image.height / background.height

        new_width = max(background.width * height_ratio, editor.image.width)
        new_height = max(background.height * width_ratio, editor.image.height)

        background = background.resize((int(new_width), int(new_height)))

        left_margin = (background.width - editor.image.width) / 2
        top_margin = (background.height - editor.image.height) / 2

        background = background.crop((left_margin,
                                      top_margin,
                                      left_margin + editor.image.width,
                                      top_margin + editor.image.height))

        background.paste(editor.image.resize(background.size), (0, 0), editor.image.resize(background.size))

        # Paste the discount square onto the image (replace 'x' and 'y' with your desired coordinates)
        if discount:
            editor.image.paste(discount_square, (2900, 3700), discount_square)
            editor.add_text(discount, (2960, 3990), "fonts/Montserrat-Black.ttf", 400, "white")

        background.paste(editor.image.resize(background.size), (0, 0), editor.image.resize(background.size))

        # Сохраняем изображение с уникальным именем файла
        output_path = "output/output.png"
        i = 1
        while os.path.exists(output_path):
            output_path = f"output/output{i}.png"
            i += 1

        background.save(output_path)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
