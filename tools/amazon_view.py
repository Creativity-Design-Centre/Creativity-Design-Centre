from bs4 import BeautifulSoup
import requests
import time
import re
import os
from urllib.parse import urlparse, urlencode


def get_base_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    cookies = {
       
    }
    html_content = requests.get(
        url, "html.parser", headers=headers, cookies=cookies)
    soup_content = BeautifulSoup(html_content.text, features="lxml")
    return soup_content


def get_review_count(_url):
    soup_content = get_base_data(_url)
    print(soup_content)
    review_count = soup_content.find(
        "span", attrs={"data-hook": "cr-filter-info-review-count"})
    all_count = re.findall(r"\d+\.?\d*",
                           review_count.text.split('of')[1])[0]
    return int(all_count)


def get_data(_url):
    tmp_save = []
    print(_url)
    soup_content = get_base_data(_url)
    # review_content = soup_content.find('div', attrs={"id": "cm_cr-review_list"})
    # review_content = soup_content.find('div', attrs={"class": 'review-text'})
    # review_c = review_content.find_all('div', attrs={"class": 'review-text'})
    print('-----------------> beginning')
    review_content = soup_content.find_all(
        "span", attrs={"class": "review-text"})
    for i in review_content:
        tmp_save.append(i.find("span").text + '\n')
        print('get_data', i.find("span").text)
    return tmp_save
    print('----------------> finishing')
# print(r)


if __name__ == "__main__":
    print("please input the url(address)")
    _url = input('')
    addurl = _url
    file_name = 'product-review' + addurl.split('/')[4]
    print(get_review_count(_url))
    pages = int(get_review_count(_url) / 10) - 1
    print(pages)

    for i in range(int(pages)):
        # set init page number
        i = i + 1
        # pars input url
        _parse = urlparse(_url)
        _query = _parse.query
        _query_spilt = _query.split('&')
        _new_params = {}
        for j in _query_spilt:
            key = j.split('=')[0]
            value = j.split('=')[1]
            _new_params[key] = value
        _new_params['pageNumber'] = i
        print(_new_params)
        _new_url = _parse.scheme + '://' + _parse.netloc + \
            _parse.path + '?' + urlencode(_new_params)
        # addurl = _new_url
        print('===>', _new_url)
        loop_data = get_data(_new_url)
        review_file = open('./' + file_name + '.txt', 'a')
        review_file.writelines(loop_data)
        time.sleep(10)
