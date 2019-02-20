import os
import requests
from PIL import Image
from bs4 import BeautifulSoup

soup = BeautifulSoup(requests.get(
    "https://afuntw.github.io/Test-Crawling-Website/pages/portfolio/index.html").text, 'lxml')

OutputPath = os.path.abspath('..\PythonResults')
if not os.path.exists(OutputPath):
    os.makedirs(OutputPath)

for imgscr in soup.find_all('img'):
    ImageAddress = imgscr['src']
    ImageResponse = requests.get(ImageAddress, stream=True)
    ImageStream = Image.open(ImageResponse.raw)
    FileName = os.path.join(OutputPath, os.path.basename(
        ImageAddress).split('.')[0] + "." + ImageStream.format.lower())
    ImageStream.save(FileName)
    print("save image at " + FileName)
