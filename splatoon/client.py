#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import pickle
import tempfile

import requests
from pyquery import PyQuery

SPL_ROOT = 'https://splatoon.nintendo.net'

class Client:
    def __init__(self, username, password = '', lang = 'ja-JP'):
        self.username = username
        self.password = password if password else ''
        self.lang = lang if lang else 'ja-JP'
        self.cookies = None
        self.loggingin = False

        cookies_dir = '%s/pysplatoon' % tempfile.gettempdir()
        if not os.path.exists(cookies_dir):
            os.makedirs(cookies_dir)

        self._cookies_path = '%s/%s' % (cookies_dir, self.username)

    def _login_params(self):
        r = requests.get(SPL_ROOT + "/users/auth/nintendo")
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

    def friend_list(self):
        if not self.loggingin:
            self.login()

        r = requests.get(SPL_ROOT + '/friend_list/index.json',
                         cookies = self.cookies)

        return r.json()

    def ranking(self):
        if not self.loggingin:
            self.login()


        r = requests.get(SPL_ROOT + '/ranking/index.json',
                         cookies = self.cookies)

        dat = r.json()

        for k in dat.keys():
            for i, friend in enumerate(dat[k]):
                dat[k][i]['score'] = int(''.join(friend['score']))
                dat[k][i]['rank'] = int(''.join(friend['rank']))

        return dat

    def current_stages(self):
        d = dict(
            regular = [],
            gachi_rule = '',
            gachi = []
        )

        if not self.loggingin:
            self.login()

        r = requests.get(SPL_ROOT + '/schedule', cookies = self.cookies)

        doc = PyQuery(r.text)

        names = doc('span.map-name')
        images = doc('span.map-image')

        if names and images:
            for i in range(4):
                if i < 2:
                    d['regular'].append(dict(
                        name = names[i].text,
                        image = images[i].attrib['data-retina-image'],
                    ))
                else:
                    d['gachi'].append(dict(
                        name = names[i].text,
                        image = SPL_ROOT + images[i].attrib['data-retina-image'],
                    ))

            d['gachi_rule'] = doc('span.rule-description')[0].text

        return d

