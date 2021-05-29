# coding=utf-8
import requests
import urllib
from bs4 import BeautifulSoup
import re
import xlwt

# 影片详细链接的规则
findLink = re.compile(r'<a class="" href="(.*?)">')  # 创建正则表达式对象，表示规则
# 影片图片的链接的规则
findImgSrc = re.compile(
    r'<img alt="(.*?)" class="" src="https://(.*?)" width="100"/>', re.S)
# 影片的片面
findTitle = re.compile(r'<span class="title">(.*?)</span>')
# 影片的评分
findRating = re.compile(
    r'<span class="rating_num" property="v:average">(.*)</span>')
# 影片评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 影片概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 找到影片相关信息
findbd = re.compile(r'<p class="">(.*?)</p>', re.S)


def main():
    baseurl = "https://movie.douban.com/top250?start="
# 1，爬取网页
    savepath = "豆瓣电影top.xls"
    datalist = getDate(baseurl)

# 3，保存数据
    save_data(datalist, savepath)
    # savepath(savepath)
    askURL(baseurl)

# 爬取网页


def getDate(baseurl):
    datalist = []
    for i in range(0, 10):                            # 调用获取页面信息的函数*10次
        url = baseurl + str(i*25) + '&filter='
        html = askURL(url)                            # 保存获取到的网页源码
# 2，逐一解析数据
        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.find_all('div', class_="item"):
            data = []                                 # 保存一步电影的所有信息
            item = str(item)
            link = re.findall(findLink, item)[0]    # re库用来通过正则表达式查找指定的字符串
            data.append(link)
            # ImgSrc = re.findall(findImgSrc, item)[0]
            # data.append(ImgSrc)
            Titles = re.findall(findTitle, item)
            # data.append(Titles)
            if(len(Titles) == 2):
                ctitle = Titles[0]                    # 添加中文名
                data.append(ctitle)
                otitle = Titles[1].replace("/", "")
                data.append(otitle)                   # 添加外国名
            else:
                data.append(Titles[0])
                data.append(" ")                      # 外国名留空
            rating = re.findall(findRating, item)
            data.append(rating)
            judgeNum = re.findall(findJudge, item)
            data.append(judgeNum)
            inq = re.findall(findInq, item)
            if len(inq) != 0:  # 如果为空
                inq = inq[0].replace("。", "")
                data.append(inq)
            else:
                data.append(" ")
            bd = re.findall(findbd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)  # 去掉</br>
            bd = re.sub('/', " ", bd)                 # 替换/
            data.append(bd.strip())                   # 去掉前后的空格
            # print(data)
            datalist.append(data)                     # 把处理好的信息放到datalist中
    # print(datalist)
    return datalist


def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66"
    }
# ---------------用户代理：表示告诉豆瓣服务器我们是什么类型的机器，浏览器（本质上是告诉浏览器，我们可以接受什么水平的文件）------------
    requst = urllib.request.Request(url, headers=head)
    html = ""
    # 返回并解码收到的回复
    try:
        response = urllib.request.urlopen(requst)
        html = response.read().decode("utf-8")
        # print(html)

    except urllib.error.URLError as e:                  # 异常处理
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def save_data(datalist, savepath):
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('豆瓣电影', cell_overwrite_ok=True)
    col = ('电影详细链接',  '影片中文名', '影片外国名', '评分', '评价数', '概况', '相关信息')
    for i in range(0, 7):
        sheet.write(0, i, col[i])
    for i in range(0, 250):
        print("第%d条" % (i+1))
        data = datalist[i]
        for j in range(0, 7):
            sheet.write(i+1, j, data[j])
    book.save(savepath)


if __name__ == "__main__":
    main()
    print('爬取完毕')


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# try:
#     response = urllib.request.urlopen("http://httpbin.org/get", timeout=0.1)
#     print(response.read().decode("utf-8"))
# except urllib.error.URLError as e:
#     print("time out")

# response = urllib.request.urlopen("http://www.baidu.com")
# print(response.status)

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66"
# }
# url = "http://www.douban.com"
# data = bytes(urllib.parse.urlencode({'name': 'eric'}), encoding="utf-8")
# req = urllib.request.Request(
#     url=url, data=data, headers=headers, method="POST",
# )
# response = urllib.request.urlopen(req)
# print(response.read().decode("utf-8"))

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
