# coding: utf-8

import urllib
import requests
import json


class WXSDK(object):
    def __init__(self, appid, secret, ):
        self.appid = appid
        self.secret = secret
        self.access_token = None
        self.url_prefix = 'https://api.weixin.qq.com/cgi-bin'
        # surong
        self.access_token = 'zonPuKkPHJxxB50CwtYghZ-FtKrJ8xQXsFHzZmscBsd07DCZqhWSPOKMnH70aWsVS8-qwz4GdqvWlbYYTODBsqQwG4yBQ0oF_381qjEaz0KHFNkIJMcImQNEKq4dOF-TXTLeAHAMIA'
        # guanjia
        # self.access_token = 'eRheQQQqevT0Mv_mGNCQ91HdJQw3it_e50rbaMhwpfL6xfaxGhKSOquhZC93TzW7YIqOJLo1gw-5x4GkBGkOfzYy4EZev0h2mQqGkMux_FxYH2eU_s72Xnwkk74yk9JWSUZjABADFK'
        # gongyu
        #self.access_token = 'bOzcUhPeMfPCnrpDPQuHYk59rjzQnkJS9RH0zAAI12G6fP-l0bCYylvF9bkaZj3xpeIIoJP80pQkVrRvZZAipoqzrq_jcrtGWhsnJRjEIR8HJNfAAAVXB'

    def get_url(self, path):
        if path == '/token':
            return '%s%s' % (self.url_prefix, path)
        return '%s%s?access_token=%s' % (self.url_prefix, path, self.access_token)

    def send(self, path, params=None, method='GET'):
        url = self.get_url(path)
        if method == 'GET':
            resp = requests.get(url, params)
        else:
            resp = requests.post(url, data=params)
        resp_data = resp.json()

        logstr = u'send_request: url=%s %s=%s resp_code=%s resp_text:%s' % (
            url, method, params, resp.status_code, resp.text)
        print logstr
        print json.dumps(resp_data, ensure_ascii=False, indent=4)
        return True, resp_data

    def get_access_token(self):
        path = '/token'
        params = {
            'grant_type': 'client_credential',
            'appid': self.appid,
            'secret': self.secret,
        }
        return self.send(path, params)

    def menu_get(self):
        path = '/menu/get'
        return self.send(path)

    def menu_create(self):
        path = '/menu/create'
        params = {
            "button": [
                {
                    "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxf806b49682664d9d&redirect_uri=http%3A%2F%2Ffdwx.h2ome.cn%2Ffdoauth2%3Fpub%3D96228f7a356a11e7890300163e0013dd&response_type=code&scope=snsapi_userinfo&state=bills#wechat_redirect",
                    "type": "view",
                    "name": "交 租"
                },
                {
                    "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxf806b49682664d9d&redirect_uri=http%3A%2F%2Ffdwx.h2ome.cn%2Ffdoauth2%3Fpub%3D96228f7a356a11e7890300163e0013dd&response_type=code&scope=snsapi_userinfo&state=user#wechat_redirect",
                    "type": "view",
                    "name": "用户中心"
                }
            ]
        }
        # params = json.dumps(params)
        return self.send(path, params, method='POST')

    def get_current_selfmenu_info(self):
        path = '/get_current_selfmenu_info'
        return self.send(path)


if __name__ == '__main__':
    # guanjia
    #appid, secret = 'wxed1a36ce3fa969f5', 'bb3830caf045ab10c9c2c902f1751252'
    # gongyu
    # appid, secret = 'wxbdea7c5cd9da4138', 'f08fd722917158e8a0bdc308f5966065'
    # surong
    appid, secret = 'wxf806b49682664d9d', '64e2a599d54afc4d821e58e35e54600c'
    sdk = WXSDK(appid, secret)
    #sdk.get_access_token()
    # sdk.menu_get()
    # sdk.menu_create()
    sdk.get_current_selfmenu_info()
