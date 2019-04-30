import urllib
import urllib.request
import ssl
import random
import re


UAs=[
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
]


webURLs=["http://www.jd.com",
         "http://www.baidu.com"]

## 浏览器伪装，模拟是一个正常的浏览器发出的请求
def UA():
    opener = urllib.request.build_opener()
    thisua = random.choice(UAs)
    ua=("User-Agent", thisua)
    opener.addheaders = [ua]
    urllib.request.install_opener(opener)
    print("当前使用的UA是：%s" %thisua)

def urlCrawler(url):
    UA()
    ssl._create_default_https_context = ssl._create_unverified_context
    #data = urllib.request.urlopen(random.choice(webURLs)).read(100).decode("utf-8", "ignore")
    try:
        data=urllib.request.urlopen(url).read().decode("utf-8", "ignore")
        print(len(data))
        link_pat="<div class=\"article-item clearfix\">[\s\S].*?[\s\S]target=\"_blank\">"
        links = re.compile(link_pat, re.S).findall(data)
        title_pat = "<p class=\"text-ellipsis-one article-title\">.*?</p>"
        titles =  re.compile(title_pat, re.S).findall(data)
        content_pat = "<div class=\"article-summary text-ellipsis\">.*?</div>"
        contents = re.compile(content_pat, re.S).findall(data)

        link_before="<a href=\""
        link_after=" target=\""
        link_before_len=len(link_before)

        title_before="article-title\">"
        title_after="</p>"
        title_before_len=len(title_before)

        cont_before="text-ellipsis\">"
        cont_after="</div>"
        cont_before_len=len(cont_before)

        for j in range(0, len(links)):
            link_start_i=links[j].index(link_before)
            link_stop_i=links[j].index(link_after)
            links[j]=links[j][(link_start_i+link_before_len):(link_stop_i-1)] #前面有一个空格

            title_start_i=titles[j].index(title_before)
            title_stop_i=titles[j].index(title_after)
            titles[j]=titles[j][(title_start_i+title_before_len):title_stop_i]

            cont_start_i=contents[j].index(cont_before)
            cont_stop_i=contents[j].index(cont_after)
            contents[j]=contents[j][(cont_start_i+cont_before_len):cont_stop_i]

            print(links[j])
            print(titles[j])
            print(contents[j])
            print("-------")
    except Exception as err:
        pass


if __name__ == '__main__':
    url="https://www.iqianyue.com/"
    urlCrawler(url)