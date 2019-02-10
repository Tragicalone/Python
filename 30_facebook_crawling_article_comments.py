import os
import requests
import pandas as pd
from datetime import datetime

#目前不知道如何查token
# 透過 Graph API 觀察文章 ID 與 token
article_id = '1213927345375910'
token = ''

comments = []
pages = 0

url = 'https://graph.facebook.com/v2.11/{}/comments?pretty=0&limit={}&access_token={}'.format(
    article_id, 100, token
)

#url = 'https://graph.facebook.com/v2.11/1213927345375910/comments?pretty=0&limit=100&access_token='

while True:
    pages += 1
    resp = requests.get(url)
    data = resp.json()
    comments += data['data']

    if 'next' not in data['paging']:
        print('EOF')
        break
    else:
        url = data['paging']['next']
        print('pages {}'.format(pages))

print('comment length = {}'.format(len(comments)))

df = pd.DataFrame.from_records(comments)
df.head()

results = os.path.abspath('..\PythonResults')
if not os.path.exists(results):
    os.makedirs(results)

filename = os.path.join(results, '{}.csv'.format(article_id))
df.to_csv(filename, index=False)
print('Save file - {}'.format(filename))
