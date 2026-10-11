import requests
import time
from hashlib import md5
from urllib.parse import urlencode

from Gorgon import Gorgon
from Argus import Argus
from Ladon import Ladon


# ================= SIGN =================
def sign(params, payload: str = None, sec_device_id: str = "", cookie: str = None,
         aid: int = 1233, license_id: int = 1611921764,
         sdk_version_str: str = "v05.00.00-android",
         sdk_version: int = 167000000,
         platform: int = 0, unix: int = None):

    if not unix:
        unix = int(time.time())

    x_ss_stub = md5(payload.encode()).hexdigest() if payload else None

    return Gorgon(params, unix, payload, cookie).get_value() | {
        "x-ladon": Ladon.encrypt(unix, license_id, aid),
        "x-argus": Argus.get_sign(
            params, x_ss_stub, unix,
            platform=platform,
            aid=aid,
            license_id=license_id,
            sec_device_id=sec_device_id,
            sdk_version=sdk_version_str,
            sdk_version_int=sdk_version
        )
    }


# ================= PARAMS =================
def base_params():
    ts = int(time.time())
    return {
        "aweme_id": awid,
        "type": "1",
        "channel_id": "3",
        "enter_from": "others_homepage",

        "iid": iid,
        "device_id": did,

        "ac": "wifi",
        "aid": "1233",
        "app_name": "musical_ly",
        "channel": "googleplay",

        "version_code": "430104",
        "version_name": "43.1.4",
        "build_number": "43.1.4",
        "manifest_version_code": "2024301040",
        "update_version_code": "2024301040",
        "ab_version": "43.1.4",

        "device_platform": "android",
        "os": "android",
        "os_api": "33",
        "os_version": "13",

        "device_type": "SM-S911B",
        "device_brand": "samsung",

        "resolution": "1080*2340",
        "dpi": "420",
        "language": "en",
        "locale": "en",
        "region": "DZ",
        "sys_region": "DZ",
        "op_region": "DZ",
        "current_region": "DZ",
        "timezone_name": "Africa/Algiers",
        "timezone_offset": "3600",

        "host_abi": "arm64-v8a",
        "ssmix": "a",
        "is_pad": "0",
        "app_type": "normal",
        "content_language": "en,ar",

        "ts": str(ts),
        "_rticket": str(ts * 1000),
    }


# ================= DATA =================
def build_payload():
    return urlencode({
        "aweme_id": awid,
        "type": "1"
    })


# ================= SESSION DATA =================
cook = "PASTE_VALID_COOKIE_HERE"

iid = "7389856192924976902"
did = "7389854904419223045"
awid = "7348952636785167621"

url = "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/commit/item/digg/"

payload = build_payload()
params = urlencode(base_params())
sign_headers = sign(params, payload, cookie=cook)


# ================= HEADERS =================
headers = {
    "User-Agent": (
        "com.zhiliaoapp.musically/2024301040 "
        "(Linux; U; Android 13; en; SM-S911B; "
        "Build/TP1A.220624.014; "
        "Cronet/TTNetVersion:7b46c09c 2024-10-01 "
        "QuicVersion:4d7a2a12 2024-09-18)"
    ),
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",

    "x-ss-req-ticket": str(int(time.time() * 1000)),
    "x-ss-dp": "1233",

    "passport-sdk-version": "6030000",
    "tt-ticket-guard-version": "3",

    "x-tt-dm-status": "login=1;ct=1;rt=1",
    "x-tt-store-region": "dz",
    "x-tt-store-region-src": "uid",

    "x-gorgon": sign_headers["x-gorgon"],
    "x-khronos": sign_headers["x-khronos"],
    "x-argus": sign_headers["x-argus"],
    "x-ladon": sign_headers["x-ladon"],

    "Cookie": cook
}


# ================= REQUEST =================
response = requests.post(
    url,
    params=base_params(),
    data=payload,
    headers=headers,
    timeout=10
)

print(response.text)
