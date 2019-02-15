import os
import cv2
import datetime
import requests
import pytesseract
import numpy as np
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

StartTime = datetime.datetime.now()
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

OutputPath = os.path.abspath("..\PythonResults")
if not os.path.exists(OutputPath):
    os.makedirs(OutputPath)

ValidateRGB = cv2.imread(os.path.join(OutputPath, "CutScreen.png"), cv2.IMREAD_GRAYSCALE)
cv2.imshow("Origin", ValidateRGB)
ValidateBlurRGB = cv2.medianBlur(ValidateRGB, 5)
ReturnThreshold, ValidateBlurRGB = cv2.threshold(ValidateBlurRGB, 127, 255, cv2.THRESH_BINARY)
ValidateText = pytesseract.image_to_string(ValidateBlurRGB, config="-c tessedit_char_whitelist=0123456789")

cv2.imshow(ValidateText, ValidateBlurRGB)
cv2.waitKey(0)
cv2.destroyAllWindows()
RGBList = []
for IndexH in range(10):
    ModifiedRGB = cv2.fastNlMeansDenoisingColored(ValidateRGB, None, IndexH * 10, IndexH * 10, 7, 21)
    ModifiedRGB = cv2.cvtColor(ModifiedRGB, cv2.COLOR_BGR2GRAY)
    ReturnThreshold, ModifiedRGB = cv2.threshold(ModifiedRGB, 127, 255, cv2.THRESH_BINARY)
    cv2.imwrite(os.path.join(OutputPath, "ModifiedCutScreen.png"), ModifiedRGB)
    ValidateImage = Image.open(os.path.join(OutputPath, "ModifiedCutScreen.png"))
    print(pytesseract.image_to_string(ValidateImage))
    RGBList += [ModifiedRGB]
ShowRGB = np.vstack(RGBList)
cv2.imshow("", ShowRGB)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("使用 ", (datetime.datetime.now() - StartTime).total_seconds(), " 秒")
