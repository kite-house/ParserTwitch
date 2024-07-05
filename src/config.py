from os import getenv
import requests
from fake_useragent import UserAgent

def get_access_token(client_id, client_token):
    params = {
        'client_id' : client_id,
        'client_secret' : client_token,
        'grant_type' : 'client_credentials',
    }

    response = requests.post('https://id.twitch.tv/oauth2/token', params=params)

    if response.status_code == 200:
        access_token = response.json()['access_token']
        return f'Bearer {access_token}'
    
    else:
        raise SystemError('Couldn`t get access token')

client_id = getenv('client_id')
client_token = getenv('client_token')
access_token = get_access_token(client_id, client_token)


# Заголовок для запросов Twitch
headersTwitchAPI = {
    'Client-ID': client_id,
    'Authorization': access_token
}

# Заголовок для запросов Yandex Search
headersYandex = {
    'User-Agent': UserAgent().random,
    "content-type": "application/x-www-form-urlencoded",

}


# URL API TWITCH

urlAPITwitch = 'https://api.twitch.tv/helix'

# URL YANDEX SEARCH

urlYandexSearch = 'https://yandex.ru/search'