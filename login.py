import requests
import json
from typing import Tuple
import qrcode
import logs

log = logs.get_logger(__name__)
class Login():   
    
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/ 537.36 Edg/107.0.1418.62'}
    
    def __init__(self):
        ...
    def apply_QR_code(self) -> Tuple[str,str]:
        try:
            res = requests.get(url='https://passport.bilibili.com/x/passport-login/web/qrcode/generate',headers=self.headers)
            res = json.loads(res.text)
            data = res['data']
            log.debug(data)
            url = data['url']
            token = data['qrcode_key']
        except Exception as e:
            log.error("101:申请登录二维码失败")
            log.debug(e)
            exit(-101)
        return url, token
    
    def generate_QR_code(self,qrcode_url:str) -> None:
        qr = qrcode.QRCode()
        qr.add_data(qrcode_url)
        qr.print_ascii(invert=True)
        img = qr.make_image()
        img.show()
        
    def do_web_login(self,session,token:str)-> int:
        params = {'qrcode_key':token}
        try:
            res = session.get(url='https://passport.bilibili.com/x/passport-login/web/qrcode/poll',params=params,headers=self.headers)
            res = json.loads(res.text)
            data = res['data']
            code = data['code']
        except Exception as e:
            log.error("102:登陆失败")
            log.debug(e)
            exit(-102)
        return code
    
    def login(self,session):
        url, token = self.apply_QR_code()
        print('扫码后关闭图片')
        self.generate_QR_code(url)
        while True:
            input('已扫码？按任意键确认：')
            code = self.do_web_login(session, token)
            if code == 0:
                print('登录成功')
                log.debug('100:登陆成功')
                break
            elif code == 86038:
                print('二维码失效，请重试')
                log.info('103:二维码失效，请重试')
                exit(-103)
            elif code in (86090,86101):
                print('请扫码并确认')
                log.debug('105:请扫码并确认')
            else:
                log.error(f'104:登录错误，code:{code}')
                exit(-104)

    