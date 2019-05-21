# 网络爬虫演练项目

## 正则表达式
正则表达式是一个必须掌握的硬指标，因为爬来的东西要过滤自己想要的东西就要大量的文字处理。

## xpath

这里给出XPath表达式的例子及对应的含义:

```
/html/head/title: 选择HTML文档中 <head> 标签内的 <title> 元素
/html/head/title/text(): 选择上面提到的 <title> 元素的文字
//td: 选择所有的 <td> 元素
//div[@class="mine"]: 选择所有具有 class="mine" 属性的 div 元素
```
上边仅仅是几个简单的XPath例子，XPath实际上要比这远远强大的多。 如果您想了解的更多，我们推荐 通过这些例子来学习XPath, 以及 这篇教程学习”how to think in XPath”.



## 建立爬虫项目，开干

### 浏览器伪装，IP代理
很多服务器有很多反爬虫措施，比如检查你的UA，还有是否相同的IP地址在短时间频繁请求。

### 网站分析：
2个抓包工具的学习：fiddler和Charles。
Fiddler主要是Windows下面的工具，Charles是MacOS下的工具（需要付费）。
其实工作原理是一样的，都是通过代理机制，浏览器把他们作为http访问的代理服务器，他们来截取上传和下行的数据，然后进行解析。
可能对Https的代理需要配置一下，就是一个certificate的事情，把他们的根证书安装到你的浏览器上，这样从这个浏览器上进行https的访问也会被截取和破解。

### 确定目标网站要爬的东西:
调取源码进行分VIM析，尤其是html标记，才能形成正确的正则表达式。

### 确定爬虫的库：urllib，requests 和Scrapy，搭建爬虫框架
这三种库都可以用来进行爬虫，要根据目标网站的实际情况选择合适的爬虫库，搭建合适的爬虫库.
本项目将分别用这三种库来进行爬虫实验和demo。

### 关于scrapy，中文教材可参见：
https://scrapy-chs.readthedocs.io/zh_CN/1.0/intro/tutorial.html

- 安装依赖库：
```bash
pip install wheel
pip install lxml
```

- 创建爬虫项目：
参考文献： https://scrapy-chs.readthedocs.io/zh_CN/1.0/intro/tutorial.html

创建一个Scrapy项目
在开始爬取之前，您必须创建一个新的Scrapy项目。 进入您打算存储代码的目录中，运行下列命令:
`scrapy startproject tutorial`

定义提取的Item
Item 是保存爬取到的数据的容器；其使用方法和python字典类似。虽然您也可以在Scrapy中直接使用dict，但是 Item 提供了额外保护机制来避免拼写
错误导致的未定义字段错误。
```python
import scrapy

class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
```

编写爬取网站的 spider 并提取 Item
- Spider是用户编写用于从单个网站(或者一些网站)爬取数据的类。
其包含了一个用于下载的初始URL，如何跟进网页中的链接以及如何分析页面中的内容， 提取生成 item 的方法。

- 为了创建一个Spider，您必须继承 scrapy.Spider 类， 且定义一些属性:

- name: 用于区别Spider。 该名字必须是唯一的，您不可以为不同的Spider设定相同的名字。
start_urls: 包含了Spider在启动时进行爬取的url列表。 因此，第一个被获取到的页面将是其中之一。 后续的URL则从初始的URL获取到的数据中提取。
parse() 是spider的一个方法。 被调用时，每个初始URL完成下载后生成的 Response 对象将会作为唯一的参数传递给该函数。 该方法负责解析返回的数据(response data)，提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象。

- parse这部分可以通过xpath和正则表达式来进行提取元素
xpath(): 传入xpath表达式，返回该表达式所对应的所有节点的selector list列表 。
css(): 传入CSS表达式，返回该表达式所对应的所有节点的selector list列表.
extract(): 序列化该节点为unicode字符串并返回list。
re(): 根据传入的正则表达式对数据进行提取，返回unicode字符串list列表。

编写 Item Pipeline 来存储提取到的Item(即数据)：
- Item 对象是自定义的python字典。 您可以使用标准的字典语法来获取到其每个字段的值。(字段即是我们之前用Field赋值的属性):
```python
import DmozItem
item = DmozItem()
item['title'] = 'Example title'
```
- 最简单存储爬取的数据的方式是使用 Feed exports:
```bash
scrapy crawl dmoz -o items.json
```
- 如果需要对爬取到的item做更多更为复杂的操作，您可以编写 Item Pipeline 。 
类似于我们在创建项目时对Item做的，用于您编写自己的 tutorial/pipelines.py 也被创建。 不过如果您仅仅想要保存item，您不需要实现任何的pipeline。

### 分布式爬虫架构，多台服务器并行爬
这个主要有几个技术难点：
- 1） 如何部署分布式爬虫代码：可以通过docker的方式来布置不同的容器来实现分布式爬虫，当然也可以直接用不同的服务器，主要是解决通信问题。
- 2）如何完成通信，也有几种解决办法：
    - 2.1 通过中央服务器来控制，比如在中央服务器通过redis数据库来进行判断，是否该链接已经爬过，如果爬过，就跳过；否则就爬，并标记出来
    - 2.2 直接分不同的任务到各个分布式服务器，每个服务器干不同任务，已经分好，开始爬。
    - 2.3 还有一种是，这两种方式结合起来爬。


### 设计存储结构，对爬下来的内容如何存储？
- 存在数据库中，比如mysql，但是数据库的读写开销大，效率不快，这个用于重要数据的存储，另外数据字节小的情况
- 可以存储成文件，比如视频，图片；
- 也可以进行高级缓存，比如redis等高效数据库中。

### 一些坑：
1. 有时候会自己中断，我建议都搞一下try... except 在except里面继续continue，忽略错误，除非程序有结构性错误，必须改。
2. js的request经常要有些随机数，这些随机数也是经过一堆运算获得，如果不能搞定这个就不能构造一个合法的请求，也就不能拿到你想要的数据，因此需要有
很强的js基础，jQuery的基础。
3. csv的读写基础要牢固一些，如果加上Python的数据处理库，比如padas，或者platlib等一些统计学，AI的库，可以继续进行数据处理，这部分看你的需求。
4. 请求不能在短时间过于频繁，否则会出各种各样的错误，都是一些网络错误，也无从下手去修改，因此加一下sleep就会好一些，如果sleep的是一个随机数，也会好一些，真正模拟用户的请求。
5. 监控自己爬虫CPU和内存不能太高，如果太高有可能会被系统干掉，因此在程序里面也要注意这部分，在读写大块的json，或者大量的字符串处理，这方面的技巧要注意一下。

以上，暂时这么多，有问题可以欢迎讨论，如果有更好的建议，也请一并提出。

