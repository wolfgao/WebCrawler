class transCookie:
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict

if __name__ == "__main__":
    cookie = '_zap=7f331506-02e4-43c0-a865-3cf076a8a73d; _xsrf=KzTzHJ2jz3MhcJiaeS9QGMaU6YExKj7u; d_c0="AEBlX07aOQ-PTs9x0wPSoIEoxOz6Dy_A8fg=|1554360470"; __gads=ID=9d158b6c7f04b8e1:T=1554360931:S=ALNI_MYcqCkLtaW7lNYz-vcgmyqoFCo8rQ; __utmv=51854390.100--|2=registration_date=20170620=1^3=entry_date=20170620=1; _ga=GA1.2.1783837872.1556267738; q_c1=e196828ffd264bb7aee43e1fffeecbe1|1557141126000|1554360487000; tst=r; __utma=51854390.1783837872.1556267738.1556267738.1557141336.2; __utmc=51854390; __utmz=51854390.1557141336.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; tgw_l7_route=116a747939468d99065d12a386ab1c5f; capsion_ticket="2|1:0|10:1557303050|14:capsion_ticket|44:NmRjYTcwMDQ3NmFkNGMyZmJkMDA5ZDI1NGNjOGM0ODI=|2f2e59b931772c810ed5de7536ffafb098d7deaa7d4551b7e1c33cf26a610151"; z_c0="2|1:0|10:1557303057|4:z_c0|92:Mi4xTXhVX0JRQUFBQUFBUUdWZlR0bzVEeVlBQUFCZ0FsVk5FZDJfWFFBbk40S1BELW5VMmJoQlFMTVAySjV0c2ZDOXdn|5bf15c597e808d3c474aa8bcc1c5d227880b9fa98975a32bf3ea713049430248"'
    trans = transCookie(cookie)
    print(trans.stringToDict())