import re
import os
import requests
from PIL import Image
from pprint import pprint
from bs4 import BeautifulSoup
from urllib.parse import urljoin

Request = requests.get(
    "https://afuntw.github.io/Test-Crawling-Website/pages/blog/index.html")

AllH1Text = []
ViewedURLList = []
WaitingURLList = list(set(urljoin(Request.url, ATag['href'])
                          for ATag in BeautifulSoup(Request.text, 'lxml').find_all('a')))

while WaitingURLList:
    Request = requests.get(WaitingURLList.pop())
    Soup = BeautifulSoup(Request.text, 'lxml')
    AllH1Text += [H1Tag.text for H1Tag in Soup.find_all('h1')]
    ViewedURLList += [Request.url]
    WaitingURLList += filter(lambda URLText: URLText not in ViewedURLList,
                             [urljoin(Request.url, ATag['href']) for ATag in Soup.find_all('a')])
    WaitingURLList = list(set(WaitingURLList))
    TextTarget("WaitingURLList:\n" + str(WaitingURLList) + "\nViewedURLList:\n" +
          str(ViewedURLList) + "\nAllH1Text:\n" + str(AllH1Text) + '\n' + '=' * 87)
