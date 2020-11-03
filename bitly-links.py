import requests
from dotenv import load_dotenv
import os
from urllib.parse import urlparse
import validators
import argparse

BITLY_URL ={
    'shorten': 'https://api-ssl.bitly.com/v4/shorten',
            'clicks': 'https://api-ssl.bitly.com/v4/bitlinks/'
}
headers = {
    'Authorization': '',
    'Content-Type': 'application/json'
}

data = {
    'domain': '',
    'long_url': ''
}


def shorten_link(bitly_token, url):
    headers['Authorization'] = f'Bearer {bitly_token}'
    data['long_url'] = url
    response = requests.post(BITLY_URL['shorten'], json=data, headers=headers)
    response.raise_for_status()
    bitlink = response.json()['link']
    return bitlink


def count_cliks(bitly_token, raw_link):
    headers['Authorization'] = f'Bearer {bitly_token}'
    params = {'unit': 'day', 'units': -1}
    _, url_scheme, url_path = urlparse(raw_link)[0:3]
    url = f"{BITLY_URL['clicks']}{url_scheme}{url_path}/clicks/summary"
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    total_clicks = response.json()['total_clicks']
    return total_clicks


def check_is_bitlink(bitly_token, raw_link):
    headers['Authorization'] = f'Bearer {bitly_token}'
    _, url_scheme, url_path = urlparse(raw_link)[0:3]
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{url_scheme}{url_path}'
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    link = handling_cline()
    load_dotenv()
    bitly_token = os.getenv('BITLY_TOKEN')
    is_bitlink = check_is_bitlink(bitly_token, link)
    if not validators.url(link):
        print('Ошибка в URL')
        return
    if is_bitlink:
        total_clicks = count_cliks(bitly_token, link)
        print(f"Количество переходов по ссылке битли: {total_clicks}")
        return
    bitlink = shorten_link(bitly_token, link)
    print(f'Короткая ссылка: {str(bitlink)}')


def handling_cline():
    parser = argparse.ArgumentParser()
    parser.add_argument('link', help='Enter your link here')
    args = parser.parse_args()
    return args.link



if __name__ == "__main__":
    main()