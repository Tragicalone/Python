import os
import requests
import pandas
from bs4 import BeautifulSoup

Respose = requests.get("http://www.boxofficemojo.com/yearly/")
Soup = BeautifulSoup(Respose.text, 'lxml')
Rows = Soup.find('table', attrs={'cellspacing': '1'}).find_all('tr')

print(Rows[0])
print('_' * 50 + '\n')
print(Rows[1].stripped_strings)
print('_' * 50 + '\n')
print(list(Rows[1].stripped_strings))

ColumnNames = [Item.text for Item in Rows.pop(0)]
Rows = [list(Row.stripped_strings) for Row in Rows]


Data = pandas.DataFrame(Rows, columns=ColumnNames)

SavePath = "Results"
if not os.path.exists(SavePath):
    os.makedirs(SavePath)
Data.to_csv(SavePath + "\\boxofficemojo.csv", index=False)
