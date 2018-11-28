import os
import requests
from PIL import Image
#from time import ctime
from pprint import pprint
from bs4 import BeautifulSoup
from datetime import datetime

AssignedLastModifiedTime = datetime(2018, 1, 29, 14, 39, 10)
ImageURLS = [IMGTag['src'] for IMGTag in BeautifulSoup(requests.get(
    "https://afuntw.github.io/Test-Crawling-Website/pages/portfolio/index.html").text, "lxml").find_all('img')]

OutputPath = os.path.abspath('..\PythonResults')
if not os.path.exists(OutputPath):
    os.makedirs(OutputPath)

for ImageURL in ImageURLS:
    ImageHeaders = dict(requests.head(ImageURL).headers)
    if 'Last-Modified' in ImageHeaders and datetime.strptime(ImageHeaders['Last-Modified'], '%a, %d %b %Y %H:%M:%S GMT') < AssignedLastModifiedTime:
        continue
    ImageData = Image.open(requests.get(ImageURL, stream=True).raw)
    BaseFileName = os.path.basename(ImageURL)
    print("catch the filename " + BaseFileName +
          " and the real format is " + ImageData.format)
    SavedFileName = os.path.join(OutputPath, BaseFileName.split('.')[
                                 0] + '.' + ImageData.format.lower())
    ImageData.save(SavedFileName)
    print("save image at " + SavedFileName)
