# -*- coding: utf-8 -*-
import scrapy
from zhihu.items import ZhihuItem
from scrapy import Request
import http.cookiejar
import urllib
import ssl
#from zhihu import settings


class ZhSpider(scrapy.Spider):
    name = 'zh'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/']
    #cookie = settings['COOKIE']  # 带着Cookie向网页发请求
    cookie = http.cookiejar.CookieJar()

    headers = {
        'Connection': 'keep - alive',  # 保持链接状态
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }
    # 对请求的返回进行处理的配置
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }

    def login(self, login_url):
        login_data = {'username': '13910116476', 'password': 'ioReid0406', }
        postdata = bytes(urllib.parse.urlencode(login_data), "utf8")
        ssl._create_default_https_context = ssl._create_unverified_context
        handler = urllib.request.HTTPCookieProcessor(self.cookie)
        opener = urllib.request.build_opener(handler)
        rst = opener.open(login_url, postdata)
        print(rst.read())

    # 爬虫的起点,当然头信息，伪装ip在别的地方设置也行
    def start_requests(self):
        self.login("https://www.zhihu.com/signin?next=%2F")
        yield Request(self.start_urls[0], callback=self.parse, cookies=self.cookie,
                      headers=self.headers, meta=self.meta)

    def parse(self, response):
        item = ZhihuItem()
        print(response)
        item["title"] = response.xpath("//meta[@itemprop='name']/@content").extract()
        item["content"] = response.xpath("//span[@itemprop='text']/text()").extract()
        item["link"] = response.xpath("//a[@data-za-detail-view-id='3942']/@href").extract()
        #item["like"] = response.xpath("//button[@class='Button VoteButton VoteButton--up']/text()").extract()
        #item["dislike"] = response.xpath("//button[@class='Button VoteButton VoteButton--down']/text()/").extract()
        #item["comment"] = response.xpath("//button[@]class='Button ContentItem-action Button--plain Button--withIcon Button--withLabe']/text()").extract()
        print(item['title'],item['content'])
        #yield item
        '''
        for i in range(2, 101):
            url = "http://category.dangdang.com/pg" + str(i) + "-cp01.54.06.00.00.00.html"
            yield Request(url, callback=self.parse)
        '''