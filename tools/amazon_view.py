from bs4 import BeautifulSoup
import requests
import time
import re
import os
from urllib.parse import urlparse, urlencode


def get_base_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding": "gzip, deflate", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"
    }

    cookies = {"session-id": "262-6285588-4935355", " i18n-prefs": "GBP", " ubid-acbuk": "257-2158496-9450536", " lc-acbuk": "en_GB",
               " session-token": "FwK5lvWuF0KZWniIBw1PQywMFlZ+RLLLfp4z5oIhvIrCFixTOv7Qx08S/r/qy5RKTCEaD6OkfGbFe4mE+dKH4NdPVCR40hj94cJmRh34Q164HHuiITyA4Fse6BFl9rZ7pvv+o69gcbItLmxfOHkrgYNdRODMJ578tLSAHGwOar1aa9ct8Y2EsOIQU+PLRACX", " session-id-time": "2082758401l", " csm-hit": "tb:s-3KBEGE51Y5H40ZJ52X4S|1602491049203&t:1602491051320&adb:adblk_no"}
    html_content = requests.get(
        url, "html.parser", headers=headers, cookies=cookies)
    soup_content = BeautifulSoup(html_content.text, features="lxml")
    return soup_content


def get_review_count(_url):
    soup_content = get_base_data(_url)
    review_count = soup_content.find(
        "div", attrs={"data-hook": "cr-filter-info-review-rating-count"})
    review_count = review_count.find('span').text
    review_count = review_count.replace(',', '')
    review_count = review_count.split('|')[1]
    review_count = re.findall(r"\d+\.?\d*", review_count)
    #print(int(review_count[0]))
    return (int(review_count[0]))
    # all_count = re.findall(r"\d+\.?\d*",
    #                        review_count.text.split('of')[1])[0]
    # return int(all_count)


def filter_emoji(desstr, restr=''):
    # 过滤表情
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)


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
        #print('=====<<<<<<<', i.find("span"), i.find("span") is not None)
        if i.find("span") is not None:
            tmp_save.append(filter_emoji(i.find("span").text) + '\n')
            #print('get_data', i.find("span").text)
    return tmp_save
    print('----------------> finishing')
# print(r)


if __name__ == "__main__":
    print("please input the url(address)")
    _url = input('')
    addurl = _url
    file_name = 'product-review' + addurl.split('/')[4]
    print(get_review_count(_url))
    pages = int(get_review_count(_url) / 10) + 1
    _parse = urlparse(_url)
    _query = _parse.query
    _query_spilt = _query.split('&')
    i = 0
    _new_params = {}
    for j in _query_spilt:
        key = j.split('=')[0]
        value = j.split('=')[1]
        _new_params[key] = value
    if 'pageNumber' in _new_params:
        i = _new_params['pageNumber']
        #print(i)
    else:
        i = 1
        _new_params['pageNumber'] = 1
    print(_new_params)

    for i in range(int(i), int(pages)):
        # pars input url
        _new_url = _parse.scheme + '://' + _parse.netloc + \
            _parse.path + '?' + urlencode(_new_params)
        # addurl = _new_url
        print('===>', _new_url)
        loop_data = get_data(_new_url)
        review_file = open('./' + file_name + '-' +
                           _new_params['filterByStar'] + '.txt', 'a')
        review_file.writelines(loop_data)
        i = i + 1
        _new_params['pageNumber'] = i
        time.sleep(3)
