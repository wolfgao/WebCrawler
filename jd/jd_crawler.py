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
    url="https://search.jd.com/Search?keyword="+key+"&enc=utf-8&page="+str(i+1)
    ua(uapools)
    data=urllib.request.urlopen(url).read().decode("utf-8","ignore")

    #拿到item id 列表
    item_id_pat = '<li data-sku="(.*?)" class="gl-item">'
    item_ids = re.compile(item_id_pat, re.S).findall(data)
    print(item_ids)
    for item_id in item_ids:
        id_url="https://item.jd.com/"+item_id+".html"
        print(id_url)
        item_data = urllib.request.urlopen(id_url).read().decode("gbk","ignore")

        title_pat = '<div class="sku-name">(.*?)</div>'
        comment_pat = '<a class="count J-comm-'+item_id+'" href="#none">(.*?)</a>'
        price_pat = '<strong class="p-price" id="jd-price">(.*?)</strong>'

        title = re.compile(title_pat,re.S).findall(item_data)
        if len(title) > 0:
            title = title[0]
            print(title)

        ## TODO：京东屏蔽了这部分，需要看一下js代码才能解开
        comments = re.compile(comment_pat, re.S).findall(item_data)
        if len(comments) >0 :
            comment = comments[0]
            print(comment)
        ## TODO：京东屏蔽了这部分，需要看一下代码才能解码
        price = re.compile(price_pat, re.S).findall(item_data)
        if len(price) > 0:
            price = price[0]
            print(price)

        ## TODO： 可以尝试爬一下图片的link，或者下载图片？

        ## TODO：这部分完成内容存储