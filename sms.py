import requests
import time
import random
from urllib.parse import urlencode
from hashlib import md5
from Gorgon import Gorgon
from Argus import Argus
from Ladon import Ladon
from solver import Solver
class TikTokOTP:
    def __init__(self, device_id, iid):
        self.device_id = device_id
        self.iid = iid
        self.host = "api16-normal-useast5.tiktokv.us"
    def xor_mobile(self, mobile: str) -> str:
        return "".join([hex(ord(_) ^ 5)[2:] for _ in mobile])
    def sign_request(self, params: str, payload: str, cookie: str = None):
        unix = int(time.time())
        x_ss_stub = md5(payload.encode('utf-8')).hexdigest()
        
        gorgon_headers = Gorgon(params, unix, payload, cookie).get_value()
        
        signatures = {
            "x-ladon": Ladon.encrypt(unix, 1611921764, 1233),
            "x-argus": Argus.get_sign(
                params, 
                x_ss_stub, 
                unix,
                platform=0,
                aid=1233,
                license_id=1611921764,
                sec_device_id="",
                sdk_version_int=134744640 
            )
        }
        return {**gorgon_headers, **signatures}
    def send_otp(self, phone_number):
        print("[*] Solving Captcha...")
        Solver(self.device_id, self.iid).solve_captcha()
        params = {
            "passport-sdk-version": "1",
            "device_platform": "android",
            "os": "android",
            "ssmix": "a",
            "_rticket": int(time.time() * 1000),
            "channel": "googleplay",
            "aid": "1233",
            "app_name": "musical_ly",
            "version_code": "430603",
            "version_name": "43.6.3",
            "device_type": "SM-S9260",
            "device_brand": "Samsung",
            "language": "en",
            "os_api": "32",
            "os_version": "12",
            "current_region": "DZ",
            "sys_region": "US",
            "ts": int(time.time()),
            "iid": self.iid,
            "device_id": self.device_id
        }
        data = {
            "check_register": "0",
            "query_sms_permission": "1",
            "auto_read": "1",
            "account_sdk_source": "app",
            "mix_mode": "1",
            "mobile": self.xor_mobile(phone_number),
            "type": "3731"
        }
        query_str = urlencode(params)
        payload_str = urlencode(data)
        headers = {
            "host": self.host,
            "sdk-version": "2",
            "passport-sdk-version": "1",
            "x-tt-pba-enable": "1",
            "x-tt-dm-status": "login=1;ct=1;rt=1",
            "x-tt-bypass-dp": "1",
            "user-agent": "com.zhiliaoapp.musically/2024306030 (Linux; U; Android 12; en_US; SM-S9260; Build/V417IR;tt-ok/3.12.13.21)",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

        headers.update(self.sign_request(query_str, payload_str))
        url = f"https://{self.host}/passport/mobile/send_code/v1/"
        try:
            response = requests.post(url, params=params, data=payload_str, headers=headers)
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
if __name__ == "__main__":
    client = TikTokOTP(
        device_id="7590755553484883512", 
        iid="7598953365327316756"
    )
    phone = "0550123456" 
    print(f"[*] Attempting to send OTP to: {phone}")
    result = client.send_otp(phone)
    print(f"[+] Server Response: {result}")