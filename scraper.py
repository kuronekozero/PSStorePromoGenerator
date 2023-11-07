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

    # Ищем все теги <li> с атрибутом itemprop="itemListElement" и извлекаем текст из вложенных тегов <span>
    platform_elements = game_info_div.find_all('li', {'itemprop': 'itemListElement'})
    platforms = [platform.find('span', {'itemprop': 'name'}).text for platform in platform_elements]

    # Возвращаем только второй элемент списка, так как это информация о платформе
    if len(platforms) > 1:
        platforms = platforms[1]

    return game_title, platforms













