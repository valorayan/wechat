# coding:utf-8
from . import api
from flask import request, abort
from project.utils.wechat import WeChat


@api.route('/index', methods=['GET', 'POST'])
def index():
    wechat = WeChat()
    if request.method == 'GET':
        return wechat.valid()
    else:
        wechat.create_menu()

        # wechat.response_msg()
        # access_token = wechat.get_access_token()
        # print(access_token)



