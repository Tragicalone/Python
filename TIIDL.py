import os
import cv2
import datetime
import requests
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

StartTime = datetime.datetime.now()
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

OutputPath = os.path.abspath("..\PythonResults")
if not os.path.exists(OutputPath):
    os.makedirs(OutputPath)

ChromeDriver = webdriver.Chrome("chromedriver.exe")
ChromeDriver.get("http://insprod.tii.org.tw/database/insurance/query.asp")
ChromeDriver.maximize_window()
ChromeDriver.implicitly_wait(10)

ImageTag = ChromeDriver.find_element(By.XPATH, "//*[@id='printContext']/table/tbody/tr/td/table[2]/tbody/tr/td[1]/table[3]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[5]/td/img")

ChromeDriver.save_screenshot(os.path.join(OutputPath, "ChromeScreen.png"))
ValidateImage = Image.open(os.path.join(OutputPath, "ChromeScreen.png"))
ValidateImage = ValidateImage.crop((ImageTag.location["x"] + 1, ImageTag.location["y"] + 1, ImageTag.location["x"] + ImageTag.size["width"] - 1, ImageTag.location["y"] + ImageTag.size["height"] - 1))
ValidateImage.save(os.path.join(OutputPath, "CutScreen.png"))

ValidateRGB = cv2.imread(os.path.join(OutputPath, "CutScreen.png"))
cv2.imshow("Origin", ValidateRGB)
for IndexH in range(10):
    ModifiedRGB = cv2.fastNlMeansDenoisingColored(ValidateRGB, None,
                                                  IndexH * 10, 10, 7, 21)
    cv2.imwrite(os.path.join(OutputPath, "ModifiedCutScreen.png"), ModifiedRGB)
    ValidateImage = Image.open(
        os.path.join(OutputPath, "ModifiedCutScreen.png"))
    ValidateText = pytesseract.image_to_string(ValidateImage)
    cv2.imshow("H " + str(IndexH) + " " + ValidateText, ModifiedRGB)
cv2.waitKey(0)
cv2.destroyAllWindows()

ValidateTag = ChromeDriver.find_element(
    By.XPATH,
    "//*[@id='printContext']/table/tbody/tr/td/table[2]/tbody/tr/td[1]/table[3]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[5]/td/input[1]",
)
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
print("使用 ", (datetime.datetime.now() - StartTime).total_seconds(), " 秒")
