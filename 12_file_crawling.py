import requests
import re
import os

from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import urljoin

Response = requests.get("http://exam.lib.ntu.edu.tw/graduate")
Soup = BeautifulSoup(Response.text, "lxml")
OutputPath = os.path.abspath("Results")
if not os.path.exists(OutputPath):
    os.makedirs(OutputPath)

PDFImages = Soup.find_all("img", class_=re.compile(
    ".*field-icon-application-pdf$"))
for PDFIndex, PDFImage in enumerate(PDFImages):
    PDFUrl = urljoin(Response.url, PDFImage.parent['href'])
    FileNames = os.path.basename(PDFUrl).split('&')
    FileName = FileNames[1].replace("nid=", "") + '_' + FileNames[0]
    PDFStream = requests.get(PDFUrl, stream=True)

    FileName = os.path.join(OutputPath, FileName)
    with open(FileName, 'wb') as FileWriter:
        for StreamBuffer in PDFStream.iter_content(2048):
            FileWriter.write(StreamBuffer)

    print('({}/{}) save file {}'.format(PDFIndex + 1, len(PDFImages), FileName))
