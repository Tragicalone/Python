import re
import os
import requests
from PIL import Image
from pprint import pprint
from bs4 import BeautifulSoup
from tldextract import extract
from urllib.parse import urljoin
from urllib.parse import urlparse

SearchedURLList = []
SearchURLList = ["http://aiacademy.tw/"]
RootDomain = extract(SearchURLList[0]).domain
while SearchURLList:
    CurrentURL = SearchURLList.pop()
    SearchedURLList += [CurrentURL]
    TextTarget(CurrentURL)
    for ATag in BeautifulSoup(requests.get(CurrentURL).text, "lxml").find_all('a'):
        if not ATag.has_attr("href"):
            continue
        if ATag.has_attr("class"):
            ATagClass = str(ATag["class"])
        else:
            ATagClass = ""
        ATagURL = urljoin(CurrentURL, ATag["href"])
        if extract(ATagURL).domain != RootDomain:
            continue
        if re.match(".*#.*", ATagURL):
            continue
        if re.match("[^https|http].*", urlparse(ATagURL).scheme):
            continue
        if re.match("javascript.*", ATagURL):
            continue
        if ATagURL in SearchedURLList:
            continue
        if ATagURL in SearchURLList:
            continue
        if re.match(".*disabled.*", ATagClass):
            continue
        SearchURLList += [ATagURL]
    TextTarget("SearchURLList:" + str(len(SearchURLList)) +
          ", SearchedURLList:" + str(len(SearchedURLList)))
with open("..\\PythonResults\\15_valid_URL.txt", "w") as FileWriter:
    for SearchedURL in SearchedURLList:
        FileWriter.write(SearchedURL + '\n')
pprint(SearchedURLList)
