import requests
from dotenv import load_dotenv
import os
from urllib.parse import urlparse
import validators

headers = {
            'Authorization': '',
            'Content-Type': 'application/json'
}

data = {
        'domain': '',
        'long_url': ''
}


Bitly_urls = {
    'shorten': 'https://api-ssl.bitly.com/v4/shorten'
}


def shorten_link(TOKEN, url):
    headers['Authorization'] = f'Bearer {TOKEN}'
    data['long_url'] = url
    response = requests.post(Bitly_urls['shorten'], json=data, headers=headers)
    response.raise_for_status()
    bitlink = response.json()['link']
    return bitlink


def count_cliks(TOKEN, raw_link):
    headers['Authorization'] = f'Bearer {TOKEN}'
    params = {'unit': 'day', 'units': -1}
    _, url_scheme,url_path = urlparse(raw_link)[0:3]
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{url_scheme}{url_path}/clicks/summary'
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    total_clicks = response.json()['total_clicks']
    return total_clicks


def check_is_bitlink(TOKEN, raw_link):
    if not validators.url(raw_link):
        print('Ошибка в URL')
        exit()
    headers['Authorization'] = f'Bearer {TOKEN}'
    _, url_scheme, url_path = urlparse(raw_link)[0:3]
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{url_scheme}{url_path}'
    response = requests.get(url, headers=headers)
    bitlink_exists = (response.status_code == 200)
    return bitlink_exists


def main():
    link = input('Введите ссылку')
    short = check_is_bitlink(TOKEN, link)
    if short:
        total_clicks = count_cliks(TOKEN, link)
        print(f"Всего кликов: {total_clicks}")
        return
    bitlink = shorten_link(TOKEN, link)
    print(f'Короткая ссылка: {str(bitlink)}')



if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    main()
    exit()


