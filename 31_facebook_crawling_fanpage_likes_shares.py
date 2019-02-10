import os
import requests
import pandas as pd

from datetime import datetime

# 透過 Graph API 觀察文章 ID 與 token
fanpage_id = '136845026417486'
token = ''

url = 'https://graph.facebook.com/v2.11/{}/posts?fields={}&access_token={}'.format(
    fanpage_id, 'id,created_time,name,likes.limit(0).summary(true),shares,message', token
)

posts = []
pages = 0

while True:
    resp = requests.get(url)
    data = resp.json()
    posts += data['data']
    pages += 1
    
    if 'next' not in data['paging']:
        print('EOF')
        break
        
    else:
        url = data['paging']['next']
        print('page {}'.format(pages))

posts_summary = []
for post in posts:
    p = {}
    for k, v in post.items():
        if k == 'likes' and 'summary' in v and 'total_count' in v['summary']:
            p['total_likes'] = v['summary']['total_count']
        elif k == 'shares' and 'count' in v:
            p['total_shares'] = v['count']
        else:
            p[k] = v
    posts_summary.append(p)

df = pd.DataFrame.from_records(posts_summary)
df.head()


results = os.path.abspath('../results')
if not os.path.exists(results):
    os.makedirs(results)
    
filename = os.path.join(results, 'fanpage_{}.csv'.format(fanpage_id))
df.to_csv(filename, index=False)
print('Save file - {}'.format(filename))