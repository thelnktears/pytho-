import requests
import bs4
import os
from selenium import webdriver
import time
import threading


def getHTMLText(href, html):
    '''
    从每一页的连接中获取每一页的HTML代码
    :param href: 每一页的连接地址，用列表表示
    :param html: 每一页的HTML代码，用列表表示
    :return: None
    '''
    try:
        i = 0
        for connection in href:  # 遍历每一页的连接地址
            print(
                ".............................................................................................................")
            print("开始解析")
            print(connection)  # 打印将要解析的连接地址
            files = requests.get(connection)  # 爬取每个页面的HTML地址
            # print(files.status_code)
            files.raise_for_status()  # 检查返回状态，200 为连接正常，否则产生异常
            files.encoding = files.apparent_encoding
            # print(files.text)
            soup = bs4.BeautifulSoup(files.text, 'html.parser')  # 解析页面文件
            html.append(soup)  # 将每页的HTML源码文件添加到html的列表中
            i = i + 1
            # print(soup.prettify())
            # print(html)
        print(".............................................................................................................")
    except:
        print("异常")


def getHref(html, url):
    '''
    从每页的HTML源码文件中获得资源文件的名称和连接
    :param html: 每页的HTML代码
    :param url: 每一个资源文件的地址和名称，用字典保存
    :return: None
    '''
    # print(html.a.attrs)
    i = 0
    for i in html:  # 遍历每一资源页
        for link in i.find_all("a"):  # 查找资源页的资源地址
            # print(link.string)
            # print(link.get("href"))
            hrefstring = str(link.string).strip()  # 去掉资源名称中的空格\r\t等字符
            hrefURL = str(link.get("href")).strip()  # 去掉资源地址中的空格\r\t等字符
            # href.update(link.string , link.get("href"))
            # print(href[link.string])
            url[hrefstring] = hrefURL  # 将资源保存到列表中
    # print(url)


def getfiles(url):
    '''
    从我们的到的资源链接中获取到文件，并且保存到本地的技术报告文件夹
    :param url: 获取到的资源文件的连接和名称的字典
    :return: None
    '''
    path = os.getcwd() + r"\技术报告"  # 获取到目前文件夹路径，构造要保存的文件夹路径
    # 判断是否存在文件夹，没有的话建立文件夹
    if not os.path.isdir(path):  # 判断是否有这么个路径，没有的话就开始创建
        os.mkdir(path)  # 创建文件夹
        os.chdir(path)  # 将工作路径切换到将要下载到的文件夹
        print(os.getcwd())
    else:
        os.chdir(path)  # 将工作路径切换到将要下载到的文件夹
        print(os.getcwd())
        i = 1
        for filesvalue in url.keys():  # 遍历资源链接的字典
            # filesname = os.path.splitext(filesvalue)[0]  # 从资源的字典中获得文件名称
            # filesdriname = os.path.splitext(filesvalue)[1]
            # filesName = filesname+filesdriname
            print("开始下载" + filesvalue)
            files = open(filesvalue, mode="wb")  # 创建文件
            try:
                f = requests.get(url.get(filesvalue))  # 获得文件
                f.raise_for_status()
                f.encoding = f.apparent_encoding
                files.write(f.content)  # 写入文件
                files.close()  # 关闭文件
                print("下载完成............................................."+ str(i))
                i = i + 1
            except:
                print("下载失败")


def hrefNmae(url):
    '''
    筛选资源名称和链接，通过筛选资源名称，得到我们想要的资源
    :param url: 每个资源的名称与连接的字典
    :return: None
    '''
    i = 0
    for name in list(url.keys()):  # 遍历存资源链接和名称的字典
        # print(name)
        # 筛选我们想要的资源
        if (name.find("检查表") >= 0) or (name.find(".jpg") >= 0) or (name.find(".png") >= 0) \
                or (name.find(".JPEG") >= 0) or (name.find("照片") >= 0) or (name.find("承诺书") >= 0) \
                or (name.find(".xlsx") >= 0) or (name.find("回执") >= 0) or (name.find("表") >= 0) \
                or (name.find("参赛证明") >= 0) or (name.find("图片") >= 0) or (name.find(".JPG") >= 0) \
                or (name.find(".PNG") >= 0) or (name.find(".jpeg") >= 0) or (name.find(".bmp") >= 0):
            del (url[name])  # 删除我们不想要的资源
            continue
        else:
            # print(name)
            i = i + 1
    print(i)  # 打印我们想要的资源的数量


def geturl(begainurl, href):
    '''
    从主页开始，遍历我们想要的页面，获得页面地址
    :param begainurl: 主页的url连接
    :param href: 每个子页面的连接
    :return: None
    '''
    options = webdriver.ChromeOptions()  # 实例化Chrome浏览器的设置
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)  # 实例化Chrome浏览器
    driver.get(begainurl)  # 从主页开始
    # "/html/body/div[4]/div[3]/div[1]/ul/li[7]/a/span[1]"
    # "/html/body/div[4]/div[3]/div[1]/ul/li[6]/a/span[1]"
    # "/html/body/div[4]/div[3]/div[1]/ul/li[5]/a/span[1]"
    # "/html/body/div[4]/div[3]/div[1]/ul/li[4]/a/span[1]"
    # "/html/body/div[4]/div[3]/div[1]/ul/li[4]/a/span[1]"
    # "/html/body/div[4]/div[3]/div[1]/ul/li[2]/a/span[1]"
    # "/html/body/div[4]/div[3]/div[1]/ul/li[1]/a/span[1]"
    for i in range(1, 7):
        xpath = "/html/body/div[4]/div[3]/div[1]/ul/li[" + str(i) + "]/a/span[1]"  # 构造xpath
        # print(xpath)
        href1 = driver.find_element_by_xpath(xpath).click()  # 寻找对应的元素并且点击进入下一个页面
        soup = bs4.BeautifulSoup(driver.page_source, "html.parser")  # 解析页面代码文件
        url = soup.iframe.attrs["src"]  # 获取想要的连接地址
        print(url)
        href.append(url)  # 将地址添加到列表当中
        time.sleep(2)  # 等待页面加载完毕
        driver.get(begainurl)  # 从主页开始
        time.sleep(2)
    time.sleep(2)
    driver.close()  # 关闭浏览器页面
    driver.quit()
    # print(href)                                                         # 打印获取到的连接列表


if __name__ == "__main__":
    href = []
    html = []
    url = {}
    beginurl = "https://smartcar.cdstm.cn/index/8.html"
    geturl(beginurl, href)  # 从主页获取每个页面的url连接
    getHTMLText(href, html)  # 获得每个页面的HTML源码
    getHref(html, url)  # 从HTML源码中获得资源名称和连接
    hrefNmae(url)  # 筛选获得到的连接名称和连接地址
    print(url.items())  # 输出资源的名称和连接
    getfiles(url)  # 获取到文件
