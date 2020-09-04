# dwz-python

This repo demostrate how to use [API](https://dwz.cn/console/apidoc/v3) for DWZ in Python.

[Token](https://console.bce.baidu.com/dwz/#/dwz/token) is required.
it's not suggest to implement API in your front-end code, which may lead to leaking token.

## Normal user
```python
from dwz import Dwz

dwz = Dwz("token")

# create short URL (dwz.cn) for 2 long URLs with 1 year validity
long_urls = ["https://www.baidu.com/1","https://www.baidu.com/2"]
result = dwz.create(long_urls, "1-year")

# query origin long URL for 'https://dwz.cn/shortPath'
result = dwz.query("shortPath")

# delete 'https://dwz.cn/shortPath'
result = dwz.delete("shortPath")
```
## Custom domain user
```python
from dwz import Dwz

dwz = Dwz("token", "custom.dwz.cn")

# create short URL (custom.dwz.cn) for 2 long URLs with 1 year validity
long_urls = ["https://www.baidu.com/1","https://www.baidu.com/2"]
result = dwz.create(long_urls, "1-year")

# query origin long URL for 'https://custom.dwz.cn/shortPath'
result = dwz.query("shortPath")

# delete 'https://custom.dwz.cn/shortPath'
result = dwz.delete("shortPath")
```