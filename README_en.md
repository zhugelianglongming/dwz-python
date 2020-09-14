# dwz-python

This repo demonstrate how to use [API](https://dwz.cn/console/apidoc/v3) for DWZ in Python.

* [Token](https://console.bce.baidu.com/dwz/#/dwz/token) is required.

## Normal user
```python
from dwz import Dwz

dwz = Dwz("token")

# create short URL (dwz.cn) for multi long URLs with 1 year validity
long_urls = ["https://www.baidu.com/1","https://www.baidu.com/2"]
results = dwz.create(long_urls, "1-year")
# create short URL (dwz.cn) for single long URLs with long-term validity
short_url = dwz.create_single("https://www.baidu.com/3", "long-term")

# query origin long URL for 'https://dwz.cn/shortPath'
long_url = dwz.query("https://dwz.cn/shortPath")

# delete 'https://dwz.cn/shortPath'
dwz.delete("https://dwz.cn/shortPath")
```
## Custom domain user
You can apply a custom domain by submitting a [ticket](https://ticket.bce.baidu.com/#/ticket/create~productId=188&questionId=706&channel=2),
BTW not free~
```python
from dwz import Dwz

# a custom domain as 'custom.dwz.cn'
dwz = Dwz("token", "custom.dwz.cn")

# create short URL (custom.dwz.cn) for multi long URLs with 1 year validity
long_urls = ["https://www.baidu.com/1","https://www.baidu.com/2"]
results = dwz.create(long_urls, "long-term")
# create short URL (custom.dwz.cn) for single long URLs with long-term validity
short_url = dwz.create_single("https://www.baidu.com/3", "long-term")

# query origin long URL for 'https://custom.dwz.cn/shortPath'
long_url = dwz.query("https://custom.dwz.cn/shortPath")

# delete 'https://custom.dwz.cn/shortPath'
dwz.delete("https://custom.dwz.cn/shortPath")
```