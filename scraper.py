from bs4 import BeautifulSoup
import requests
from converter import convert_price

def parse_game_info(url):
    # Отправляем запрос на сервер и получаем HTML-код страницы
    response = requests.get(url)
    html = response.text

    # Создаем объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Ищем элемент с названием игры
    game_title_element = soup.find('div', {'class': 'game-title-info-name'})
    game_title = game_title_element.text

    # Ищем div с классом "game-title-info"
    game_info_div = soup.find('div', {'class': 'game-title-info'})

    # Ищем все теги <a> с атрибутом itemprop="item" и извлекаем текст из вложенных тегов <span>
    platform_elements = game_info_div.find_all('a', {'itemprop': 'item'})
    platforms = [platform.find('span', {'itemprop': 'name'}).text.replace(' ', '') for platform in platform_elements]

    # Ищем тег <meta> с атрибутом itemprop="price" и извлекаем значение его атрибута content
    price_element = soup.find('meta', {'itemprop': 'price'})
    price_in_lira = float(price_element['content']) if price_element else 0

    # Конвертируем цену в рубли
    price_in_rubles = convert_price(price_in_lira)

    # Добавляем символ рубля к цене
    price = f"{price_in_rubles}₽"

    # Ищем тег <span> с классом "game-cover-save-bonus" и извлекаем его текст
    discount_bonus_element = soup.find('span', {'class': 'game-cover-save-bonus'})
    discount_regular_element = soup.find('span', {'class': 'game-cover-save-regular'})

    if discount_bonus_element:
        discount = discount_bonus_element.text
    elif discount_regular_element:
        discount = discount_regular_element.text
    else:
        discount = ''

    # Ищем все теги <li> с атрибутом itemprop="itemListElement"
    list_elements = soup.find_all('li', {'itemprop': 'itemListElement'})

    # Извлекаем текст из вложенного тега <span> с атрибутом itemprop="name" для тега <li>, у которого <meta itemprop="position" content="3">
    platforms = ''
    for list_element in list_elements:
        meta_tag = list_element.find('meta', {'itemprop': 'position', 'content': '3'})
        if meta_tag:
            platforms = list_element.find('span', {'itemprop': 'name'}).text.replace(' ', '')
            break

    # Ищем ссылку на страницу игры в PS Store
    ps_store_link_element = soup.find('a', {'class': 'game-buy-button-href'})
    ps_store_link = ps_store_link_element['href'] if ps_store_link_element else ''

    # Отправляем запрос на сервер и получаем HTML-код страницы PS Store
    response = requests.get(ps_store_link)
    html = response.text

    # Создаем объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Ищем теги <dd> с атрибутами data-qa для PS4 и PS5
    voice_values = []
    for attr in ["gameInfo#releaseInformation#voice-value", "gameInfo#releaseInformation#ps4Voice-value", "gameInfo#releaseInformation#ps5Voice-value"]:
        element = soup.find('dd', {'data-qa': attr})
        if element:
            voice_values.append(element.text)

    subtitles_values = []
    for attr in ["gameInfo#releaseInformation#subtitles-value", "gameInfo#releaseInformation#ps4Subtitles-value", "gameInfo#releaseInformation#ps5Subtitles-value"]:
        element = soup.find('dd', {'data-qa': attr})
        if element:
            subtitles_values.append(element.text)

    # Проверяем, содержат ли тексты "Rusça"
    if any("Rusça" in value for value in voice_values):
        language = "ПОЛНОСТЬЮ НА РУССКОМ"
    elif any("Rusça" in value for value in subtitles_values):
        language = "РУССКИЕ СУБТИТРЫ"
    elif voice_values or subtitles_values:  # Если были найдены теги с информацией о языке
        language = "АНГЛИЙСКИЙ ЯЗЫК"
    else:
        language = ""  # Если теги с информацией о языке не были найдены

    return game_title, platforms, price, discount, language
