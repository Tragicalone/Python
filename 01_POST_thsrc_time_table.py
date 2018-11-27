import os
import pandas
import datetime
import requests
from bs4 import BeautifulSoup

#目前不能跑

after_one_week = datetime.datetime.now() + datetime.timedelta(weeks=1)
after_one_week_format = after_one_week.strftime('%Y/%m/%d')
print("The date after one week - " + after_one_week.strftime('%Y/%m/%d'))

form_data = {
    'StartStation': '台北站',
    'EndStation': '左營站',
    'DepartureSearchDate': after_one_week.strftime('%Y/%m/%d'),
    'DepartureSearchTime': '14:00',
}

form_data = {
    'StartStation': '977abb69-413a-4ccf-a109-0272c24fd490',
    'EndStation': '9c5ac6ca-ec89-48f8-aab0-41b738cb1814',
    'DepartureSearchDate': after_one_week.strftime('%Y/%m/%d'),
    'DepartureSearchTime': '14:00',
}

resp = requests.post(
    "https://www.thsrc.com.tw/tw/TimeTable/SearchResult", data=form_data)
soup = BeautifulSoup(resp.text, 'lxml')

rows = soup.table.find_all('tr', recursive=False)

colname, rows = rows[1], rows[2:]
colname = list(colname.stripped_strings)

for i, row in enumerate(rows):
    trips = row.find('td', class_='column1')
    t_departure = row.find('td', class_='column3')
    t_arrive = row.find('td', class_='column4')
    duration = row.find('td', class_='column2')
    early_ticket = row.find('td', class_='Width1')

    trips = trips.text if trips else None
    t_departure = t_departure.text if t_departure else ''
    t_arrive = t_arrive.text if t_arrive else ''
    duration = duration.text if duration else ''
    early_ticket = list(early_ticket.stripped_strings) if early_ticket else ''
    early_ticket = early_ticket[0] if early_ticket else ''

    rows[i] = [trips, t_departure, t_arrive, duration, early_ticket]

df = pandas.DataFrame(rows, columns=colname)
df

results = os.path.abspath('..\PythonResults')
if not os.path.exists(results):
    os.makedirs(results)

filename = os.path.join(results, 'thsrc_{}.csv'.format(
    after_one_week.strftime('%Y%m%d')))
df.to_csv(filename, index=False)
print('Save csv to {}'.format(filename))
