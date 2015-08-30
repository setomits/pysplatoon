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
            os.remove(self._cookies_path)

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

    def schedule(self):
        if not self.loggingin:
            self.login()

        r = requests.get(SPL_ROOT + '/schedule', cookies = self.cookies)

        doc = PyQuery(r.text)

        spans = doc('span.stage-schedule')
        r_names = doc('div.stage-list:even span.map-name')
        r_imgs = doc('div.stage-list:even span.map-image')
        g_names = doc('div.stage-list:odd span.map-name')
        g_imgs = doc('div.stage-list:odd span.map-image')
        g_rules = doc('div.stage-list:odd span.rule-description')

        stages = []

        if spans:
            for i in range(len(spans)):
                stages.append(
                    dict(
                        span = spans.eq(i).text(),
                        stages = dict(
                            regular = [
                                dict(name = r_names.eq(2*i).text(),
                                     image = SPL_ROOT + \
                                     r_imgs.eq(2*i).attr('data-retina-image')),
                                dict(name = r_names.eq(2*i+1).text(),
                                     image = SPL_ROOT + \
                                     r_imgs.eq(2*i+1).attr('data-retina-image')),
                            ],
                            gachi = [
                                dict(name = g_names.eq(2*i).text(),
                                     image = SPL_ROOT + \
                                     g_imgs.eq(2*i).attr('data-retina-image')),
                                dict(name = g_names.eq(2*i+1).text(),
                                     image = SPL_ROOT + \
                                     g_imgs.eq(2*i+1).attr('data-retina-image')),
                            ]),
                        gachi_rule = g_rules.eq(i).text()
                    ))

        return stages


    def current_stages(self):
        _stages = self.schedule()
        if len(_stages):
            return _stages[0]
        else:
            return {}

