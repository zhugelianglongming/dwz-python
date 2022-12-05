# dwz-python

[中文](README.md) | English

This repo demonstrates how to use [API](https://dwz.cn/console/apidoc/v3) for DWZ in Python.

* [Token](https://console.bce.baidu.com/dwz/#/dwz/token) is required.

## Normal user
```python
import dwz

client = dwz.Dwz("my token")

# create short URL (dwz.cn) for multi long URLs with 1 year validity
long_urls = ["https://my.domain/very-long-path", "https://my.domain/?very-long=query"]
results = client.create(long_urls, dwz.TOV.ONE_YEAR)
# create short URL (dwz.cn) for single long URLs with long-term validity
short_url = client.create_single("https://my.domain/very-long-suffix", dwz.TOV.LONG_TERM)

# query target long URL for 'https://dwz.cn/shortPath'
long_url = client.query("https://dwz.cn/shortPath")
long_url = client.query("shortPath")

# update short URL 'https://dwz.cn/shortPath' with target long URL as 'https://my.domain/new-long-url'
client.update("https://dwz.cn/shortPath", "https://my.domain/new-long-url")
client.update("shortPath", "https://my.domain/new-long-url")

# delete 'https://dwz.cn/shortPath'
client.delete("https://dwz.cn/shortPath")
client.delete("shortPath")
```
## Custom domain user
You can apply a custom domain by submitting a [ticket](https://ticket.bce.baidu.com/#/ticket/create~productId=188&questionId=706&channel=2),
BTW not free~
```python
import dwz

# a custom domain as '*.dwz.cn'
client = dwz.Dwz("my token", "custom.dwz.cn")

# create short URL (custom.dwz.cn) for multi long URLs with 1 year validity
long_urls = ["https://my.domain/very-long-path", "https://my.domain/?very-long=query"]
results = client.create(long_urls, dwz.TOV.ONE_YEAR)
# create short URL (custom.dwz.cn) for single long URLs with long-term validity
short_url = client.create_single("https://my.domain/very-long-suffix", dwz.TOV.LONG_TERM)

# query target long URL for 'https://custom.dwz.cn/shortPath'
long_url = client.query("https://custom.dwz.cn/shortPath")
long_url = client.query("shortPath")

# update short URL 'https://custom.dwz.cn/shortPath' with target long URL as 'https://my.domain/new-long-url'
client.update("https://custom.dwz.cn/shortPath", "https://my.domain/new-long-url")
client.update("shortPath", "https://my.domain/new-long-url")

# delete 'https://custom.dwz.cn/shortPath'
client.delete("https://custom.dwz.cn/shortPath")
client.delete("shortPath")
```