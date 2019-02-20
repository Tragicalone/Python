import datetime
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

StartTime = datetime.datetime.now()
ChromeDriver = webdriver.Chrome("chromedriver.exe")
ChromeDriver.get("http://www.sharecourse.net/sharecourse/course")
Soap = BeautifulSoup(ChromeDriver.page_source, "lxml")
with open("Error.log", mode="w", encoding='UTF-8') as FileError:
    for ClassDiv in Soap.findAll("div", {"class": "card hvr-underline-from-center"}):
        for BodyDiv in ClassDiv.findAll("div", {"class": "card-body"}):
            FileError.write(BodyDiv.text.replace('\n', ' ') + '\n')
        FileError.write(ClassDiv.get("onclick") + '\n')
        FileError.write('_' * 50 + '\n')
    for filterValue in Soap.find("select", {"id": "filterSelector"}).findAll("option"):
        FileError.write(filterValue.text + '\n')
    FileError.write('_' * 50 + '\n')

Filter = ChromeDriver.find_element_by_id("filterSelector")

ChromeDriver.close()
TextTarget("使用 ", (datetime.datetime.now() - StartTime).total_seconds(), " 秒")

# data2 = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
# print(data2)
# data2 = list(input("Insert Number: "))
# print(data2)
# if (1, 2, 3) in data2:
#     print(101 // 10)
#     print(10 // 3.5)
# else:
#     print(10 % 3.5)
#     print(10 ** 8)
# print("Hello\nworld\nI am Python")
