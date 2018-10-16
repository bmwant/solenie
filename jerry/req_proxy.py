import requests

url = 'http://checkip.amazonaws.com/'

proxies = {
    'http': '116.206.61.234:8080',
    'https': '116.206.61.234:8080',
}

r = requests.get(url, proxies=proxies)
print(r.status_code)
print(r.content)
