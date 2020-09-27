# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import os
import json
import re

base_url = 'https://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word='

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, compress',
    'Accept-Language': 'en-us;q=0.5,en;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}


def get_request_URL(key):
    global base_url
    return base_url + key


def request_html_body(url):
    #print(requests.get(url, "html.parser", headers=headers, allow_redirects=False))
    return requests.get(url, "html.parser", headers=headers, allow_redirects=False)


def request_soup_body(html):
    return BeautifulSoup(html.text, features="lxml")


def find_all_data(h):
    return re.findall('"objURL":"(.*?)",', h, re.S)


def find_img(s):
    img_list = s.find_all('img', attrs={"class": "main_img"})
    return img_list


def _init():
    res = get_request_URL('umbrella')
    html_body = request_html_body(res)
    all_data = find_all_data(html_body.text)
    print(all_data)


_init()
