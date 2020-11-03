import requests
from dotenv import load_dotenv
import os
from urllib.parse import urlparse
import validators
import argparse

BITLY_URL = {
    'shorten': 'https://api-ssl.bitly.com/v4/shorten',
    'clicks': 'https://api-ssl.bitly.com/v4/bitlinks/'
}


def shorten_link(headers, data):
    response = requests.post(BITLY_URL['shorten'], json=data, headers=headers)
    response.raise_for_status()
    bitlink = response.json()['link']
    return bitlink


def count_cliks(headers, raw_link):
    params = {'unit': 'day', 'units': -1}
    _, url_scheme, url_path = urlparse(raw_link)[0:3]
    url = f"{BITLY_URL['clicks']}/{url_scheme}{url_path}/clicks/summary"
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    total_clicks = response.json()['total_clicks']
    return total_clicks


def check_is_bitlink(headers, raw_link):
    _, url_scheme, url_path = urlparse(raw_link)[0:3]
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{url_scheme}{url_path}'
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    link = get_url_from_user()
    load_dotenv()
    bitly_token = os.getenv('BITLY_TOKEN')
    headers = make_request_fields(bitly_token, link)['headers']
    data = make_request_fields(bitly_token, link)['data']
    if not validators.url(link):
        print('Ошибка в URL')
        return
    is_bitlink = check_is_bitlink(headers, link)
    if is_bitlink:
        total_clicks = count_cliks(headers, link)
        print(f"Количество переходов по ссылке битли: {total_clicks}")
        return
    bitlink = shorten_link(headers, data)
    print(f'Короткая ссылка: {bitlink}')


def get_url_from_user():
    parser = argparse.ArgumentParser()
    parser.add_argument('link', help='Enter your link here')
    args = parser.parse_args()
    return args.link


def make_request_fields(bitly_token, link=''):
    headers = {
        'Authorization': f'Bearer {bitly_token}',
        'Content-Type': 'application/json'
    }
    if link:
        data = {
            'long_url': link
        }
    return {'headers': headers, 'data': data}


if __name__ == "__main__":
    main()
