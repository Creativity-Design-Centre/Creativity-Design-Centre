import urllib.parse as up
import requests
from random import randint
import re


class search_image:
    def __init__(self, key):
        self.key = key

    def get_google_image(self):
        data = requests.get(
            "https://image.so.com/zj?ch=%s&sn=30&listtype=new&temp=1" % (self.key)).text
        print(data)
        return data

    def get_image(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, compress',
            'Accept-Language': 'en-us;q=0.5,en;q=0.3',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
        }
        url = 'https://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word='
        url = url + self.key
        res = requests.get(url, "html.parser",
                           headers=headers, allow_redirects=False).text
        img_list = re.findall('"objURL":"(.*?)",', res, re.S)
        return img_list
