import requests

url = 'https://www.kinopoisk.ru/film/939411/'

proxies = {
    'http': '188.235.60.170:51362',
    'https': '188.235.60.170:51362',
}

r = requests.get(url, proxies=proxies)
print(r.status_code)
print(r.content)
