import urllib.request
import re
import random
keyname="女装"
key=urllib.request.quote(keyname)
uapools=[
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    ]

def ua(uapools):
    thisua=random.choice(uapools)
    print(thisua)
    headers=("User-Agent",thisua)
    opener=urllib.request.build_opener()
    opener.addheaders=[headers]
    #安装为全局
    urllib.request.install_opener(opener)
for i in range(1,101):
    print("-----第"+str(i)+"页商品-----")
    url="https://s.taobao.com/search?q="+key+"&s="+str((i-1)*44)
    ua(uapools)
    data=urllib.request.urlopen(url).read().decode("utf-8","ignore")
    pat='"nid":"(.*?)"'
    idlist=re.compile(pat,re.S).findall(data)
    for j in range(0,len(idlist)):
        thisid=idlist[j]
        thisurl="https://item.taobao.com/item.htm?id="+str(thisid)
        itemdata=urllib.request.urlopen(thisurl).read().decode("gbk","ignore")
        titlepat='<h3 class="tb-main-title" data-title="(.*?)"'
        detailpat='<p class="tb-subtitle">(.*?)</p>'
        pricepat='<em class="tb-rmb-num">(.*?)</em>'
        title=re.compile(titlepat,re.S).findall(itemdata)
        if(len(title)>0):
            title=title[0]
        else:
            continue
        detail=re.compile(detailpat,re.S).findall(itemdata)
        if(len(detail)>0):
            detail=detail[0]
        else:
            detail=0
        price=re.compile(pricepat,re.S).findall(itemdata)
        if(len(price)>0):
            price=price[0]
        else:
            price=0
        commenturl="https://rate.taobao.com/detailCount.do?_ksTS=1523812034136_172&callback=jsonp173&itemId="+str(thisid)
        commentdata=urllib.request.urlopen(commenturl).read().decode("utf-8","ignore")
        countpat='{"count":(.*?)}'
        count=re.compile(countpat,re.S).findall(commentdata)
        if(len(count)>0):
            count=count[0]
        else:
            count=0
        print("--------------")
        print("商品名:"+str(title))
        print("描述信息:"+str(detail))
        print("价格:"+str(price))
        print("评论数:"+str(count))
