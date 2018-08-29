import datetime
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

StartTime = datetime.datetime.now()
ChromeDriver = webdriver.Chrome("D:/Document/Python/chromedriver")
ChromeDriver.get("http://insprod.tii.org.tw/database/insurance/query.asp")
Soup = BeautifulSoup(ChromeDriver.page_source, "lxml")
Temp = Soup.findAll("img")
ChromeDriver.get("bmp.asp")


print("使用 ", (datetime.datetime.now() - StartTime).total_seconds(), " 秒")
exit()

FileError = open("Error.log", mode="w", encoding='UTF-8')
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
ChromeDriver.close()
