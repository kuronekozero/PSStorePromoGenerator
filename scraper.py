from bs4 import BeautifulSoup
import requests

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
    platforms = [platform.find('span', {'itemprop': 'name'}).text for platform in platform_elements]

    # Ищем тег <meta> с атрибутом itemprop="price" и извлекаем значение его атрибута content
    price_element = soup.find('meta', {'itemprop': 'price'})
    price = price_element['content'] if price_element else ''

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
            platforms = list_element.find('span', {'itemprop': 'name'}).text
            break

    return game_title, platforms, price, discount

















