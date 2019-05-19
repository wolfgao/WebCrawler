import urllib.request
import re
import http.cookiejar
import random
import ssl
import time
from selenium import webdriver

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
        #comment_pat = '<a class="count J-comm-'+item_id+'" href="#none">(.*?)</a>'
        price_pat = '<strong class="p-price" id="jd-price">(.*?)</strong>'
        pic_pat = '<img data-img="1" width="350" height="350" src="//(.*?)" alt="'
        title = re.compile(title_pat,re.S).findall(item_data)
        if len(title) > 0:
            title = title[0]
            print(title)

        ## 京东屏蔽了这部分，经过分析，这部分是通过js 来实现的
        ## 比如下面的回调获得，我们只要拿到skuId, 在这里就是productId
        ## https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv7&productId=25700505099&score=0&sortType=5&isShadowSku=0&page=0&pageSize=10

        import json
        callback_url = "https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv7&productId="\
                       +str(item_id)+"&score=0&sortType=5&isShadowSku=0&page=0&pageSize=10"
        comment_response = urllib.request.urlopen(callback_url).read().decode("gbk","ignore")
        len_start = len("fetchJSON_comment98vv7(")
        # 最后一个字符是')'，也要干掉
        len_body = len(comment_response)

        if len_body >0:
            comment_json = json.loads(comment_response[len_start:len_body-2])
            print(comment_json)
            print("好评度： %s" %(comment_json['productCommentSummary']['goodRateShow']))
            print("商品评价： %s" %(comment_json['productCommentSummary']['commentCountStr']))


        #comments = re.compile(comment_pat, re.S).findall(item_data)
        #if len(comments) >0 :
        #    comment = comments[0]
        #    print(comment)

        ## 京东屏蔽了这部分，需要看一下代码才能解码
        ## https://p.3.cn/prices/mgets?skuIds=J_25700505099

        price_url = "https://p.3.cn/prices/mgets?skuIds=J_"+str(item_id)
        price_response = urllib.request.urlopen(price_url).read().decode("gbk","ignore")
        if len(price_response) > 0:
            price = json.loads(price_response)
            print(price[0]['op'])

        ## 可以尝试爬一下图片的link，或者下载图片？
        image_pat = '<img data-img="1" width="350" height="350" src="//(.*?)" alt="'
        image_links = re.compile(image_pat, re.S).findall(item_data)
        if len(image_links) >0:
            image_link = image_links[0]
            print(image_link)

        ## TODO：这部分完成内容存储