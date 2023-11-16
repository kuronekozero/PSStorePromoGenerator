import math
import json

# Определите ваши переменные здесь
less100tr = 5
less699tr = 4.6
less1199tr = 4.3
less1799tr = 4.1
more1799tr = 4
percenttr = 0.07

less100ua = 3
less699ua = 2.8
less1199ua = 2.5
less1799ua = 2.3
more1799ua = 2
percentua = 0.07

def save_coefficients(coefficients):
    with open('coefficients.json', 'w') as f:
        json.dump(coefficients, f)

def load_coefficients():
    try:
        with open('coefficients.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def convert_price(price_in_currency, region):
    # Округляем цену в большую сторону до целых единиц
    price_in_currency = math.ceil(price_in_currency)

    # Выбираем коэффициент для конвертации в рубли в зависимости от цены
    if region == "tr-store":
        if price_in_currency < 100:
            coefficient = less100tr
        elif price_in_currency < 699:
            coefficient = less699tr
        elif price_in_currency < 1199:
            coefficient = less1199tr
        elif price_in_currency < 1799:
            coefficient = less1799tr
        else:
            coefficient = more1799tr

        if coefficient != less100tr:
            # Прибавляем 7% к цене
            price_in_currency += price_in_currency * percenttr

    elif region == "ua-store":
        if price_in_currency < 100:
            coefficient = less100ua
        elif price_in_currency < 699:
            coefficient = less699ua
        elif price_in_currency < 1199:
            coefficient = less1199ua
        elif price_in_currency < 1799:
            coefficient = less1799ua
        else:
            coefficient = more1799ua

        if coefficient != less100ua:
            # Прибавляем 7% к цене
            price_in_currency += price_in_currency * percentua

    # Округляем цену в большую сторону до целых единиц
    price_in_currency = math.ceil(price_in_currency)

    # Конвертируем цену в рубли
    price_in_rubles = price_in_currency * coefficient

    # Округляем цену в большую сторону до десятков
    price_in_rubles = math.ceil(price_in_rubles / 10.0) * 10

    return price_in_rubles
