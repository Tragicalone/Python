import os
import re
import cv2
import time
import numpy
import pandas
import shutil
import datetime
import threading
import pytesseract
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
DownloadPath = os.path.abspath("..\\PythonResults\\SeleniumDownload")
if not os.path.exists(DownloadPath):
    os.makedirs(DownloadPath)
for FileName in os.listdir(DownloadPath):
    if re.match(".*.pdf|.*.png",  FileName.lower()):
        os.unlink(DownloadPath + "\\" + FileName)

StartTime = datetime.datetime.now()
ChromeOptions = webdriver.ChromeOptions()
ChromeOptions.add_experimental_option("prefs", {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], "download.default_directory": os.path.abspath("../PythonResults/SeleniumDownload")})

FileError = open("Error.log", mode="w", encoding="UTF-8")
FileError.close()
DownloadTable = pandas.read_csv(DownloadPath + "\\DLHistory.csv", encoding="utf_8_sig", quoting=1, dtype=numpy.str)
DownloadTable.set_index("TIISerial", inplace=True, verify_integrity=True)

ChromeDriver = webdriver.Chrome("chromedriver.exe", options=ChromeOptions)
ChromeDriver.maximize_window()
ChromeDriver.implicitly_wait(10)
ChromeDriver.get("http://insprod.tii.org.tw/database/insurance/query.asp")

CompanySelect = Select(ChromeDriver.find_element(By.XPATH, "//*[@id='printContext']/table/tbody/tr/td/table[2]/tbody/tr/td[1]/table[3]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/select"))
CompanyList = [option.text for option in CompanySelect.options]
CompanyList = [[Company[: Company.find("-")], Company[Company.find("-") + 1:]] for Company in CompanyList]

for IndexCompany, [CompanyID, CompanyName] in enumerate(CompanyList):
    # 篩選壽險
    if CompanyID[0] == "0":
        continue
    if not os.path.exists(DownloadPath + "\\" + CompanyName):
        os.makedirs(DownloadPath + "\\" + CompanyName)
    # 破驗證碼
    while True:
        ChromeDriver.get("http://insprod.tii.org.tw/database/insurance/query.asp")
        CompanySelect = Select(ChromeDriver.find_element(By.XPATH, "//*[@id='printContext']/table/tbody/tr/td/table[2]/tbody/tr/td[1]/table[3]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/select"))
        CompanySelect.select_by_index(IndexCompany)
        ImageTag = ChromeDriver.find_element(By.XPATH, "//*[@id='printContext']/table/tbody/tr/td/table[2]/tbody/tr/td[1]/table[3]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[5]/td/img")
        ChromeDriver.save_screenshot(DownloadPath + "\\ChromeScreen.png")
        RGBOrigin = cv2.imread(DownloadPath + "\\ChromeScreen.png")
        RGBOrigin = RGBOrigin[ImageTag.location["y"] + 1: ImageTag.location["y"] + ImageTag.size["height"] - 1, ImageTag.location["x"] + 1: ImageTag.location["x"] + ImageTag.size["width"] - 1]
        RGBBlurred = cv2.cvtColor(RGBOrigin, cv2.IMREAD_GRAYSCALE)
        RGBBlurred = cv2.medianBlur(RGBBlurred, 5)
        RGBBlurred = cv2.threshold(RGBBlurred, 127, 255, cv2.THRESH_BINARY)[1]

        # 只下載現售商品
        if True:
            CurrentTag = ChromeDriver.find_element(By.XPATH, "//*[@id='printContext']/table/tbody/tr/td/table[2]/tbody/tr/td[1]/table[3]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]/label[2]/input[1]")
            while not bool(CurrentTag.get_attribute("checked")):
                CurrentTag.click()

        ValidateText = ""
        for IndexH in range(4):
            RGBChar = RGBBlurred[0: RGBBlurred.shape[0], int(IndexH * RGBBlurred.shape[1] / 4): int((IndexH + 1) * RGBBlurred.shape[1] / 4)]
            ValidateText += pytesseract.image_to_string(RGBChar, config="-psm 10 -c tessedit_char_whitelist=0123456789")
        cv2.imwrite(os.path.join(DownloadPath + "\\" + ValidateText + "_ORI.png"), RGBOrigin)
        cv2.imwrite(os.path.join(DownloadPath + "\\" + ValidateText + "_BUR.png"), RGBBlurred)
        ChromeDriver.find_element(By.XPATH, "//*[@id='printContext']/table/tbody/tr/td/table[2]/tbody/tr/td[1]/table[3]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[5]/td/input[1]").send_keys(ValidateText)
        time.sleep(1)
        ChromeDriver.find_element(By.ID, "Go2225").click()
        try:
            WebDriverWait(ChromeDriver, 3).until(expected_conditions.alert_is_present())
            Alert = ChromeDriver.switch_to.alert()
            Alert.accept()
        except Exception as exception:
            break
    # 破驗證碼
    print("開始下載" + CompanyName)
    # 下載
    IndexPage = 0
    while True:
        IndexPage += 1
        ChromeDriver.get("http://insprod.tii.org.tw/database/insurance/resultQueryAll.asp?page=" + str(IndexPage) + "&fQueryAll=&CompanyID=" + CompanyID + "&categoryId=")
        time.sleep(1)

        ProductNameURLList = []
        for ProductTag in ChromeDriver.find_elements(By.XPATH, "//*[@id='printContext']/table/tbody/tr/td/table[2]/tbody/tr/td/table[3]/tbody/tr/td/table/tbody/tr[3]/td/table[2]/tbody/tr"):
            if ProductTag.size["height"] < 2:
                continue
            ProductName = ProductTag.find_element(By.XPATH, "td[2]").text.lstrip().replace("/", "／").replace("?", "？").replace("\\", "＼").replace("*", "＊").replace("#", "＃").replace("<", "＜").replace(">", "＞").replace("|", "｜").replace("\"", "”").replace(":", "：")
            LaunchDate = ProductTag.find_element(By.XPATH, "td[4]").text.strip().replace("/", "")
            CloseDate = ProductTag.find_element(By.XPATH, "td[6]").text.strip().replace("/", "")
            ProductURL = ProductTag.find_element(By.XPATH, "td[2]/a").get_attribute("href")
            TIISerial = ProductURL[ProductURL.find("productId=") + 10:]
            ProductNameURLList.append([ProductName, LaunchDate, CloseDate, TIISerial, ProductURL])

        if len(ProductNameURLList) == 0:
            break

        for [ProductName, LaunchDate, CloseDate, TIISerial, ProductURL] in ProductNameURLList:

            if TIISerial in DownloadTable.T:
                Company = DownloadTable.loc[TIISerial]
                os.rename(DownloadPath + "\\" + CompanyName + "\\" + TIISerial + "_" + Company.values[1][:50] + "_" + Company.values[2] + "_" + Company.values[3] + ".pdf", DownloadPath + "\\" + CompanyName + "\\" + TIISerial + "_" + ProductName[:50] + "_" + LaunchDate + "_" + CloseDate + ".pdf")
                DownloadTable.loc[TIISerial] = [CompanyName, ProductName, LaunchDate, CloseDate]
                continue

            ChromeDriver.execute_script("window.open('" + ProductURL + "')")
            ChromeDriver.switch_to.window(ChromeDriver.window_handles[1])

            ProvisionTag = None
            try:
                ProvisionTag = ChromeDriver.find_element(By.XPATH, "//*[@id='printContext']/table/tbody/tr/td/table[2]/tbody/tr/td/table[3]/tbody/tr/td/table[1]/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[19]/td/table/tbody/tr/td/a")
            except Exception as exception:
                FileError = open("Error.log", mode="a", encoding="UTF-8")
                FileError.write("無條款 " + CompanyName + "\\" + ProductName + "\n")
                FileError.close()

            if ProvisionTag:
                ProvisionFileName = ProvisionTag.text
                ClickReturn = ProvisionTag.click()
                ProvisionFileExists = False
                for IndexWait in range(15):
                    ProvisionFileExists = os.path.isfile(DownloadPath + "\\" + ProvisionFileName)
                    time.sleep(1)
                    if ProvisionFileExists:
                        shutil.move(DownloadPath + "\\" + ProvisionFileName, DownloadPath + "\\" + CompanyName + "\\" + TIISerial + "_" + ProductName[:50] + "_" + LaunchDate + "_" + CloseDate + ".pdf")
                        DownloadTable.loc[TIISerial] = [CompanyName, ProductName, LaunchDate, CloseDate]
                        break
                if not ProvisionFileExists:
                    FileError = open("Error.log", mode="a", encoding="UTF-8")
                    FileError.write("下載失敗 " + CompanyName + "\\" + ProductName + ".pdf\n")
                    FileError.close()

            ChromeDriver.close()
            ChromeDriver.switch_to.window(ChromeDriver.window_handles[0])
            time.sleep(0.1)

        DownloadTable.to_csv(DownloadPath + "\\DLHistory.csv", encoding="utf_8_sig", quoting=1)
        print(CompanyName + " 下蛓 " + str(IndexPage) + " 頁，目前使用 ", (datetime.datetime.now() - StartTime).total_seconds(), " 秒")
    # 下載
    print("已下蛓 " + CompanyName + " 目前使用 ", (datetime.datetime.now() - StartTime).total_seconds(), " 秒")

ChromeDriver.close()
print("共使用 ", (datetime.datetime.now() - StartTime).total_seconds(), " 秒")
