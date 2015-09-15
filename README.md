# What is this?

This is a Python client library to get Splatoon data like online friends, stages and so on.
Only latest Python is supported.


# How to Use

```
>>> from splatoon import Client
>>> c = Client('YOUR_USER_NAME', 'YOUR_PASSWORD')
>>> c.login()

>>> current = c.current_stages()
>>> for stage in current['stages']['regurar']
...   print(stage)
>>> for stage in current['stages']['gachi']
...   print(stage)
>>> print(current['gachi_rule'])

>>> friends = c.fliend_list()
>>> for friend in friends:
...   print(friend['mii_name'], ':', friend['mode'])

>>> ranking = c.ranking()
>>> for friend in ranking['regular']:
...   print(friend['rank'], friend['mii_name'], friend['score'])
>>> for friend in ranking['gachi']:
...   print(friend['rank'], friend['mii_name'], friend['score'])
```
