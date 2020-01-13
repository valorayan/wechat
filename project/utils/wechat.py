# coding:utf-8
from project import constant, redis_store
from flask import request, abort, current_app
import hashlib, urllib, json, xmltodict
import requests as req


class WeChat(object):
    def __init__(self):
        self.token = constant.WECHAT_TOKEN
        self.appid = constant.WECHAT_APPID
        self.appsecret = constant.WECHAT_APPSECRET

    def valid(self):
        """get方法，校验微信"""
        echostr = request.args.get('echostr')
        if not echostr:
            abort(403)
        if self.check_signature():
            return echostr

    def check_signature(self):
        """校验配置微信"""
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        if not all(['signature', 'timestamp', 'nonce']):
            return False
        tmp_list = [self.token, timestamp, nonce]
        tmp_list.sort()
        tmp_list = "".join(tmp_list)
        s1 = hashlib.sha1()
        s1.update(tmp_list.encode())
        sign = s1.hexdigest()
        if signature != sign:
            return False
        return True

    def get_access_token(self):
        """获取access_token"""
        try:
            access_token = redis_store.get('wx_access_token')
        except Exception as e:
            current_app.logger.error(e)
        if access_token is not None:
            return access_token
        url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
            self.appid, self.appsecret)
        resp = urllib.request.urlopen(url)
        response = resp.read().decode()
        url_resp = json.loads(response)
        print(url_resp)
        if 'errcode' in url_resp:
            current_app.logger.error('获取token失败')
            abort(400)
        access_token = url_resp.get('access_token')
        try:
            redis_store.setex('wx_access_token', constant.ACCESS_TOKEN_EXPIRED, access_token)
        except Exception as e:
            current_app.logger.error(e)
        return access_token

    def response_msg(self):
        """微信消息处理方法"""
        xml_str = request.data
        data = xmltodict.parse(xml_str)
        data = data['xml']
        if data.get('MsgType') == 'text':
            result = {
                'xml': {
                    'ToUserName': data['FromUserName'],
                    'FromUserName': data['ToUserName'],
                    'CreateTime': time.time(),
                    'MsgType': 'text',
                    'Content': data.get('Content'),
                }
            }
            result = xmltodict.unparse(result)
            return result
        else:
            pass

    def create_menu(self):
        """创建菜单"""
        #  https://api.weixin.qq.com/cgi-bin/menu/create?access_token=ACCESS_TOKEN
        url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % self.get_access_token()
        data = {
            "button": [
                {
                    "type": "click",
                    "name": "今日歌曲",
                    "key": "V1001_TODAY_MUSIC"
                },
                {
                    "name": "菜单",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "搜索",
                            "url": "http://www.soso.com/"
                        },
                        {
                            "type": "miniprogram",
                            "name": "wxa",
                            "url": "http://mp.weixin.qq.com",
                            "appid": "wx286b93c14bbf93aa",
                            "pagepath": "pages/lunar/index"
                        },
                        {
                            "type": "click",
                            "name": "赞一下我们",
                            "key": "V1001_GOOD"
                        }]
                }]
        }
        resp = req.post(url, data=data)
        resp = resp.text()
        print(resp)
