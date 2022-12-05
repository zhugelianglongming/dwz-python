# dwz-python

中文 | [English](README_en.md)

本代码库演示了通过 Python 调用百度短网址 [API](https://dwz.cn/console/apidoc/v3) 的方法。

* [Token](https://console.bce.baidu.com/dwz/#/dwz/token) 是必须的鉴权参数。

## 常规用法
```python
import dwz

client = dwz.Dwz("my token")

# 为多条长网址链接创建 1 年有效的短网址 (dwz.cn/xxx)
long_urls = ["https://my.domain/very-long-path", "https://my.domain/?very-long=query"]
results = client.create(long_urls, dwz.TOV.ONE_YEAR)
# 为单条长网址链接创建长期有效的短网址 (dwz.cn/xxx)
short_url = client.create_single("https://my.domain/very-long-suffix", dwz.TOV.LONG_TERM)

# 查询 'https://dwz.cn/shortPath' 对应的长网址链接
long_url = client.query("https://dwz.cn/shortPath")

# 更新短网址：'https://dwz.cn/shortPath' 的目标长网址为 'https://my.domain/new-long-url'
client.update("https://dwz.cn/shortPath", "https://my.domain/new-long-url")

# 删除短网址：'https://dwz.cn/shortPath'
client.delete("https://dwz.cn/shortPath")
```
## 定制域名用法
定制域名目前可通过 [工单](https://ticket.bce.baidu.com/#/ticket/create~productId=188&questionId=706&channel=2) 申请购买
```python
import dwz

# 设置定制域名：'*.dwz.cn'
client = dwz.Dwz("my token", "custom.dwz.cn")

# 为多条长网址链接创建 1 年有效的短网址 (custom.dwz.cn/xxx)
long_urls = ["https://my.domain/very-long-path", "https://my.domain/?very-long=query"]
results = client.create(long_urls, dwz.TOV.ONE_YEAR)
# 为单条长网址链接创建长期有效的短网址 (custom.dwz.cn/xxx)
short_url = client.create_single("https://my.domain/very-long-suffix", dwz.TOV.LONG_TERM)

# 查询 'https://custom.dwz.cn/shortPath' 对应的长网址链接
long_url = client.query("https://custom.dwz.cn/shortPath")

# 更新短网址：'https://custom.dwz.cn/shortPath' 的目标长网址为 'https://my.domain/new-long-url'
client.update("https://custom.dwz.cn/shortPath", "https://my.domain/new-long-url")

# 删除短网址 'https://custom.dwz.cn/shortPath'
client.delete("https://custom.dwz.cn/shortPath")
```