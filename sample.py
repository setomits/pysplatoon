#!/usr/bin/env python
# -*- coding: utf-8 -*-

from splatoon import Client

def _main():
    c = Client('YOUR_USER_NAME', 'YOUR_PASSWORD')
    c.login()

    stages = c.current_stages()
    print('# Regular Stages')
    for s in stages['regular']:
        print('*', s)
    print()

    print('# Earnest Stages:', stages['earnest_rule'])
    for s in stages['earnest']:
        print('*', s)
    print()

    friends = c.friend_list()
    print('# Friends online')
    for f in friends:
        print('##', f['mii_name'])
        print('* mode:', f['mode'])


if __name__ == '__main__':
    _main()
