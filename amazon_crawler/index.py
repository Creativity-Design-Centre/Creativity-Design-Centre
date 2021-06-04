import requests
from bs4 import BeautifulSoup
import time
import re
import os
from urllib.parse import urlparse, urlencode
from urllib.request import urlretrieve


def get_base_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    cookies = {
        "session-id": "261-1957888-7202748",
        " i18n-prefs": "GBP",
        " ubid-acbuk": "261-5345569-9891737",
        " session-token": "\"E0pO45oCeR3JkxO5Bz4peu3Uvqg/HYz+E6FjhumQhGx8xQtyR5tOFbfbiQffGxFY6tX+B8Notjqc/9Mh/pJA8fy0UyZLpThpWEq70oE+g4zzQ1ItMrE4ZM0eTUJfYwsKutz+D0/DngbOvKskHKDfD3zFSRsykCzlGdlYJXR6H5Z9daML2QRGRWYfrAvTzQdikwhF9gzdLUGpuS9G9BS/t7qaQGLQgslz1vnmUw6dHm8",
        " x-acbuk": "\"4TPDu@QtIjoKoewvppBEp7zzPgOJ9YQobRZ7sCA7q6Cbc1y7WmHhK1Gd3je0E27H\"",
        " at-acbuk": "Atza|IwEBILjnl2gjznMB0Rv4BDV-PZwzxFcCekjwMxksMYhLF9CMtrwv5_eVZ_8whzpihda3cEdkwdPNoSVuZ7U6H-yUcpVvflzFZusrSk4nV6MVGmjqYThBlZP6hmyDfXrIQjgTi5JfbF7BzbXZoWjVFzGq-pUxhUarHSjz9IJxJczikatgf4gp31idDcBhoEFxdFYWThqX8O4jNm-WUlpV3dmsqA_WItjlfeIih0yt9axXPMXL6g",
        " sess-at-acbuk": "\"bbg5GxXRT/QkpYhjD6e7Z7YD6uC4GSpzMuEw8Uz6xBs",
        " sst-acbuk": "Sst1|PQH5eifgfU3Pbyy9J2vcGsY4CQahk1diJMggIX1G0JT5eoXlo2vvP43lD4IbpblADLRHk6OeLDIwFVXQakF5NF7yaaMRLnF-zreD6RmHnlPb8mOQysr5s51gtj8ohy1DXNUp3egGU5m_sJjMSVaM7H15MbRmniiIJ4BXYuRPh3JjYZSmmXNz7M45wNUvY24es8aV1BLR1H-DbE4VpGYtvoXmNtfAYsE2MAvuSpJHZMpfkvyyRGE94vUJne6O0oF4sB8MDFTngoDhuQSB3DBWRmBN9jv9QyF8nWTbRJCXAVqDowE",
        " csm-hit": "tb:s-TRR53QGNYK7QM6R6M1CV|1622725658172&t:1622725659295&adb:adblk_no",
        " session-id-time": "2082758401l"
    }
    html_content = requests.get(
        url, "html.parser", headers=headers, cookies=cookies)
    soup_content = BeautifulSoup(html_content.text, features="lxml")
    return soup_content


def get_content(addr, product):
    soup_content = get_base_data(addr)
    image_list = soup_content.findAll('div', attrs={"data-component-type": "s-search-result"})
    image_addr_list = []
    for i in image_list:
        image_tag = i.find('img', attrs={"data-image-latency": "s-product-image"})
        image_addr_list.append(image_tag.get('src'))
    download_image(image_addr_list, product)


def file_action(product):
    if not os.path.isdir('./data/%s' % product):
        os.makedirs('./data/%s' % product)


def download_image(image_list, product):
    for f in image_list:
        file_name = f.split('/')[-1]
        urlretrieve(f, './data/%s/%s' % (product, file_name))


if __name__ == "__main__":
    query = input('Please Enter the Product you wanna search:')
    file_action(query)
    page_num = input('Please Enter how many pages you want (tips: start from 0)')
    _num = int(page_num)
    for i in range(_num):
        _url = 'https://www.amazon.co.uk/s?k=%s&page=%s&qid=1622725783&ref=sr_pg_2' % (query, i + 1)
        get_content(_url, query)
