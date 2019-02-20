import os
import pandas
import datetime
import requests
from bs4 import BeautifulSoup

Response = requests.get("http://www.boxofficemojo.com/yearly/")
RowData = BeautifulSoup(Response.text, "lxml").find(
    "table", attrs={"cellspacing": "1"}).find_all("tr")
ColumnName = RowData.pop(0)
ColumnName = [Item.text for Item in ColumnName]
RowData = [list(Item.stripped_strings) for Item in RowData]
DataFrame = pandas.DataFrame(RowData, columns=ColumnName)
PathResult = os.path.abspath("Results")
if not os.path.exists(PathResult):
    os.makedirs(PathResult)
FileName = os.path.join(PathResult, "boxofficemojo.csv")
DataFrame.to_csv(FileName, index=False)
TextTarget("Save csv to {}".format(FileName))


after_one_week = datetime.datetime.now() + datetime.timedelta(weeks=1)
TextTarget("The date after one week - {}".format(after_one_week.strftime("%Y/%m/%d")))

DataForm = {"StartStation": "977abb69-413a-4ccf-a109-0272c24fd490", "EndStation": "9c5ac6ca-ec89-48f8-aab0-41b738cb1814",
            "SearchDate": after_one_week.strftime("%Y/%m/%d"), "SearchTime": "14:00", "SearchWay": "DepartureInMandarin", "RestTime": "", "EarlyOrLater": ""}

Response = requests.post(
    "https://www.thsrc.com.tw/tw/TimeTable/SearchResult", data=DataForm)

RowData = BeautifulSoup(Response.text, "lxml").table.find_all(
    "tr", recursive=False)

ColumnName, RowData = RowData[1], RowData[2:]
ColumnName = list(ColumnName.stripped_strings)

for i, row in enumerate(RowData):
    trips = row.find("td", class_="column1")
    t_departure = row.find("td", class_="column3")
    t_arrive = row.find("td", class_="column4")
    duration = row.find("td", class_="column2")
    early_ticket = row.find("td", class_="Width1")

    trips = trips.text if trips else None
    t_departure = t_departure.text if t_departure else ""
    t_arrive = t_arrive.text if t_arrive else ""
    duration = duration.text if duration else ""
    early_ticket = list(early_ticket.stripped_strings) if early_ticket else ""
    early_ticket = early_ticket[0] if early_ticket else ""

    RowData[i] = [trips, t_departure, t_arrive, duration, early_ticket]

DataFrame = pandas.DataFrame(RowData, columns=ColumnName)

FileName = os.path.join(PathResult, "thsrc_{}.csv".format(
    after_one_week.strftime("%Y%m%d")))
DataFrame.to_csv(FileName, index=False)
TextTarget("Save csv to {}".format(FileName))
