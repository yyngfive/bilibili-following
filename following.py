import logs
import requests
import json
from typing import List
import time
import random
log = logs.get_logger(__name__)


class Following():

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/ 537.36 Edg/107.0.1418.62'}

    miss = []    

    def get_mid(self, session: requests.Session) -> int:
        try:
            res = session.get(url='https://api.bilibili.com/nav',
                          headers=self.headers)
            res = json.loads(res.text)
            data = res['data']
        except Exception as e:
            log.error('201:获取登录用户UID失败')
            log.debug(e)
            exit(-201)
        return data['mid']

    def get_total_follow(self,session: requests.Session) -> int:
        try:
            mid = self.get_mid(session)
            res = session.get(url='https://api.bilibili.com/x/relation/followings',
                            headers=self.headers, params={'vmid': mid})
            data = json.loads(res.text)['data']
        except Exception as e:
            log.error('202:获取关注总数失败')
            log.debug(e)
            exit(-202)
        return data['total']

    def get_follow_list(self,session: requests.Session, page: int = 1) -> List[dict]:
        mid = self.get_mid(session)
        try:
            res = session.get(url='https://api.bilibili.com/x/relation/followings',
                          headers=self.headers,
                          params={'vmid': mid, 'pn': page, 'ps': 50})
            data = json.loads(res.text)['data']
        except Exception as e:
            log.error('203:获取关注列表失败')
            log.debug(e)
            exit(-203)
        return data['list']
    
    def get_fans(self,mid: int) -> int:
        try:
            res = requests.get(url='https://api.bilibili.com/x/relation/stat',
                        headers=self.headers, params={'vmid': mid})
            res = json.loads(res.text)
            data = res['data']
        except Exception as e:
            log.error(f'204:获取UP主：{mid}粉丝数失败')
            log.debug(e)
            exit(-204)
        return data['follower']
    
    def get_up_stat(self,session: requests.Session, mid: int) -> dict:
        info = {}
        try:
            res = session.get(url='https://api.bilibili.com/x/space/upstat',
                            headers=self.headers, params={'mid': mid})
            res = json.loads(res.text)
            data = res['data']
            view = data['archive']['view']
            likes = data['likes']
        except Exception as e:
            log.error(f'205:获取UP主：{mid}总览信息失败')
            log.debug(e)
            exit(-205)
        info['view'] = view
        info['likes'] = likes
        return info
    
    def get_up_videos(self,mid: int) -> dict:
        for _ in range(5):
            res = requests.get(url='http://api.bilibili.com/x/space/arc/search',
                            headers=self.headers, params={'mid': mid, 'pn': 1, 'ps': 1})
            res = json.loads(res.text)
            
            code = res['code']
            
            if code == 0:
                data = res['data']
                break
            else:
                log.info((code,res['message']))
            time.sleep(random.randint(1, 3))
        try:
            total = data['page']['count']
        except:
            log.warning(f'206:获取UP主:{mid}视频信息失败')
            total = 0

        if total != 0:
            fields = data['list']['tlist']
            fields_count = {value['name']: value['count']
                            for value in fields.values()}
            newest = data['list']['vlist'][0]['created']
            newest = time.strftime('%Y-%m-%d', time.localtime(newest))
            page = total // 51 + 1
            for _ in range(5):
                res = requests.get(url='http://api.bilibili.com/x/space/arc/search',
                                headers=self.headers, params={'mid': mid, 'pn': page, 'ps': 50})
                res = json.loads(res.text)
                code = res['code']
                if code == 0:
                    break
                else:
                    log.info((code,res['message']))
                time.sleep(random.randint(1, 3))
            try:
                data = res['data']
                oldest = data['list']['vlist'][-1]['created']
                oldest = time.strftime('%Y-%m-%d', time.localtime(oldest))
            except:
                log.warning(f'207：获取UP主：{mid}最早视频信息失败')
                oldest = '1970-1-1'
                self.miss.append(mid)
        else:
            self.miss.append(mid)
            fields_count = {'无': 0}
            newest = '1970-1-1'
            oldest = '1970-1-1'

        info = {
            'total': total,
            'fields_count': fields_count,
            'newest': newest,
            'oldest': oldest
        }
        return info
