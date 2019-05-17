'''
这个文件主要是用requests库来尝试进行爬虫：如果没有加载，首先需要 pip install requests

请求方式:get、post、put…
参数：params、headers、proxies、cookies、data
-------- request 参数 ----------
params:主要是get的参数，以字典方式存储你
headers：主要是伪装浏览器，以字典方式存储
proxies: 代理设置，比如代理IP
cookies:
data： 主要是post是传入的参数，以字典方式存储
-------- response ------------
下面是response的数据域：
text    响应数据
content  响应数据（b）
encoding  网页编码
cookies   响应cookie
url       当前请求的url
status_code   状态码
'''

import requests
import re

hd={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",}
#px={"http":"http://127.0.0.1:8888"}
rst=requests.get("http://www.aliwx.com.cn/",headers=hd)
title=re.compile("<title>(.*?)</title>",re.S).findall(rst.text)
print(title)

pr={"wd":"阿里文学",}
rst=requests.get("http://www.baidu.com/s",params=pr)
#可以继续对结果进行过滤，挖掘自己想要的信息。
print(rst.url)

#requests支持POST
postdata={"name":"测试账号",
      "pass":"测试密码",
      }
rst=requests.post("http://www.iqianyue.com/mypost/",data=postdata)
print(rst.status_code)