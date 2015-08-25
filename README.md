# What is this?

This is a Python client library to get Splatoon data like online friends, stages and so on.
Only latest Python is supported.


# How to Use

```
>>> from splatoon import Client
>>> c = Client('YOUR_USER_NAME', 'YOUR_PASSWORD')
>>> c.login()

>>> stages = c.current_stages()
>>> for stage in stages['regurar']
...   print(stage)
>>> for stage in stages['earnest']
...   print(stage)
>>> print(stages['earnest_rule'])

>>> friends = c.fliend_list()
>>> for friend in friends:
...   print(friend['mii_name'], ':', friend['mode'])

>>> ranking = c.ranking()
>>> for friend in ranking['regular']:
...   print(friend['rank'], friend['mii_name'], friend['score'])
>>> for friend in ranking['gachi']:
...   print(friend['rank'], friend['mii_name'], friend['score'])
```
