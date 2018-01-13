#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import http.cookiejar as cookielib
import re

from user import header, log_header, user


def login(s):
    data = {
        'vwriter': user['username'],
        'vpassword': user['password'],
        'rmflag': '1',
        'fowardURL': '',
        'from': '',
    }
    s.get(url='http://passport.tianya.cn/', headers=header, timeout=30)
    html1 = s.post(url='https://passport.tianya.cn/login', data=data, headers=log_header)
    p1 = re.compile(r'location\.href="(.*)"')
    link = p1.findall(html1.content.decode())[0]
    html = s.get(url=link, headers=header, timeout=30)
    print(html.content.decode())
    p2 = re.compile(r'<script type="text/javascript" src="(.*)"></script>')
    links = p2.findall(html.content.decode())
    p3 = re.compile(r"js\.src = '(.*)';")
    link = p3.findall(html.content.decode())[0]
    for each in links:
        s.get(url=each, headers=header, timeout=30)
    s.get(url='http://passport.tianya.cn/' + link, headers=header, timeout=30)
    s.cookies.save()
    return 0


def islogin(s):
    html = s.get(url='http://bbs.tianya.cn/api?method=bbs.api.getUserTotalArticleList&params%5BpageSize%5D=45', headers=header, timeout=30)
    print(eval(html.content.decode())['message'])
    return 0


if __name__ == '__main__':
    session = requests.session()
    session.cookies = cookielib.LWPCookieJar(filename='cookies')
    # noinspection PyBroadException
    try:
        session.cookies.load(ignore_discard=True)
        islogin(session)
    except Exception:
        print('cookies load fail')
        login(session)
        islogin(session)
