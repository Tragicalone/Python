import re
import os
import requests
from PIL import Image
from pprint import pprint
from bs4 import BeautifulSoup
from tldextract import extract
from urllib.parse import urljoin
from urllib.parse import urlparse


def InvalidURL(AURL):
    if re.match('.*#.*', AURL): return True
    elif re.match('[^https|http].*', urlparse(AURL).scheme): return True
    elif re.match('javascript.*', AURL): return True
    else: return False


SearchedURLList = []
SearchURLList = ["http://aiacademy.tw/"]
RootDomain = extract(SearchURLList[0]).domain

while SearchURLList:
    CurrentURL = SearchURLList.pop()
    SearchedURLList.append(CurrentURL)
    ATagSet = BeautifulSoup(requests.get(CurrentURL).text, "lxml").find_all('a')
    for ATag in ATagSet:
        if not ATag.has_attr("href"):
            continue
        ATagURL = ATag["href"]
        if InvalidURL(ATagURL):
            continue
        ATagURL = urljoin(CurrentURL, ATagURL)
        if ATagURL not in SearchedURLList and ATagURL not in SearchURLList and extract(ATagURL).domain == RootDomain:
            SearchURLList.append(ATagURL)
    print("SearchURLList:" + str(len(SearchURLList)) + ", SearchedURLList:" + str(len(SearchedURLList)))
pprint(SearchedURLList)

