
import base64
import json
import re

import requests
from bs4 import BeautifulSoup
from requests import request

URL_API = '/v2/api'
URL_LOGIN = f'{URL_API}/auth/login'
URL_GRADES = f'{URL_API}/student/all_subjects'

class user():
    def __init__(self, username_: str, password_: str, domain_: str):
        self.cache_dump = {}
        self.protocol = 'https://'
        self.domain = domain_
        self.username = username_
        self.password = password_
        self.cookies = None

    def reqst(self, url, method='POST', data=None, json=None, cache=None, get_cache=None, **kwargs):
        if get_cache is not None and (temp := self.cache_dump.get(get_cache, False)):
            result = temp
        else:
            # print(self.protocol + self.domain + url)
            result = request(method, self.protocol + self.domain + url, json=json, data=data, cookies=self.cookies,
                             allow_redirects=True, **kwargs)

        if result.text.count(f'window.location = "{self.domain}{self.domain}/v2/login";'):
            self.request_cookies()
            return self.reqst(url, method=method, data=data, json=json, cache=cache, get_cache=get_cache, **kwargs)

        try:
            result.json()
        except ValueError:
            pass
        else:
            if isinstance(result.json(), dict):
                if error := result.json().get('error', False):
                    raise Exception(f"{error}: {result.json().get('error', False)}")

        if cache is not None:
            self.cache_dump[cache] = result
        return result

    def request_cookies(self):
        class LoginError(Exception):
            pass

        login_payload = dict(username=self.username, password=self.password)
        login = requests.get(self.protocol + self.domain + URL_LOGIN, json=login_payload, allow_redirects=True, params={"semesterWechsel": 1})
        if 'error' in (data := login.json()).keys() and data['error'] is not None:
            raise LoginError(f"{data['error']}: {data['message']}")
        self.cookies = login.cookies
        
    
    def request_grades(self, **kwargs):
        return self.reqst(URL_GRADES, **kwargs)