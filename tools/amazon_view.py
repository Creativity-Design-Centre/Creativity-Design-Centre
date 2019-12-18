from bs4 import BeautifulSoup
import requests
import time
import re
import os


def get_base_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    cookies = {
       
    }
    html_content = requests.get(
        _url, "html.parser", headers=headers, cookies=cookies)
    soup_content = BeautifulSoup(html_content.text, features="lxml")
    return soup_content


def get_review_count(_url):
    soup_content = get_base_data(_url)
    review_count = soup_content.find(
        "span", attrs={"data-hook": "cr-filter-info-review-count"})
    all_count = re.findall(r"\d+\.?\d*",
                           review_count.text.split('of')[1])[0]
    return int(all_count)


def get_data(_url):
    tmp_save = []
    soup_content = get_base_data(_url)
    # review_content = soup_content.find('div', attrs={"id": "cm_cr-review_list"})
    # review_content = soup_content.find('div', attrs={"class": 'review-text'})
    # review_c = review_content.find_all('div', attrs={"class": 'review-text'})
    print('-----------------> beginning')
    review_content = soup_content.find_all(
        "span", attrs={"class": "review-text"})
    for i in review_content:
        tmp_save.append(i.find("span").text + '\n')
        print(i.find("span").text)
    return tmp_save
    print('----------------> finishing')
# print(r)


if __name__ == "__main__":
    print("please input the url(address)")
    _url = input('')
    addurl = _url
    file_name = 'product-review' + addurl.split('/')[4]
    pages = int(get_review_count(_url) / 10) - 1
    print(pages)
    for i in range(int(pages)):
        i = i + 1
        print('page is ' + str(i))
        addurl = _url + str(i)
        print('===>', addurl)
        loop_data = get_data(addurl)
        review_file = open('./' + file_name + '.txt', 'a')
        review_file.writelines(loop_data)
        time.sleep(10)
