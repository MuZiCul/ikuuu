import requests
import json

from config.config import WECOM_CID, WECOM_AID, WECOM_SECRET, WECOM_TOUID

cookies = {
    'lang': 'zh-cn',
    'uid': '755899',
    'email': '110muzicul110%40gmail.com',
    'key': '75fe857f6fee3f6118b62bd1d508f2d80a632ce155e6d',
    'ip': '9b90675e640e5f5a99aa5d062ec52706',
    'expire_in': '1671454410',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
    'Referer': 'https://ikuuu.co/user',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://ikuuu.co',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Connection': 'keep-alive',
}


def sign_in_iku():
    try:
        response = requests.post('https://ikuuu.co/user/checkin', cookies=cookies, headers=headers,
                                            proxies={'http': f'http://127.0.0.1:11223',
                                                     'https': f'http://127.0.0.1:11223'})
        text = json.loads(response.text)
        if text['ret'] == 0:
            send_to_wecom(text['msg'])
        if text['ret'] == 1:
            send_to_wecom(text['msg'])
    except Exception as e:
        send_to_wecom('流量签到服务器错误：'+str(e))


def send_to_wecom(msg):
    wecom_cid = WECOM_CID
    wecom_aid = WECOM_AID
    wecom_secret = WECOM_SECRET
    wecom_touid = WECOM_TOUID
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url, proxies={'http': f'http://127.0.0.1:11223',
                                                     'https': f'http://127.0.0.1:11223'}).content
    access_token = json.loads(response).get('access_token')
    if access_token and len(access_token) > 0:
        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        data = {
            "touser": wecom_touid,
            "agentid": wecom_aid,
            "msgtype": "text",
            "text": {
                "content": msg
            },
            "duplicate_check_interval": 600
        }
        response = requests.post(send_msg_url, data=json.dumps(data), proxies={'http': f'http://127.0.0.1:11223',
                                                     'https': f'http://127.0.0.1:11223'}).content
        return response
    else:
        return 0
