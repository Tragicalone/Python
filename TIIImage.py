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

OutputPath = os.path.abspath("../PythonResults")
if not os.path.exists(OutputPath):
    os.makedirs(OutputPath)

ValidateRGB = cv2.imread(os.path.join(OutputPath, "CutScreen.png"), cv2.IMREAD_GRAYSCALE)
ValidateBlurRGB = cv2.medianBlur(ValidateRGB, 5)
ReturnThreshold, ValidateBlurRGB = cv2.threshold(ValidateBlurRGB, 127, 255, cv2.THRESH_BINARY)
cv2.imwrite(os.path.join(OutputPath, "ModifiedCutScreen.png"), ValidateBlurRGB)

TextTarget("BIN " + pytesseract.image_to_string(ValidateBlurRGB, config="-psm 7").replace(" ", ""))

ShowRGB = np.vstack([ValidateRGB, ValidateBlurRGB])
cv2.imshow("", ShowRGB)
cv2.waitKey(0)
cv2.destroyAllWindows()

TextTarget("使用 ", (datetime.datetime.now() - StartTime).total_seconds(), " 秒")
