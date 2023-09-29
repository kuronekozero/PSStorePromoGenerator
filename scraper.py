import re
from bs4 import BeautifulSoup
import requests

url = 'https://www.playstation.com/en-tr/games/ea-sports-ufc-4/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Найти div с информацией об игре
game_info_div = soup.find('div', {'class': 'content-grid'})

# Извлечь данные из этого div
game_title_div = game_info_div.find(lambda tag: tag.name == 'h1' and tag.get('data-qa') and 'mfe-game-title' in tag.get('data-qa'))
game_name = game_title_div.text if game_title_div else None

# Извлечь цену игры
price_info = re.search(r'\d+,\d+ TL', game_info_div.text)
game_price = price_info.group() if price_info else None

platforms = [span.text.strip() for span in game_info_div.find_all('span') if span.text.strip() in ['PS4', 'PS5', 'PC']]

# Извлечь информацию о скидке
discount_info = game_info_div.find('span', {'data-qa': 'mfeCtaMain#offer0#discountInfo'})
if discount_info:
    discount_text = discount_info.text
    discount_percentage = re.search(r'\d+%', discount_text)
    discount = discount_percentage.group() if discount_percentage else 0
else:
    discount = None

print(game_name, game_price, platforms, discount)
