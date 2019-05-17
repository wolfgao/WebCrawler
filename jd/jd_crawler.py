import urllib.request
import re
import http.cookiejar
import random
import ssl

keyname="绘本"
key=urllib.request.quote(keyname)
uapools=[
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    ]

cjar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
ssl._create_default_https_context = ssl._create_unverified_context

def ua(uapools):
    thisua=random.choice(uapools)
    #print(thisua)
    headers=("User-Agent",thisua)
    #opener=urllib.request.build_opener()
    opener.addheaders=[headers]
    #安装为全局
    urllib.request.install_opener(opener)

for i in range(1,101):
    print("-----第"+str(i)+"页商品-----")
    url="https://s.taobao.com/Search?keyword="+key+"&enc=utf-8&page="+str(i+1)
    ua(uapools)
    data=urllib.request.urlopen(url).read().decode("utf-8","ignore")

    #开始过滤
    #拿到书名
    item_id_pat = '<strong class="J_(.*?)" data-done'
    item_id = re.compile(item_id_pat, re.S).findall(data)
    id_url="https://item.jd.com/"+item_id+".html"
    print(id_url)
    item_data = urllib.request.urlopen(id_url).read().decode("utf-8","ignore")

    title_pat='<div class="sku-name">(.*?)</div>'
    comment_pat='<a class="count J-comm-25700505099" href="#none">400+</a>'



    title_link = re.compile(title_link_pat,re.S).findall(data)
    print(title_link)

    #TODO：拿到价格

    #TODO：拿到评论数

    #TODO：存储到一个csv文件中
