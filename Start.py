import datetime

import requests
from bs4 import BeautifulSoup

StartTime = datetime.datetime.now()
Response = requests.get("https://jimmy15923.github.io/example_page")
if Response.status_code != 200:
    print("Response Status: response.status_code")
else:
    with open("Error.log", mode="w", encoding='UTF-8') as FileError:
        FileError.write(Response.text + '\n')
        Soup = BeautifulSoup(Response.text, "lxml")
        FileError.write(Soup.find("h1").text)
        FileError.write('\n' + '_' * 50 + '\n')
print("使用 ", (datetime.datetime.now() - StartTime).total_seconds(), " 秒")

from selenium import webdriver

ChromeDriver = webdriver.Chrome("D:/Document/Python/chromedriver")
ChromeDriver.get("http://www.sharecourse.net/sharecourse/course")
Soap = BeautifulSoup(ChromeDriver.page_source, "lxml")
with open("Error.log", mode="a", encoding='UTF-8') as FileError:
    for ClassDiv in Soap.findAll("div", {"class": "card hvr-underline-from-center"}):
        FileError.write('\n' + '_' * 50 + '\n')
        for BodyDiv in ClassDiv.findAll("div", {"class": "card-body"}):
            FileError.write(BodyDiv.text + '\n')
        FileError.write(ClassDiv.get("onclick") + '\n')
ChromeDriver.close()
print("使用 ", (datetime.datetime.now() - StartTime).total_seconds(), " 秒")

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
