import urllib.request
import re
import http.cookiejar
import random
import ssl
import time

import redis as redis
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

import csv
csv_file = open('jd_crawler_res_p18.csv', 'w', newline='')
first_line = ['SkuId', '标题', '作者', '图片链接', '评论数', '好评率', '价格']
csv_writer =  csv.writer(csv_file)
csv_writer.writerow(first_line)

## 通过redis来去重
rconn = redis.Redis("127.0.0.1", "6379")

for i in range(36,200, 2):
    print("-----第"+str(i//2)+"页商品-----")
    url="https://search.jd.com/Search?keyword="+key+"&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page="+str(i)+"&suggest=1.his.0.0&psort=3&s=61&click=0"
    "https://search.jd.com/Search?keyword=%E7%BB%98%E6%9C%AC&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.his.0.0&psort=3&page=13&s=361&click=0"
    ua(uapools)
    data=urllib.request.urlopen(url).read().decode("utf-8","ignore")

    #拿到item id 列表
    item_id_pat = '<li data-sku="(.*?)" class="gl-item">'
    item_ids = re.compile(item_id_pat, re.S).findall(data)
    #print(item_ids)
    for skuid in item_ids:

        ## TODO：这里要想办法去重，可以用redis或者mysql来去重，如果ID存在，就跳过，否则才进行爬虫
        isdo = rconn.hget("skuid", str(skuid))
        if (isdo != None):
            print("这个商品- %s 已经爬过了，因此跳过" %(skuid))
            continue
        rconn.hset("skuid", str(skuid), "1")

        id_url="https://item.jd.com/"+str(skuid)+".html"
        print(id_url)

        # 我们的目标是：SKUID, 标题，作者，评论数，好评度，图片link，价格，但是好评度，价格，评论数都是动态加载，因此我们这里只能分析js获得
        title = ''
        author = ''
        image_link = ''
        comment_count = ''
        good_rate = ''
        price = ''
        try:
            item_data = urllib.request.urlopen(id_url).read().decode("gbk","ignore")
            time.sleep(8)
            ## 标题
            title_pat = '<title>(.*?)【摘要 书评 试读】- 京东图书</title>'
            title = re.compile(title_pat,re.S).findall(item_data)
            if len(title) > 0:
                title = title[0]
                #print(title)

            ## 作者
            author_pat = 'authors: [(.*?)],'
            authors = re.compile(author_pat, re.S).findall(item_data)
            if len(authors) > 0 :
                author = authors[0]
            else:
                ## 可以从title里面获取
                rindex = title.rfind(')')
                lindex = title.rfind('(')
                if rindex >0 and lindex >0:
                    author = title[lindex+1:rindex]
            #print("作者是： %s" % (author))

            ## 图片的link
            image_pat = '<img data-img="1" width="350" height="350" src="//(.*?)" alt="'
            image_links = re.compile(image_pat, re.S).findall(item_data)
            if len(image_links) > 0:
                image_link = image_links[0]
                #print(image_link)
        except Exception as e:
            # 出现问题后打印log，继续爬
            print("出问题的item链接 %s" %(id_url))
            print(e)
            continue

        ## 京东屏蔽了评论和价格，经过对js的分析是动态加载来实现的
        ## 比如下面的回调获得，我们只要拿到skuId, 在这里就是productId
        ## https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv7&productId=25700505099&score=0&sortType=5&isShadowSku=0&page=0&pageSize=10
        time.sleep(5)
        import json
        import jsonpath
        callback_url = "https://sclub.jd.com/comment/productCommentSummaries.action?referenceIds=" + str(skuid)
        try:
            comment_response = urllib.request.urlopen(callback_url).read().decode("gbk","ignore")
            len_body = len(comment_response)

            if len_body >0:
                comment_json = json.loads(comment_response)
                #print(comment_json)
                comment_count = str(jsonpath.jsonpath(comment_json, '$..CommentCount')[0])
                good_rate = str(jsonpath.jsonpath(comment_json, '$..GoodRateShow')[0])
                #print("好评度： %s" %(good_rate))
                #print("商品评价： %s" %(comment_count))
        except Exception as e:
            print(callback_url)
            print(e)
            continue

        ## 京东屏蔽了这部分，需要看一下代码才能解码
        ## https://p.3.cn/prices/mgets?skuIds=J_25700505099
        time.sleep(5)
        price_url = "https://p.3.cn/prices/mgets?skuIds=J_"+str(skuid)
        try:
            price_response = urllib.request.urlopen(price_url).read().decode("gbk","ignore")
            if len(price_response) > 0:
                price_json = json.loads(price_response)
                price = price_json[0]['op']
                #print("售卖价格： %s" %(price))
        except Exception as e:
            print(price_url)
            print(e)
            continue

        ## 这部分完成内容存储，这里是准备一个csv格式文件来完成存储
        item_row = [skuid, title, author, image_link, comment_count, good_rate, price]
        print(item_row)
        csv_writer.writerow(item_row)
csv_file.close()
