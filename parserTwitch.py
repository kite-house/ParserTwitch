from src.config import *
from bs4 import BeautifulSoup as bs4
import src.formAnswer as formAnswer
import asyncio
import time
import sys
import requests

def get_game_id(game_name: str):
    ''' Получение ид игры по её названию '''
    response = requests.get(f'{urlAPITwitch}/games', headers=headersTwitchAPI, params={'name': game_name})
    if response.status_code == 200:
        data = response.json()['data']
        if not data: raise ValueError("Couldn't find such a game")
        return data[0]['id']
    
    else:
        raise SystemError(str(response.json()['error']))



async def get_social_links(user_name: str):
    ''' Поиск всех социальных сетей в яндекс поиске  '''
    result = []
    response = requests.post(f'{urlYandexSearch}/?text={user_name}+стример', headers = headersYandex)
    time.sleep(1)
    if response.status_code == 200:
        soup = bs4(response.content, 'html.parser')
        answers = soup.find_all('div', class_ = 'Organic Organic_withThumb Organic_thumbFloat_right Organic_thumbPosition_full organic Typo Typo_text_m Typo_line_s')
        answers += soup.find_all(class_ = 'Organic organic Typo Typo_text_m Typo_line_s')
        try:
            if not answers: return await get_social_links(user_name)  # Если не удалось получить информацию, пробуем ещё раз
        except RecursionError:
            return result

        for data in answers:
            link = data.find('a', class_ = 'Link Link_theme_normal OrganicTitle-Link organic__url link')
            about = data.find(class_ = 'OrganicTextContentSpan')
            follows = 'Not Found'
            if link:
                if about:
                    for text in about.find_all(class_ = 'KeyValue-ItemValue'):
                        if text.text.split(' ')[0].isdigit(): #  Получаем кол-ков подписчиков
                            follows = text.text

                result.append([link['href'], follows])
    return result


async def get_streamers(game_id: str, cursor: str = '', result: list = []):
    ''' Получение всех активных стримеров по выданной игре '''
    response = requests.get(f'{urlAPITwitch}/streams', headers=headersTwitchAPI, params = {'game_id': game_id, 'after': cursor})

    if response.status_code == 200:
        data = response.json()
        try:
            cursor = data['pagination']['cursor']
        except KeyError:
            return result

        else:
            for data in data['data']:
                sys.setrecursionlimit(50)
                socials_list = await asyncio.gather(get_social_links(data['user_name']))
                sys.setrecursionlimit(1000)
                for socials in socials_list:
                    if not any('www.twitch.tv' in item[0] for item in socials): # Если твич не был найден, добавляем его по логину
                        socials.append([f'https://www.twitch.tv/{data['user_login']}', 'Not found'])
                result.append(formAnswer.to_form(socials))
            return await get_streamers(game_id, cursor, result)

    else:
        raise SystemError(str(response.json()['error']))
    