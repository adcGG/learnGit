from bs4 import BeautifulSoup
from urllib import request
import chardet
import socket
import threading
from models import MySQLCommand,HTMLCommand
socket.setdefaulttimeout(20)
datainfo = 'table td'
datanextp = '.fany li a'
mysqlCommand = MySQLCommand()
mysqlCommand.connectMysql()
for i in range(2007,2013):
    url = 'http://college.gaokao.com/spepoint/a100/y'+str(i)+'/'
    predata = HTMLCommand().gethtmldata(url,datainfo)
    turnpage = HTMLCommand().gethtmldata(url,datanextp)
    # response = request.urlopen(url)
    # html = response.read()
    # charset = chardet.detect(html)
    # html = html.decode(str(charset["encoding"]))  # 设置抓取到的html的编码方式
    # # 使用剖析器为html.parser
    # soup = BeautifulSoup(html, 'html.parser')
    # predata = soup.select('table td')
    # turnpage = soup.select('.fany li a')  # 找到下一页的位置

    # if predata == []:   #页面为空的时候跳下一个
    while predata != []:
        nextlink = 'None'
        for i in range(int(len(predata)/9)):
                profession_name = predata[0+9*i].string

                school_name = predata[1+9*i].string
                average_score = 'None'
                if predata[2 + 9 * i].string !='--':
                    average_score = predata[2 + 9 * i].string
                else:
                    average_score = '0'
                hightest_score = 'None'
                if predata[3 + 9 * i].string !='--':
                    hightest_score = predata[3 + 9 * i].string
                else:
                    hightest_score = '0'

                student_area = predata[4+9*i].string

                subject = predata[5+9*i].string

                years = predata[6+9*i].string

                batch = predata[7+9*i].string

                news_dict = {
                    "profession_name": profession_name,
                    "school_name": school_name,
                    "average_score": average_score,
                    "hightest_score": hightest_score,
                    "student_area": student_area,
                    "subject": subject,
                    "years": years,
                    "batch": batch,
                    }
                try:
                     # 插入数据，如果已经存在就不在重复插入
                    res = mysqlCommand.insertData(news_dict)
                    if res:
                        dataCount=res
                except Exception as e:
                    print("插入数据失败", str(e))  # 输出插入失败的报错语句
        for i in range(len(turnpage)):  # 获取下一页的网址
            timer = threading.Timer(1,HTMLCommand.funtimer)
            if turnpage[i].string == '下一页 >>':
                nextlink = HTMLCommand().getnextlink(turnpage)
                print(nextlink)
            else:
                continue
        if nextlink !='None':
            mysqlCommand.insert_url(nextlink)
            nextlink = mysqlCommand.getLastUrl()
            predata = HTMLCommand().gethtmldata(nextlink, datainfo)
            turnpage = HTMLCommand().gethtmldata(nextlink, datanextp)
        else:
            break

mysqlCommand.closeMysql()  # 最后一定要要把数据关闭
# dataCount = 0
