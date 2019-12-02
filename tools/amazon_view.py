from bs4 import BeautifulSoup
import requests
import time
import re
import os


def get_base_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    cookies = {
        "lc-acbuk": "en_GB",
        " i18n-prefs": "GBP",
        " x-wl-uid": "11sskutT8aRflksq4oN4fPpDSeDZ4/5qB6vTwYJBeGMhBonrIhGNb/ZNtM1j9Q21ib9OvIRaoB2VCPlFUHCikjFZtEH/gW5L+I+Px0ZYbkrMMVTIVXtRAipTMOqHzHjFUfbxLFXQ8Y7M",
        " session-id": "260-1697645-0090126",
        " ubid-acbuk": "259-4044752-1476307",
        " x-acbuk": '"8467TueXm1@9HmLYUzeH1MXR65LUhuA67D@HNCI35YShLrcOATcHlFqcN4meoVKh"',
        " at-acbuk": "Atza|IwEBIMTZoqObgqGSEFkc_sIocXjhdShZN_MgM-BYojiTaEOPgPoon2I4ZT6wsRYaWF5wezwF5BcilWO2l2Eg19QalEP3_LD-byBJn0dBuX30PWPZwFHfgD_bSFREnH6IL4wWDREBw825cBC8S8UY2PKQz0-xH3Ds9vadlGg6zKTp0Y-AoiPDJ8grZI30YmBsbrk-WwKY1D0HFlHqXxHUwFDBnaM65YIhNTlaQ0THk1C7qwoKka5O15cD3s4TUoSNkULINfsXCrwlMHvxTQzV48ajowaXRvGb8IqfK-mcYMbOlMGKUos8dtUu5qUtgvnBBf4hlcahmdUnVSuMqKd9FuPyQTsqY6SWI0DJxhPjXe0H4RVcpiQbWNa4mCQdoDj2VVagQH3bOAv2imkkJ1XATE0UjJWu",
        " sess-at-acbuk": '"kIxIum1cByyUWGJ3gKHkJ3Y2CHBe2hlTqnGXu5BbogM',
        " sst-acbuk": "Sst1|PQGVBB60330Lrs_v8Q5lzpk_C0KAeNBe8JvuTPcoVFb8hrGIW3W0s6QoXn1Bc5VBxn5fUHoHvPznjvNfVqSQ9sWkJKImIvf-APJOwPO_GOsUNnGuTjkX0kn88aV5zGsEFASKQrgWYxn8BjNBogTuNg37uU0fUoUsZ-tf8A3kPuWrEmrxVHsQYRzvVVO03HhpyTYtcp81DI8ZXW3etPpbDXFtehNTm1NVRi0bIFtix5THlP95QOX-LIOqnFSl2LLaY2pvBE7Lt2ZF1CJghD0uk9TSfHC-U_0WNRysJH3oEDhAhwoj6sWHqt4oAaCxjJ_UHsMRSfpKx4LckFcRXLlqmEilVA",
        " session-token": '"tpZFJ657ILCVpsYeeOVFLrAWglUbRhL1Ag+Zn0aIcehAdTFnzF3MXYpuLXj/D30XxZc3kisVwykE/ozQXhaB3YcOlFTCvy/ELCkPezAKnkJLdODhc/TOvRdFnUqQj6YC/CbCrGJzkU3bjpETRZMxVQPKTngkMmysNO+ld3fHwmKBUI22pd2D301tzyGdgX/IlPU3sRvRrGF7SBpbc4z6lepZlYTLY4ogSs863VN7Fm2uewcXEMRIYRcdoMUIoDEDmCpYM+s/xN3Fi1jlUEvamA"',
        " session-id-time": "2082758401l",
        " csm-hit": "tb:M58NN5VF4A9YPSA0Q5WX+sa-WZTXVCG35N4G5KY7KJEJ-YSC2QC7NQVGR0RXXBXN5|1574687794714&t:1574687794714&adb:adblk_no"
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
