import requests
import os

from PIL import Image
from bs4 import BeautifulSoup

PageResponse = requests.get(
    "https://afuntw.github.io/Test-Crawling-Website/pages/portfolio/index.html")
soup = BeautifulSoup(PageResponse.text, 'lxml')
imgItems = soup.find_all('img')
imgscrs = [imgscr['src'] for imgscr in imgItems]
OutputPath = os.path.abspath('Results')
if not os.path.exists(OutputPath):
    os.makedirs(OutputPath)

for imgscr in imgscrs:
    imgResponse = requests.get(imgscr, stream=True)
    ImageStream = Image.open(imgResponse.raw)
    FileName = os.path.join(OutputPath, os.path.basename(
        imgscr).split('.')[0] + "." + ImageStream.format.lower())
    ImageStream.save(FileName)
    print('save image at {}'.format(FileName))
