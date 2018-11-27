import os
import re
import requests
from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import urljoin

Response = requests.get("http://exam.lib.ntu.edu.tw/graduate")
PDFImages = BeautifulSoup(Response.text, "lxml").find_all(
    "img", class_=re.compile(".*field-icon-application-pdf$"))

OutputPath = os.path.abspath("..\PythonResults")
if not os.path.exists(OutputPath):
    os.makedirs(OutputPath)

for PDFIndex, PDFImage in enumerate(PDFImages):
    PDFUrl = urljoin(Response.url, PDFImage.parent['href'])
    FileNames = os.path.basename(PDFUrl).split('&')
    FileName = os.path.join(OutputPath, FileNames[0])
    PDFStream = requests.get(PDFUrl, stream=True)
    with open(FileName, 'wb') as FileWriter:
        for StreamBuffer in PDFStream.iter_content(2048):
            FileWriter.write(StreamBuffer)
    print(str(PDFIndex + 1) + "/" + str(len(PDFImages)) + " save file " + FileName)
