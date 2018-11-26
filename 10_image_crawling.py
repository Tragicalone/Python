import requests
import re
import os

from bs4 import BeautifulSoup
from pprint import pprint


soup = BeautifulSoup(requests.get("https://www.pexels.com/").text, 'lxml')

article = soup.find('div', class_="photos").find_all(
    'article', class_='photo-item')
imgs = [a.find('a').find('img')['src'] for a in article]
target = imgs[:5]

pprint(target)

results = os.path.abspath('Results')

if not os.path.exists(results):
    os.makedirs(results)

for i in target:
    img_resp = requests.get(i, stream=True)
    filename = re.match(r".*(pexels-photo-([0-9]{6})\.jpeg).*", i).group(1)
    print('regex catch the name ' + filename)

    filename = os.path.join(results, filename)

    with open(filename, 'wb') as f:
        for chunk in img_resp.iter_content(2048):
            f.write(chunk)
        print('Save the img at {}'.format(filename))
