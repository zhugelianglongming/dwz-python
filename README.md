# dwz-python

本代码库演示了通过 Python 调用百度短网址 [API](https://dwz.cn/console/apidoc/v3) 的方法。

* [Token](https://console.bce.baidu.com/dwz/#/dwz/token) 是必须的鉴权参数。

## 常规用法
```python
from dwz import Dwz

dwz = Dwz("token")

# 为多条长网址链接创建 1 年有效的短网址 (dwz.cn/xxx)
long_urls = ["https://www.baidu.com/1","https://www.baidu.com/2"]
results = dwz.create(long_urls, "1-year")
# 为单条长网址链接创建长期有效的短网址 (dwz.cn/xxx)
short_url = dwz.create_single("https://www.baidu.com/3", "long-term")

# 查询 'https://dwz.cn/shortPath' 对应的长网址链接
long_url = dwz.query("https://dwz.cn/shortPath")

# 删除短网址：'https://dwz.cn/shortPath'
dwz.delete("https://dwz.cn/shortPath")
```
## 定制域名用法
定制域名目前可通过 [工单](https://ticket.bce.baidu.com/#/ticket/create~productId=188&questionId=706&channel=2) 申请购买
```python
from dwz import Dwz

# 假设定制域名为 'custom.dwz.cn'
dwz = Dwz("token", "custom.dwz.cn")

# 为多条长网址链接创建 1 年有效的短网址 (custom.dwz.cn/xxx)
long_urls = ["https://www.baidu.com/1","https://www.baidu.com/2"]
results = dwz.create(long_urls, "1-year")
# 为单条长网址链接创建长期有效的短网址 (custom.dwz.cn/xxx)
short_url = dwz.create_single("https://www.baidu.com/3", "long-term")

# 查询 'https://custom.dwz.cn/shortPath' 对应的长网址链接
long_url = dwz.query("https://custom.dwz.cn/shortPath")

# 删除短网址 'https://custom.dwz.cn/shortPath'
dwz.delete("https://custom.dwz.cn/shortPath")
```