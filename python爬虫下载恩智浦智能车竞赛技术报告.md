---
title: python爬虫下载恩智浦智能车竞赛技术报告
date: 2020-04-01 13:12:08
tags:
- 目录
- python
- 爬虫
---

# 一、目标

新一届的全国大学生智能汽车竞赛开始了，想下载官网上的技术报告，看看大佬们在坐车时候的想法 ，然而官网的技术报告有点多，而且还没打包，得一个一个慢慢点击下载，下载速率太慢了，这不刚学了一下python爬虫吗，就想试试能不能使用python爬虫下载智能车竞赛官网的技术报告。
[**python** 爬虫学习](https://editor.csdn.net/md/?articleId=105045725)参见我的这篇文章
[另外我的博客上也有上传](https://thelnktears.github.io/2020/03/13/Python%E7%88%AC%E8%99%AB%E5%AD%A6%E4%B9%A0/)

<!--more-->

# 二、目标分析

## 1、技术报告的URL链接

打开官网，找到下载技术报告的页面，因为参赛的队伍比较多，优秀的队伍的技术报告也就多，所以官网将技术报告分到好几个页面中，点击一个选项组，**2019-10-23   第十四届竞赛技术报告(6)** 先找到一个要下载的技术报告，发现点击后就会下载，选中这个技术报告的名字，右键点击检查，查看网页代码，发现技术报告的下载地址就是 `<a>...</a>` 标签内 **href** 后面的链接，这样我们就找到了技术报告的链接地址了，但是一个页面中有那么多技术报告，不能一个一个填啊，所以我们就需要遍历查找这些 `<a>...</a>` 标签，从他的 **href** 属性中获得链接地址。
![4](https://img-blog.csdnimg.cn/20200401151155177.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjU4NTMxNg==,size_16,color_FFFFFF,t_70#pic_center)

## 2、下载页面的URL

反过头查看下载页面的 **URL** 连接，发现这不就是竞赛官网的资料下载页面的 **URL** 吗？这咋和下载页面的 **URL** 一样？怎么网页地址没有变。得看一下到底指什么情况，检查一下网页代码，分析情况。
![1](https://img-blog.csdnimg.cn/20200401144612701.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjU4NTMxNg==,size_16,color_FFFFFF,t_70#pic_center)
找到要下载的页面选项，将其选中，比如： **2019-10-23   第十四届竞赛技术报告(5)** 选中后右键点击检查，查看源码。
![3](https://img-blog.csdnimg.cn/20200401165104993.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjU4NTMxNg==,size_16,color_FFFFFF,t_70#pic_center)
发现这是 **JavaScript** 写的，**void(0)** 是一个点击不发生任何效果，停留在原地，称之为“死链接”，而我们想要的资源列表是在点击这段文字后出现的，那我们怎么的到还有技术报告的页面链接呢？这不是点击后跳转的吗，那就模拟人上网，用鼠标点击这个标签他不就过来了吗？然后经过查找，得出这个页面的连接放在 `<iframe>...</iframe>` 这么一个标签的 **src** 属性中。同样的方法测试别的下载页面都是一样的，所以下载页面的 **URL** 地址也就找到了。

# 三、开始写代码

## 1、获取下载页面的URL

前面分析我们知道，下载页面是 **JavaScript:void(0)** 实现的一个死链接，真正的连接在点击资料下载页面相应的文字后加载到新的资源页面后，在一个 `<iframe>...</iframe>` 标签的 **src** 属性里。我们要获得真正的下载页面的 **URL** 地址需要模拟鼠标点击，所以我们使用 **selenium** 模块中的 **webdriver**，所以先将模块导入。

```python
from selenium import webdriver
```

接下来就快开始构建一个浏览器对象，使用无头浏览器模拟点击各个标签获取到下载页面的地址先保存起来。

```python
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
    # 以下使我们要点击的标签的 xpath ，发现只有 li 标签后缀再改
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

```

## 2、获取技术报告的URL

得到每个下载页面的 **URL** 后我们需要从每个下载页面得到技术报告的 **URL** 链接，这些链接才是我们真正下载时候需要的页面，通过前面分析，技术报告的 **URL** 链接在 `<a>...</a>` 标签的 **href** 属性中。遍历我们保存的下载页面的 **URL** ，访问这些 **URL** 获取到每个页面的网页代码，从中在遍历查找 `<a>...</a>` 标签，获取到技术报告的 **URL** 。
遍历下载页面的 **URL** ，获得每一页的网页源代码

```python
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
            print("............................................................")
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
        print("..........................................................................")
    except:
        print("异常")
```

遍历获得到的网页源代码，从 `<a>...</a>` 标签获取到技术报告的 **URL** 

```python
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
```

## 3、筛选得到的URL

参看每个下载页面的内容发现，其实每个下载页面的内容挺乱的，出了要下载的技术报告外，里面还有像车模检查表、参赛证明、车模照片、电路图等，特别乱，像车模检查表这些我们都不需要，所以我们得将其筛选出去

```python
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
        if (name.find("检查表") >= 0) or (name.find(".jpg") >= 0)\
        or (name.find(".png") >= 0) or (name.find(".JPEG") >= 0)\
        or (name.find("照片") >= 0) or (name.find("承诺书") >= 0) \
        or (name.find(".xlsx") >= 0) or (name.find("回执") >= 0)\
        or (name.find("表") >= 0) or (name.find("参赛证明") >= 0) \
        or (name.find("图片") >= 0) or (name.find(".JPG") >= 0) \
        or (name.find(".PNG") >= 0) or (name.find(".jpeg") >= 0)\
        or (name.find(".bmp") >= 0):
            del (url[name])  # 删除我们不想要的资源
            continue
        else:
            # print(name)
            i = i + 1
    print(i)  # 打印我们想要的资源的数量
```

筛选过后差不多就是我们想要的了，不包括玩我的筛选问题，将一部分技术报告筛选出去的，因为太多我也没法查看，另外还有些文件名称命名比较模糊的，不知道是技术报告还是其他的什么东西的我没有进行排除，你们也可以自己尝试，因为正则表达式我感觉有点麻烦，所以我就通过保存的链接的字典中键值对进行了筛选，可能误差比较大。

## 4、获得技术报告

得到我们想要的技术报告的 **URL** 连接后我们就需要将其下载下来进行保存，这里我新建了一个文件夹，将其保存在里面。

```python
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
```

## 5、开始下载

![5](https://img-blog.csdnimg.cn/20200401162713226.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjU4NTMxNg==,size_16,color_FFFFFF,t_70#pic_center)
这样就开始下载了，下载的时候会在 **python** 文件所在目录新建一个 **技术报告** 的文件夹，下载的技术报告就会保存的那，另外中间我也尝试用多线程去跑，但我添加上之后出现问题，没法运行也就放弃了，大家可以自己尝试一下

# 四、总结

第一次使用爬虫下载自己想要的东西，很开心，虽然中间遇到了很多困难，但都一一解决了，唯一没有解决的是多线程问题，接下来会好好研究一下，争取攻破。

# 五、完整代码

```python
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
            print("..................................................................")
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
        print("........................................................")
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
        if (name.find("检查表") >= 0) or (name.find(".jpg") >= 0)\
        or (name.find(".png") >= 0) or (name.find(".JPEG") >= 0)\
        or (name.find("照片") >= 0) or (name.find("承诺书") >= 0) \
        or (name.find(".xlsx") >= 0) or (name.find("回执") >= 0)\
        or (name.find("表") >= 0) or (name.find("参赛证明") >= 0) \
        or (name.find("图片") >= 0) or (name.find(".JPG") >= 0) \
        or (name.find(".PNG") >= 0) or (name.find(".jpeg") >= 0)\
        or (name.find(".bmp") >= 0):
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

```