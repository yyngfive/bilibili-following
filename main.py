import requests
from login import Login
from following import Following
import logs
import pandas as pd
import numpy
from tqdm import tqdm
import time
import random
import json
import extension
import os
log = logs.get_logger(__name__)
# Login
login = Login()
bilibili_session = requests.Session()
login.login(bilibili_session)

# Following
df = pd.DataFrame({'name': [],
                   'uid': [],
                   'time': [],
                   'special': [],
                   'face': [],
                   'fans': [],
                   'total': [],
                   'view': [],
                   'likes': [],
                   'fields': [],
                   'first': [],
                   'newest': []})
following = Following()
log.debug(pd.__version__)
print(f'即将开始获取用户{following.get_mid(bilibili_session)}的关注列表')
log.debug(f'即将开始获取用户{following.get_mid(bilibili_session)}的关注列表')

total = following.get_total_follow(bilibili_session)
print(f'关注总数：{total}')
if os.path.exists('./following.json'):
    print('Woo')
following_list = []
for page in tqdm(range(1, total // 51 + 2)):
    time.sleep(random.randint(1, 3))
    ups = following.get_follow_list(bilibili_session, page)
    log.debug(f'Searching: page {page}, got: {len(ups)}')
    following_list.extend(ups)

print(f'获取到{len(following_list)}份数据')
log.debug(f'获取到{len(following_list)}份数据')

with open('following.json', 'w') as f:
    f.write(json.dumps(following_list))
print('原始数据已写入：following.json')
log.debug('原始数据已写入：following.json')

print('正在获取基本关注数据(当前模式：慢速防封号)')
log.debug('正在获取基本关注数据(当前模式：慢速防封号)')
for data in tqdm(following_list[1:10]):
    time.sleep(random.randint(1, 3))
    mid = data['mid']
    log.debug(f'获取UP主：{mid}的信息')
    upstat = following.get_up_stat(bilibili_session, mid)
    time.sleep(random.randint(1, 3))
    video_info = following.get_up_videos(mid)
    time.sleep(random.randint(1, 3))
    fields_count = video_info['fields_count']
    if len(fields_count) > 1:
        main_fields = sorted(fields_count.items(),
                             key=lambda x: x[1], reverse=True)[0:2]
        first_field = main_fields[0][0]
        if main_fields[1][1] / video_info['total'] >= 0.33:
            second_field = main_fields[1][0]
        else:
            second_field = ''
    else:
        first_field = sorted(fields_count.items(),
                             key=lambda x: x[1], reverse=True)[0][0]
        second_field = ''
    if second_field != '':
        fields = first_field+','+second_field
    else:
        fields = first_field
    info = {
        'name': data['uname'],
        'uid': mid,
        'time': time.strftime('%Y-%m-%d', time.localtime(data['mtime'])),
        'special': '否' if data['special'] == 0 else '是',
        'face': data['face'],
        'fans': following.get_fans(mid),
        'total': video_info['total'],
        'view': upstat['view'],
        'likes': upstat['likes'],
        'fields': fields,
        'first': video_info['oldest'],
        'newest': video_info['newest']
    }

    df.loc[len(df.index)] = info.values()

miss = len(set(following.miss))
log.debug(set(following.miss))
if miss != 0:
    print(f'有{miss}个UP主的信息未能成功获取')
    miss_list = set(following.miss)
    print(f'他们是{miss_list}')
    
print('基础数据获取完成，已保存到following.csv，正在计算拓展数据')
df.to_csv('following.csv', encoding='utf-8',index=False)
log.debug('基础数据获取完成，已保存到following.csv，正在计算拓展数据')

extensions = pd.DataFrame({
    'update':extension.ext_update(df['newest'].tolist()),
    'single_field':extension.ext_single_field(df['fields'].tolist()),
    'big_field':extension.ext_big_field(df['fields'].tolist()),
    'fans_level':extension.ext_fans_level(df['fans'].tolist())
})

extensions['view_average'] = df['view']/df['total']
extensions['view_average'].replace([numpy.inf],0,inplace=True)
extensions['view_average']=extensions['view_average'].round()
extensions['likes_average'] = df['likes']/df['total']
extensions['likes_average'].replace([numpy.inf],0,inplace=True)
extensions['likes_average']=extensions['likes_average'].round()

df['uid'] = df['uid'].astype(str)

df_new = pd.concat([df, extensions], axis=1)
df_new.to_excel('following-ups.xlsx',index=False)
df_new.to_csv('following-ups.csv', encoding='utf-8',index=False)
print('拓展数据计算完成，结果保存到following-ups.csv')
log.debug('拓展数据计算完成，结果保存到following-ups.csv')
