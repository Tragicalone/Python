import os
import requests
import pandas as pd
from datetime import datetime

# 透過 Graph API 觀察文章 ID 與 token
article_id = '232633627068_10156769966527069'
token = ''

comments = []
pages = 0

"""
nested query + 游標型分頁
%7B => {
%7D => }
%2C => ,
reference: https://www.w3schools.com/tags/ref_urlencode.asp
"""

base_url = 'https://graph.facebook.com/v2.11/{}'.format(article_id)
query = '?fields=comments.limit({})%7Battachment%2Capplication%2Cmessage.limit({})%7D&access_token={}'.format(
    10, 100, token
)
url = '{}/{}'.format(base_url, query)

while True:
    pages += 1
    resp = requests.get(url)
    data = resp.json()
    if 'comments' not in data:
        break

    comments += data['comments']['data']

    if 'after' not in data['comments']['paging']['cursors']:
        print('EOF')
        break
    else:
        cursors_after = data['comments']['paging']['cursors']['after']
        query = '?fields=comments.limit({}).after({})%7Battachment%2Capplication%2Cmessage.limit({})%7D&access_token={}'.format(
            10, cursors_after, 100, token
        )
        url = '{}/{}'.format(base_url, query)
        print('pages {}'.format(pages))

print('comments length = {}'.format(len(comments)))

for comment in comments:
    application, attachment, message = '', '', ''
    if 'application' in comment:
        app = {'application_{}'.format(k): v for k, v in comment['application'].items()}
        comment.update(app)
        del comment['application']
    if 'attachment' in comment:
        att = {
            'attachment_type': comment['attachment']['type'],
            'attachment_url': comment['attachment']['url']
        }
        comment.update(att)
        del comment['attachment']

df = pd.DataFrame.from_records(comments)
df.head()

results = os.path.abspath('../results')
if not os.path.exists(results):
    os.makedirs(results)

filename = os.path.join(results, '{}.csv'.format(article_id))
df.to_csv(filename, index=False)
print('Save file - {}'.format(filename))
