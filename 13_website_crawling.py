import re
import os
import requests
from PIL import Image
from pprint import pprint
from bs4 import BeautifulSoup
from urllib.parse import urljoin

AllH1Text = []
ViewedURLList = []

Request = requests.get(
    "https://afuntw.github.io/Test-Crawling-Website/pages/blog/index.html")
WaitingURLList = list(set([urljoin(Request.url, ATag['href'])
                           for ATag in BeautifulSoup(Request.text, 'lxml').find_all('a')]))
while WaitingURLList:
    Request = requests.get(WaitingURLList.pop())
    ViewedURLList.append(Request.url)
    Soup = BeautifulSoup(Request.text, 'lxml')

    AllH1Text += [H1Tag.text for H1Tag in Soup.find_all('h1')]
    WaitingURLList = list(set(WaitingURLList + list(filter(lambda URLText: URLText not in ViewedURLList,
                                                           [urljoin(Request.url, ATag['href']) for ATag in Soup.find_all('a')]))))
    print("WaitingURLList:\n" + str(WaitingURLList) + "\nViewedURLList:\n" +
          str(ViewedURLList) + "\nAllH1Text:\n" + str(AllH1Text) + '\n' + '=' * 87)
