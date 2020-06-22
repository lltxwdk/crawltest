import urllib.request
import urllib.parse
import urllib.robotparser
import re
import time
import datetime
import requests



class Throttle:

    def __init__(self, delay):
        # 访问同域名时需要的间隔时间
        self.delay = delay
        # key:netloc,value:lastTime.记录每个域名的上一次访问的时间戳
        self.domains = {}

    # 计算需要的等待时间，并执行等待
    def wait(self, url):
        if self.delay <= 0:
            print('delay ='+self.delay)
            return

        domain = urllib.parse.urlparse(url).netloc
        lastTime = self.domains.get(domain)

        if lastTime is not None:
            # 计算等待时间
            wait_sec = self.delay - (datetime.datetime.now() - lastTime).seconds
            if wait_sec > 0:
                time.sleep(wait_sec)

        self.domains[domain] = datetime.datetime.now()


def download(url, headers={}, retryCount=5):
    """
    下载函数
    :param url: 下载的链接
    :param headers: 伪造头
    :param retryCount: 在遇到服务器错误时重复的次数
    :return: 返回页面数据
    """
    print('download to '+ url)
    request =urllib.request.Request(url)

    try:
        response = urllib.request.urlopen(request)
    except urllib.request.URLError as e:
        if hasattr(e, 'code') and 500 <= e.code < 600:
            return download(url, headers, retryCount-1)
        return None
    return response.read()


def get_link(html):
    """
    利用正则获取页面中的所有链接
    :param html: 网页页面数据
    :return: 返回链接
    """
    # webpage_regex = re.compile('<a href="(.*?)">', re.IGNORECASE)
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)


def link_spider(start_link, crawl_link, maxDepth=10):
    """
    链接爬虫
    :param start_link: 开始链接
    :param crawl_link: 需要匹配的链接数据
    :return:
    """
    # 等待下载的链接
    wait_download_link = set([start_link])
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(start_link)
    # 解析链接
    urlObj = urllib.parse.urlparse(start_link)
    # 过滤掉重复的连接
    downloaded_link = {}
    t = Throttle(0.5)
    # 循环下载链接
    while wait_download_link:
        # 从连接列表中取出一个链接
        url = wait_download_link.pop()
        t.wait(url)
        # 下载链接的页面内容
        html = download(url)
        if html is None:
            continue
        # 获取当前页面的深度
        depth = downloaded_link.get(url)
        if depth == None:
            downloaded_link[url] = 1
            depth = 1
        if depth > maxDepth:
            print('max depth')
            continue
        # 得到页面中的所有链接
        all_link = get_link(html.decode(errors='ignore'))
        for link in all_link:
            if re.match(crawl_link, link):
                realLink = urlObj.scheme + '://' + urlObj.netloc + link
                # print(realLink)
                if realLink not in downloaded_link:
                    wait_download_link.add(realLink)
                    downloaded_link[realLink] = depth + 1



#链接的正则表达式，注意是在标签中的href属性里的才是真正的链接
PATTERN_URl = "<a.*href=\"(https?://.*?)[\"|\'].*"
 
#获取网页源代码，注意使用requests时访问https会有SSL验证，需要在get方法时关闭验证
def getHtml(url):
    res = requests.get(url,verify=False)
    text = res.text
    return text
#有时还是会有警告，可以采用以下方式禁用警告
#import urllib3
#urllib3.disable_warnings()
 
#获取指定页面中含有的url
def getPageUrl(url,html=None):
    if html == None:
        html = getHtml(url)
    uList = re.findall(PATTERN_URl, html)
    return uList
#深度字典，{url：层级,...},用来去重
depthDict = {}
 
def getUrlsDeep(url,depth = 3):
    try:
        if(depthDict[url]>=depth):
           return
 
        #避免碰到了下载链接，可见下文
        # if 'download' in str(url):
        #     return
        
        #获取此页中的所有连接
        clist = getPageUrl(url)
        print("\t\t"*depthDict[url],"#%d:%s"%(depthDict[url],url))
        for c in clist:
            #判断深度字典有有无此键，达到去重目的
            if c not in depthDict:
                depthDict[c]=depthDict[url]+1
                getUrlsDeep(c)
 
    except Exception as e:
        pass
 
if __name__ == '__main__':
    startUrl = 'https://www.allqj.com/#/'
    #爬取页面设置有第0级
    depthDict[startUrl] = 0
    #一共爬取2级
    getUrlsDeep(startUrl,depth=3)
