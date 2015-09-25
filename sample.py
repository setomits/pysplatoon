#!/usr/bin/env python
# -*- coding: utf-8 -*-

from splatoon import Client

def _main():
    c = Client('YOUR_USER_NAME', 'YOUR_PASSWORD')
    c.login()

    current = c.current_stages()
    print('# Regular Stages')
    for stage in current['stages']['regular']:
        print('*', stage)
    print()

    print('# Gachi Stages:', current['gachi_rule'])
    for stage in current['stages']['gachi']:
        print('*', stage)
    print()

    friends = c.friend_list()
    print('# Friends online')
    for f in friends:
        print('##', f['mii_name'])
        print('* mode:', f['mode'])


if __name__ == '__main__':
    _main()
