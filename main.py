import requests
import json
from dotenv import load_dotenv

load_dotenv()
import os
import sys
# у вас в инструкции указана библиотека которая не подтягивается
from urllib.parse import urlparse

TOKEN = os.getenv('TOKEN')

headers = dict(Authorization='')

data = dict(domain="bit.ly", long_url="")

Bitly_urls = {
    'shorten': 'https://api-ssl.bitly.com/v4/shorten',
    'auth': 'https://api-ssl.bitly.com/v4/user'
}


def get_user_info():
    response = requests.get(Bitly_urls['auth'], headers=headers)
    response.raise_for_status()
    print(response)
    print(response.text)


def shorten_link(TOKEN, url):
    headers['Authorization'] = f'Bearer {TOKEN}'
    data['long_url'] = url
    json_data = json.dumps(data)
    response = requests.post(Bitly_urls['shorten'], headers=headers, data=json_data)
    response.raise_for_status()
    bitlink = json.loads(response.text)['link']
    return bitlink


def count_cliks(TOKEN, raw_link):
    headers['Authorization'] = f'Bearer {TOKEN}'
    params = {'unit': 'day', 'units': -1}
    parsed = urlparse(raw_link)
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{parsed[1]}{parsed[2]}/clicks/summary'
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    total_clicks = json.loads(response.text)['total_clicks']
    return total_clicks


def main():
    link = input('Введите ссылку')
    parsed = urlparse(link)
    short = (parsed[1] == 'bit.ly')
    try:
        if short:
            total_clicks = count_cliks(TOKEN, link)
        else:
            bitlink = shorten_link(TOKEN, link)
    except requests.exceptions.HTTPError:
        print('Ошибка в URL')
    else:
        if short:
            print(f"Всего кликов: {total_clicks}")
        else:
            print(f'Короткая ссылка: {str(bitlink)}')
    finally:
        exit()


if __name__ == "__main__":
    main()
