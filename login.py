import requests
import json
from typing import Tuple
import qrcode

class Login():
    
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/ 537.36 Edg/107.0.1418.62'}
    
    def __init__(self):
        ...

    def apply_QR_code(self) -> Tuple[str,str]:
        res = requests.get(url='https://passport.bilibili.com/x/passport-login/web/qrcode/generate',headers=self.headers)
        res = json.loads(res.text)
        data = res['data']
        return data['url'],data['qrcode_key']

    def generate_QR_code(self,qrcode_url:str) -> None:
        qr = qrcode.QRCode()
        qr.add_data(qrcode_url)
        qr.print_ascii(invert=True)

    def do_web_login(self,session,token:str)-> int:
        params = {'qrcode_key':token}
        res = session.get(url='https://passport.bilibili.com/x/passport-login/web/qrcode/poll',params=params,headers=self.headers)
        res = json.loads(res.text)
        data = res['data']
        return data['code']

if __name__ == '__main__':
    login = Login()
    url,token = login.apply_QR_code()
    login.generate_QR_code(url)
    input('已扫码')
    bilibili_session = requests.Session()
    code = login.do_web_login(bilibili_session,token)
    if code == 0:
        print('登录成功')
    elif code == 86038:
        print('二维码失效')
    elif code == 86090 or code == 86101:
        print('请扫码并确认')
    else:
        print(f'错误，code:{code}')
    