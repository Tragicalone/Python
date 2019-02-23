import os
import pandas
import requests
from bs4 import BeautifulSoup

Soup = BeautifulSoup(requests.get(
    "http://www.boxofficemojo.com/yearly/").text, "lxml")
Rows = Soup.find("table", attrs={"cellspacing": '1'}).find_all("tr")

ColumnNames = [Item.text for Item in Rows.pop(0)]
Rows = [list(Row.stripped_strings) for Row in Rows]

Data = pandas.DataFrame(Rows, columns=ColumnNames)
SavePath = "..\PythonResults"
if not os.path.exists(SavePath):
    os.makedirs(SavePath)
Data.to_csv(SavePath + "\\boxofficemojo.csv", index=False)

DataLoad = pandas.read_csv(SavePath + "\\boxofficemojo.csv")
print(Data)
print(DataLoad)
