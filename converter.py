import math

def convert_price(price_in_lira):
    # Округляем цену в большую сторону до целых единиц
    price_in_lira = math.ceil(price_in_lira)

    # Выбираем коэффициент для конвертации в рубли в зависимости от цены
    if price_in_lira < 100:
        coefficient = 5.4
    elif price_in_lira < 699:
        coefficient = 4.85
    elif price_in_lira < 1199:
        coefficient = 4.6
    elif price_in_lira < 1799:
        coefficient = 4.3
    else:
        coefficient = 4.2

    if coefficient == 5.4:
        pass
    else:
        # Прибавляем 7% к цене
        price_in_lira += price_in_lira * 0.07

        # Округляем цену в большую сторону до целых единиц
        price_in_lira = math.ceil(price_in_lira)

    # Конвертируем цену в рубли
    price_in_rubles = price_in_lira * coefficient

    # Округляем цену в большую сторону до десятков
    price_in_rubles = math.ceil(price_in_rubles / 10.0) * 10

    return price_in_rubles
