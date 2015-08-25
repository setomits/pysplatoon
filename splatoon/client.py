#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import pickle

import requests
from pyquery import PyQuery

class Client:
    def __init__(self, username, password = '', lang = 'ja-JP'):
        self.username = username
        self.password = password if password else ''
        self.lang = lang if lang else 'ja-JP'
        self.cookies = None
        self.loggingin = False

        self._cookies_path = './cookies/%s' % self.username


    def _login_params(self):
        r = requests.get("https://splatoon.nintendo.net/users/auth/nintendo")
        doc = PyQuery(r.content)

        params = dict(
            client_id = '',
            state = '',
            redirect_uri = '',
            response_type = 'code',
        )

        for ele in doc('input'):
            if ele.name in params:
                params[ele.name] = ele.value

        params['lang'] = self.lang
        params['username'] = self.username
        params['password'] = self.password
        params['rememberMe'] = 'on'
        params['nintendo_authenticate'] = ''
        params['nintendo_authorize'] = ''
        params['scope']  = ''

        self.cookies = r.cookies

        return params

    def _has_cookies(self):
        return os.path.exists(self._cookies_path)

    def _save_cookies(self, cookies):
        with open(self._cookies_path, 'wb') as f:
            pickle.dump(dict(cookies), f)

        self.cookies = cookies
        
    def _load_cookies(self):
        with open(self._cookies_path, "rb") as f:
            d = pickle.load(f)
            self.cookies = requests.utils.cookiejar_from_dict(d)
            self.loggingin = True

    def login(self, password = '', force = False):
        if password:
            self.password = password
        else:
            if self.password:
                pass
            else:
                raise UnboundLocalError('password is not set')

        if force and self._has_cookies():
            os.remove("./cookies/%s" % self.username)

        if self._has_cookies():
            self._load_cookies()
        else:
            params = self._login_params()

            r = requests.post('https://id.nintendo.net/oauth/authorize',
                              data = params,
                              cookies = self.cookies)

            if r.url == 'https://id.nintendo.net/oauth/authorize':
                raise RuntimeError('unauthorized')
            else:
                self._save_cookies(r.cookies)
                self.loggingin = True

    def current_stages(self):
        d = dict(
            regular_stages = [],
            earnest_rule = '',
            earnest_stages = []
        )

        if not self.loggingin:
            self.login()

        r = requests.get('https://splatoon.nintendo.net/schedule',
                         cookies = self.cookies)

        doc = PyQuery(r.text)

        map_names = doc('span.map-name')
        if map_names:
            d['regular'] = [mn.text for mn in map_names[0:2]]
            d['earnest'] = [mn.text for mn in map_names[2:4]]
            d['earnest_rule'] = doc('span.rule-description')[0].text


        return d

    def friend_list(self):
        if not self.loggingin:
            self.login()


        r = requests.get('https://splatoon.nintendo.net/friend_list/index.json',
                         cookies = self.cookies)

        return r.json()

