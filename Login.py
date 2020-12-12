# -*- coding: utf-8 -*-
import requests
import re
from urllib.parse import urlparse
import pwden

def GetLoginUrl():  # 获取登陆链接
    apis = {}
    ids = 'ec061503-d0fa-4bbd-9a22-e5eaaccc69e9'
    params = {'ids': ids}
    r = requests.get('https://mobile.campushoy.com/v6/config/guest/tenant/info', params=params)

    old_acw_tc = requests.utils.dict_from_cookiejar(r.cookies)['acw_tc']
    apis['old_acw_tc'] = old_acw_tc
    data = r.json()['data'][0]
    appid = data['appId']
    ampUrl = data['ampUrl']

    if 'campusphere' in ampUrl or 'cpdaily' in ampUrl:
        parse = urlparse(ampUrl)
        apis['host'] = parse.netloc
        res = requests.get(parse.scheme + '://' + parse.netloc, allow_redirects=False)
        acw_tc = requests.utils.dict_from_cookiejar(res.cookies)['acw_tc']
        apis['acw_tc'] = acw_tc

        header = {'Cookie': 'acw_tc=' + acw_tc}
        apis['acw_url'] = parse.scheme + '://' + parse.netloc + '/portal/login'
        res = requests.get(apis['acw_url'], headers=header)
        apis['login-url'] = res.url
        apis['data'] = {'appid': appid, 'login_type': 'mobileLogin'}

    ampUrl2 = data['ampUrl2']
    if 'campusphere' in ampUrl2 or 'cpdaily' in ampUrl2:
        parse = urlparse(ampUrl2)
        apis['host'] = parse.netloc
        res = requests.get(parse.scheme + '://' + parse.netloc, allow_redirects=False)
        acw_tc = requests.utils.dict_from_cookiejar(res.cookies)['acw_tc']
        apis['acw_tc'] = acw_tc

        header = {'Cookie': 'acw_tc=' + acw_tc}
        apis['acw_url'] = parse.scheme + '://' + parse.netloc + '/portal/login'
        res = requests.get(apis['acw_url'], headers=header)
        apis['login-url'] = res.url
        apis['data'] = {'appid': appid, 'login_type': 'mobileLogin'}
    return apis


def Login(apis, account):
    url = apis['login-url']

    r = requests.get(url)

    cookie = requests.utils.dict_from_cookiejar(r.cookies)
    JSESSIONID = cookie['JSESSIONID']
    route = cookie['route']

    cookie = 'route=' + route + '; JSESSIONID=' + JSESSIONID + '; org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=zh_CN'
    header = {'Cookie': cookie}

    r = requests.post(url, headers=header)

    lt = re.findall('name="lt" value="(.*)"', r.text)[0]
    key = re.findall('id="pwdDefaultEncryptSalt" value="(.*?)"', r.text)[0]
    dllt = re.findall('name="dllt" value="(.*)"', r.text)[0]
    execution = re.findall('name="execution" value="(.*?)"', r.text)[0]
    rmShown = re.findall('name="rmShown" value="(.*?)"', r.text)[0]

    header = {
        'Cookie': cookie
    }
    pwd = pwden.AESEncrypt(account['password'], key)
    data = {
        'username': account['userId'],
        'password': pwd,
        'lt': lt,
        'dllt': dllt,
        'execution': execution,
        '_eventId': 'submit',
        'rmShown': rmShown
    }

    r = requests.post(url, headers=header, data=data, allow_redirects=False)

    response_headers = r.headers
    Location = response_headers['Location']
    # ticket = re.findall('(?<==).*', Location)[0]

    # payload = {'ticket': ticket}
    # r = requests.get(apis['acw_url'], params=payload, allow_redirects=False)
    # acw_tc = requests.utils.dict_from_cookiejar(r.cookies)['acw_tc']
    #
    key = {}
    r = requests.get(url=Location)
    for i in r.history:
        key.update(requests.utils.dict_from_cookiejar(i.cookies))

    return key


def GetCookie(account):
    apis = GetLoginUrl()
    key = Login(apis, account)
    return key


if __name__ == '__main__':
    userId = ''  # 你的学号
    password = ''  # 你的密码
    GetCookie({'userId': userId, 'password': password})
