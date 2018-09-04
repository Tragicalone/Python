import datetime
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image

StartTime = datetime.datetime.now()
ChromeDriver = webdriver.Chrome("chromedriver.exe")
ChromeDriver.get("http://insprod.tii.org.tw/database/insurance/query.asp")
CSSaved = ChromeDriver.save_screenshot("ChromeScreen.png")
print("Get ChromeScreen: ", CSSaved)
Screen = Image.open("ChromeScreen.png")
Images = ChromeDriver.find_elements_by_tag_name("img")
PWRect = (Images[7].location["x"], Images[7].location["y"], Images[7].location["x"] +
          Images[7].size["width"], Images[7].location["y"] + Images[7].size["height"])
CutImage = Screen.crop(PWRect)
CutImage.save("CutScreen.png")


Soup = BeautifulSoup(ChromeDriver.page_source, "lxml")
AImages = Soup.findAll("img")
for AImage in AImages:
    print(AImage)

exit()

ChromeDriver.get("bmp.asp")

FileError = open("Error.log", mode="w", encoding="UTF-8")
for ClassDiv in Soup.findAll("div", {"class": "card hvr-underline-from-center"}):
    for BodyDiv in ClassDiv.findAll("div", {"class": "card-body"}):
        FileError.write(BodyDiv.text.replace('\n', ' ') + '\n')
    FileError.write(ClassDiv.get("onclick") + '\n')
    FileError.write('_' * 50 + '\n')
for filterValue in Soup.find("select", {"id": "filterSelector"}).findAll("option"):
    FileError.write(filterValue.text + '\n')
FileError.write('_' * 50 + '\n')

Filter = ChromeDriver.find_element_by_id("filterSelector")
Filter.click()

FileError.close()
print("使用 ", (datetime.datetime.now() - StartTime).total_seconds(), " 秒")
exit()
