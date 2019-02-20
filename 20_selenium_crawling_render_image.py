import os
import re
import requests
from pprint import pprint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

OutputPath = os.path.abspath('..\PythonResults')
if not os.path.exists(OutputPath):
    os.makedirs(OutputPath)

TestURL = 'https://afuntw.github.io/Test-Crawling-Website/pages/gallery/index.html'

ImageURLs = [ImageURL['src']
             for ImageURL in BeautifulSoup(requests.get(TestURL).text, 'lxml').find_all('img', class_=re.compile('.*img-change'))]
ImageURLs = list(set(ImageURLs))

for ImageURL in ImageURLs:
    ImageRequest = requests.get(ImageURL, stream=True)
    with open(os.path.join(OutputPath, "靜態" + os.path.basename(ImageURL)), 'wb') as FileWrite:
        for StreamBuffer in ImageRequest.iter_content(2048):
            FileWrite.write(StreamBuffer)

SeleniumChrome = webdriver.Chrome()
try:
    SeleniumChrome.get(TestURL)
    SeleniumChrome.maximize_window()
    SeleniumChrome.implicitly_wait(10)

    ImageURLs = [ImageURL.get_attribute('src')
                 for ImageURL in SeleniumChrome.find_elements(By.XPATH, '/html/body/div/div/div/a/img')]
    ImageURLs = list(set(ImageURLs))

    for ImageURL in ImageURLs:
        ImageRequest = requests.get(ImageURL, stream=True)
        with open(os.path.join(OutputPath, "動態" + os.path.basename(ImageURL)), 'wb') as FileWrite:
            for StreamBuffer in ImageRequest.iter_content(2048):
                FileWrite.write(StreamBuffer)

except Exception as exp:
    TextTarget(exp)
finally:
    SeleniumChrome.quit()
