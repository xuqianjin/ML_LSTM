from bs4 import BeautifulSoup
from cmd import Cmd
from unrar import rarfile
import requests
import os
import progressbar
import shutil
import re

Host = 'http://www.jinyongwang.com'
Listurl = Host + '/lu'

filename = 'data/lu.txt'


def getList():
    res = requests.get(Listurl)
    soup = BeautifulSoup(res.text, "html5lib")
    soup = soup.find("ul", class_="mlist").find_all('li')
    proj = getProj(soup)
    proj = proj[:50]  # 取前50回
    return proj


def getProj(res):
    data = [{"name": li.get_text('', strip=True), "href": li.find('a')['href']} for li in res if li.find('a')]
    return data


def getData(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html5lib")
    soup = soup.find(id="vcon")
    soup = soup.find_all('p')
    text = ''
    for item in soup:
        text = text + item.get_text()
    print(url, '--->', len(text))
    return text


if __name__ == '__main__':
    proj = getList()
    all = ''
    for item in proj:
        try:
            data = getData(Host + item['href'])
            all = all + data
        except:
            print(item)
    with open(filename, "w", encoding='utf8') as file:
        file.write(all)
    print(len(all))
