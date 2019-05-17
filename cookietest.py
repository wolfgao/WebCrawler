import http.cookiejar
import urllib
import ssl


cookie=http.cookiejar.CookieJar()
handler=urllib.request.HTTPCookieProcessor(cookie)
opener=urllib.request.build_opener(handler)
#知乎网站
data={'username':'13910116476','password':'ioReid0406',}
data=urllib.parse.urlencode(data)

postdata=bytes(data, encoding="utf8")

ssl._create_default_https_context = ssl._create_unverified_context
request=opener.open("https://www.zhihu.com",postdata)

print(cookie)
print(request.read())
