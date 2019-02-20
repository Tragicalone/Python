import os
import cv2
import time
import datetime
import requests
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
OutputPath = os.path.abspath("../PythonResults/TIIImage")
if not os.path.exists(OutputPath):
    os.makedirs(OutputPath)
OutputPath = os.path.abspath("../PythonResults")

StartTime = datetime.datetime.now()

ChromeDriver = webdriver.Chrome("chromedriver.exe")
ChromeDriver.get("http://insprod.tii.org.tw/database/insurance/query.asp")
ChromeDriver.maximize_window()

for IndexLoop in range(10):
    ChromeDriver.refresh()
    ChromeDriver.implicitly_wait(10)
    ImageTag = ChromeDriver.find_element(By.XPATH, "//*[@id='printContext']/table/tbody/tr/td/table[2]/tbody/tr/td[1]/table[3]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[5]/td/img")
    ChromeDriver.save_screenshot(os.path.join(OutputPath, "ChromeScreen.png"))
    ValidateImage = Image.open(os.path.join(OutputPath, "ChromeScreen.png"))
    ValidateImage = ValidateImage.crop((ImageTag.location["x"] + 1, ImageTag.location["y"] + 1, ImageTag.location["x"] + ImageTag.size["width"] - 1, ImageTag.location["y"] + ImageTag.size["height"] - 1))
    ValidateImage.save(os.path.join(OutputPath, "CutScreen.png"))
    ValidateRGB = cv2.imread(os.path.join(OutputPath, "CutScreen.png"), cv2.IMREAD_GRAYSCALE)
    ValidateBlurRGB = cv2.medianBlur(ValidateRGB, 5)
    ReturnThreshold, ValidateBlurRGB = cv2.threshold(ValidateBlurRGB, 127, 255, cv2.THRESH_BINARY)
    ValidateText = pytesseract.image_to_string(ValidateBlurRGB, config="-psm 7 -c tessedit_char_whitelist=0123456789")
    TextTarget(ValidateText)
    cv2.imwrite(os.path.join(OutputPath, "TIIImage/BUR_" + ValidateText + ".png"), ValidateBlurRGB)
    ValidateImage.save(os.path.join(OutputPath, "TIIImage/ORI_" + ValidateText + ".png"))
    time.sleep(1)


ValidateTag = ChromeDriver.find_element(By.XPATH, "//*[@id='printContext']/table/tbody/tr/td/table[2]/tbody/tr/td[1]/table[3]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[5]/td/input[1]")
ValidateTag.send_keys(ValidateText)

FileError = open("Error.log", mode="w", encoding="UTF-8")
# for ClassDiv in Soup.findAll("div", {"class": "card hvr-underline-from-center"}):
#     for BodyDiv in ClassDiv.findAll("div", {"class": "card-body"}):
#         FileError.write(BodyDiv.text.replace('\n', ' ') + '\n')
#     FileError.write(ClassDiv.get("onclick") + '\n')
#     FileError.write('_' * 50 + '\n')
# for filterValue in Soup.find("select", {"id": "filterSelector"}).findAll("option"):
#     FileError.write(filterValue.text + '\n')
# FileError.write('_' * 50 + '\n')

# Filter = ChromeDriver.find_element_by_id("filterSelector")
# Filter.click()

FileError.close()
TextTarget("使用 ", (datetime.datetime.now() - StartTime).total_seconds(), " 秒")
