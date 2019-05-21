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

import csv
csv_file = open('jd_crawler_res.csv', 'w', newline='')
first_line = ['标题', '作者', '图片链接', '评论数', '好评率', '价格']
csv_writer =  csv.writer(csv_file)
csv_writer.writerow(first_line)

for i in range(1,101):
    print("-----第"+str(i)+"页商品-----")
    url="https://search.jd.com/Search?keyword="+key+"&enc=utf-8&page="+str(i+1)
    ua(uapools)
    data=urllib.request.urlopen(url).read().decode("utf-8","ignore")

    #拿到item id 列表
    item_id_pat = '<li data-sku="(.*?)" class="gl-item">'
    item_ids = re.compile(item_id_pat, re.S).findall(data)
    #print(item_ids)
    for skuid in item_ids:

        id_url="https://item.jd.com/"+str(skuid)+".html"
        print(id_url)
        time.sleep(8)
        try:
            item_data = urllib.request.urlopen(id_url).read().decode("gbk","ignore")
        except Exception as e:
            # 出现问题后打印log，继续爬
            print(e)
            continue

        #我们的目标是：标题，作者，评论数，好评度，图片link，价格，但是好评度，价格，评论数都是动态加载，因此我们这里只能分析js获得
        #comment_pat = '<a class="count J-comm-'+item_id+'" href="#none">(.*?)</a>'
        #price_pat = '<strong class="p-price" id="jd-price">(.*?)</strong>'
        #pic_pat = '<img data-img="1" width="350" height="350" src="//(.*?)" alt="'

        ## 标题
        title_pat = '<title>(.*?)【摘要 书评 试读】- 京东图书</title>'
        title = re.compile(title_pat,re.S).findall(item_data)
        if len(title) > 0:
            title = title[0]
            print(title)

        ## 试一下通过js的正则来获得name
        '''
        name_pat = 'name: \'(.*?)\','
        names = re.compile(name_pat, re.S).findall(item_data)
        name = ''
        if len(names) >0:
            name = names[0].encode('utf-8').decode('unicode_escape')
            print(name)
        '''
        ## 作者
        author_pat = 'authors: [(.*?)],'
        authors = re.compile(author_pat, re.S).findall(item_data)
        author = ''
        if len(authors) > 0 :
            author = authors[0]
        else:
            ## 可以从title里面获取
            rindex = title.rfind(')')
            lindex = title.rfind('(')
            if rindex >0 and lindex >0:
                author = title[lindex+1:rindex]
        print("作者是： %s" % (author))
        ## 京东屏蔽了这部分，经过分析，这部分是通过js 来实现的
        ## 比如下面的回调获得，我们只要拿到skuId, 在这里就是productId
        ## https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv7&productId=25700505099&score=0&sortType=5&isShadowSku=0&page=0&pageSize=10
        time.sleep(5)
        import json
        import jsonpath
        callback_url = "https://sclub.jd.com/comment/productCommentSummaries.action?referenceIds="+str(skuid)
        comment_response = urllib.request.urlopen(callback_url).read().decode("gbk","ignore")
        len_body = len(comment_response)
        comment_count = ''
        good_rate = ''
        if len_body >0:
            comment_json = json.loads(comment_response)
            #print(comment_json)
            comment_count = str(jsonpath.jsonpath(comment_json, '$..CommentCount')[0])
            good_rate = str(jsonpath.jsonpath(comment_json, '$..GoodRateShow')[0])
            print("好评度： %s" %(good_rate))
            print("商品评价： %s" %(comment_count))


        #comments = re.compile(comment_pat, re.S).findall(item_data)
        #if len(comments) >0 :
        #    comment = comments[0]
        #    print(comment)

        ## 京东屏蔽了这部分，需要看一下代码才能解码
        ## https://p.3.cn/prices/mgets?skuIds=J_25700505099
        time.sleep(5)
        price_url = "https://p.3.cn/prices/mgets?skuIds=J_"+str(skuid)
        price_response = urllib.request.urlopen(price_url).read().decode("gbk","ignore")
        price = ''
        if len(price_response) > 0:
            price_json = json.loads(price_response)
            price = price_json[0]['op']
            print("售卖价格： %s" %(price))

        ## 可以尝试爬一下图片的link，或者下载图片？
        image_pat = '<img data-img="1" width="350" height="350" src="//(.*?)" alt="'
        image_links = re.compile(image_pat, re.S).findall(item_data)
        image_link = ''
        if len(image_links) >0:
            image_link = image_links[0]
            print(image_link)

        ## 这部分完成内容存储，这里是准备一个csv格式文件来完成存储
        item_row = [title, author, image_link, comment_count, good_rate, price]
        print(item_row)
        csv_writer.writerow(item_row)
csv_file.close()
