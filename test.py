import os,pymysql
import bs4,requests,webbrowser
# link the database
# class MySQLCommand(object):
#     # 类的初始化
#     def __init__(self):
#         self.host = 'localhost'
#         self.port = 3306  # 端口号
#         self.user = 'root'  # 用户名
#         self.password = "979818137zzn"  # 密码
#         self.db = "gkdb"  # 库
#         self.table = "gkprdata"  # 表
#
#     # 链接数据库
#     def connectMysql(self):
#         try:
#             self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
#                                         passwd=self.password, db=self.db, charset='utf8')
#             self.cursor = self.conn.cursor()
#         except:
#             print('connect mysql error.')
# res = requests.get('http://college.gaokao.com/spepoint/a100/y2007/p5485/')#5485
# res.raise_for_status()
# predata = bs4.BeautifulSoup(res.text,features='html.parser')
# nextpage = predata.select('.fany li a')  #找到下一页的位置
# print(nextpage)
#
# nextlink = 'None'
# for i in range(len(nextpage)): #获取下一页的网址
#     if nextpage[i].string == '下一页 >>':
#         nextlink = nextpage[i]['href']
#         print(nextlink)
#     else:
#         continue
# if nextlink!='None':
#     webbrowser.open(nextlink)
# else:
#     print('get!')
#



# url = 'http://college.gaokao.com/spepoint/a100/y2007/'  # starting url
# os.makedirs('prdata',exist_ok=True)
# while not nextlink=='None': #Download the page
#     print('Downloading the data...')
#     res = requests.get(url)
#     res.raise_for_status()
#     predata = bs4.BeautifulSoup(res.text)
# Find the data

# from bs4 import BeautifulSoup
# from urllib import request
# import chardet
# from models import MySQLCommand
#
# for i in range(2018,2006,-1):
#     url = 'http://college.gaokao.com/spepoint/a100/y'+str(i)+'/'
#
#     response = request.urlopen(url)
#     html = response.read()
#     charset = chardet.detect(html)
#     html = html.decode(str(charset["encoding"]))  # 设置抓取到的html的编码方式
#
#     # 使用剖析器为html.parser
#     soup = BeautifulSoup(html, 'html.parser')
#     predata = soup.select('table td')
#     if predata == []:
#         print(1)
#         continue
#     else:
# #         print(2)
#
# from models import HTMLCommand
# htmlcmd = HTMLCommand()
# url = 'http://college.gaokao.com/spepoint/a100/y2007/p3/'
# soup = htmlcmd.gethtmldata(url,'.fany li a')
# nextlink = htmlcmd.getnextlink(soup)
# print(soup,';;;;;;;;;')
# # print(nextlink)
from bs4 import BeautifulSoup
from urllib import request
import chardet
import time
from models import MySQLCommand,HTMLCommand
import os,socket
# timeout = 1
# sleep_download_time =1
#
# class Htmlgetdata(object):
#     def getallhtmldata(self,url):
#         socket.setdefaulttimeout(timeout)
#         try:
#             res = requests.get(url)
#             res.raise_for_status()
#             soup = bs4.BeautifulSoup(res.text,features="html.parser")
#             predataFile = open(os.path.join('gkdata', os.path.basename(url)), 'wb')
#             predataFile.write(soup)
#             predataFile.close()
#             res.close()
#             time.sleep(sleep_download_time)
#             # selectanwser = soup.select(selectstyle)
#             # return selectanwser
#             return 0
#         except UnicodeDecodeError as e:
#             print('-----UnicodeDecodeError url:',url)
#         except socket.timeout as e:
#             print('-------socket timeout:',url)
#     def soupdata(self,predata):
#         selectanswer = predata.select
#
#
#
# datanextp = '.fany li a'
# os.makedirs('gkdata',exist_ok=True)
# url = 'http://college.gaokao.com/spepoint/a100/y2016/p1'
# nextlink = 'None'
# while(1):
#     if nextlink != 'None':
#         url = nextlink
#     turnpage = HTMLCommand().gethtmldata(url,datanextp)
#     nextlink = HTMLCommand().getnextlink(turnpage)
#     print(nextlink)
#     htmlgetdata = Htmlgetdata()
#     predata = htmlgetdata.getallhtmldata(url)
#     data =


    # predataFile = open(os.path.join('gkdata', os.path.basename(nextlink)),'wb')
from models import GMCommand
import numpy as np
import math
from numpy.linalg import *
# # print('使用列表生成一维数组')
# x0 = [318,249,251,216,219,206,212]
# gmcommand = GMCommand()
# # a = gmcommand.gmmodeling(x0, 1)
# # r0 = gmcommand.gmmodeling(x0, 2)
# # xa1 =[]
# xa0 = gmcommand.gmmodeling(x0,0)
# print('xa0:',xa0)
# A = gmcommand.residual(x0,xa0)
# modelju = gmcommand.modeljudge(x0,A)
#
#
#
#
#
#
#
# x0 = np.array(x0)
# # print(x0[1])
# r0 = [71.1,72.4,72.4,72.1,71.4,72.0,71.6]
# for k in range(1,7):
#     r0[k] = (x0[k-1])/(x0[k])
# x1 = []
# x1.append(x0[0])
#
# for i in range(1,7):
#     x1.append(x0[i]+x1[i-1])
# B = []
# Y = []
# for i in range(0,6):
#     B.append([(-0.5)*(x1[i]+x1[i+1]),1])
#
# for i in range(1,7):
#     Y.append(x0[i])
#
# B = np.array(B)
# Y = np.array(Y)
# u = np.dot(np.dot(np.linalg.inv(np.dot(B.transpose(),B)),B.transpose()),Y)
# a = u[0]
# b = u[1]
# xa0 = ['None']
# xa1 =['None']
# for k in range(0,6):
#     xa1.append((x0[0]-b/a)*math.e**(-(a*(k+1)))+b/a)
# c = (x0[0]-b/a)*math.e**(-(a*k))
# d = b/a
# xa1[0] = x0[0]
# xa0[0] = x0[0]
# for k in range(1,7):
#     xa0.append(xa1[k]-xa1[k-1])
#
# h = int(len(xa0))
# gmcommand = GMCommand()
# relative = gmcommand.relativeError(x0,xa0)
# res = gmcommand.jbpc(xa0,r0)
# print(res)
#
# cc = gmcommand.relativeError(x0,res)
# gmcommand = GMCommand()#immmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# # minscore = [607,615,641,603,581,607]
# minscore = [541,590,610,607,615,641,603,581]
# averscore = [597,623,642,640,635,654,641]
# min_pxa =gmcommand.gmmodeling(minscore,3)
# min_xa0 = gmcommand.gmmodeling(minscore,0)
# min_r0 = gmcommand.gmmodeling(minscore,2)
# judgemin_r0 = gmcommand.judgenumber(minscore)
#
#
# aver_pxa=gmcommand.gmmodeling(averscore,3)
# aver_xa0 = gmcommand.gmmodeling(averscore,0)
# aver_r0 = gmcommand.gmmodeling(averscore,2)
# judgeaver_r0 = gmcommand.judgenumber(averscore)
# A = gmcommand.residual(minscore,min_xa0)
# A2 = gmcommand.residual(averscore,aver_xa0)
# minmodeljudge = gmcommand.modeljudge(minscore,A)
# avermodeljudge = gmcommand.modeljudge(averscore,A2)
#
#
# print('最低分的预测值为:',min_pxa)
# print('平均分的预测值为:',aver_pxa)##########################################

# A = gmcommand.residual(minscore,min_xa0)
# print(A)
# pminscore = gmcommand.gmmodeling(minscore,3)
# paverscore = gmcommand.gmmodeling(averscore,3)
# print('pminscore',pminscore)
# print('paverscore',paverscore)
# p= gmcommand.Probability(570,pminscore,paverscore)

# #使成为二维数组
# print('录取概率P为：'+str(p*100)+'%')#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# mysqlcommand = MySQLCommand()
# mysqlcommand.connectMysql()
# table = "user"
# key = "username,userpassword"
# value = "'wangzhe','123456'"
# key2 = "username"
# value2 = "r"
# insert = mysqlcommand.insertall(table,key,value)
# select = mysqlcommand.select(table,key2,value2)
# print(select)
# print(type(select))
# print(insert)
# print(type(insert))
# mysqlcommand.closeMysql()


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# mysqlcommand = MySQLCommand()
# mysqlcommand.connectMysql()
# batch = '第一批'
# kemu = '理科'
# stuscore = 630
# stu_schoolname = '华南理工大学'
# mode = 4
#
# print('考生所在地区是：广东')
# print('考生批次是：',batch)
# print('考生文理科是',kemu)
# print('考生分数是：',stuscore)
# print('考生填写的学校是：',stu_schoolname)
# print('系统进行计算ing...')
#
#
#
# schoolname_chong,Pluqu_chong,recommendval = mysqlcommand.recommend(batch,kemu,stuscore,mode,stu_schoolname)
# # print(type(mysqlcommand.recommend(batch,kemu,stuscore,mode)))
# print(schoolname_chong,Pluqu_chong,recommendval)
# if Pluqu_chong==[]:
#     Pluqu_chong.append(0)
# if recommendval==[]:
#     recommendval.append(0)
# print('录取概率为：'+str(int(100*Pluqu_chong[0]))+'%')
# print('系统建议值（1-10分）：',recommendval[0])
# print(str(round(recommendval[0],2)))

# #############55555555555555555555555555555

# mysqlcommand = MySQLCommand()
# mysqlcommand.connectMysql()
# a = None
# print(type(a))
# # a=[1,2,3,4]
# print(type(len(a)))
# batch = '第一批'
# kemu = '理科'
# stuscore = 630
# stu_schoolname = None
# mode = 5
#
# schoolname_chong,Pluqu_chong,recommendval = mysqlcommand.recommend(batch,kemu,stuscore,mode,stu_schoolname)
# mode2 = 3
# schoolresult,Pluquresult,recommendvalresult = mysqlcommand.sortschool(schoolname_chong,Pluqu_chong,recommendval,mode2)
# msg = []
# print('mode = 3 ',schoolresult)
# for i in range(len(schoolresult)):
#     msg.append({
#         'schoolname':schoolresult[i],
#         'Pluquresult':Pluquresult[i],
#     })
# print(len(msg))
# print('33333333333333333333333333333333333',msg)
#
# mode2 = 1
# schoolresult,Pluquresult,recommendvalresult = mysqlcommand.sortschool(schoolname_chong,Pluqu_chong,recommendval,mode2)
# print('mode = 2',schoolresult)
# for j in range(len(schoolresult)):
#     msg.append({
#         'schoolwentuo':schoolresult[j],
#         'Pluquwentuo':Pluquresult[j],
#     })
# print('22222222222222222222222222',msg)
# print(len(msg))
# print('lastmsg',msg)


# print(Pluqu_chong,'aaaaaaaaaaaaaaaaggggggggggggggg')
# schoolnameresult = []
# Pluquresult = []
# recommendvalresult = []
# tempschoolname = []
# tempPluqu = []
# temprecommendval = []
# for i in range(len(Pluqu_chong)):
#     if Pluqu_chong[i]>=0.5 and Pluqu_chong[i]<=1:
#
#         tempschoolname.append(schoolname_chong[i])
#         tempPluqu.append(Pluqu_chong[i])
#         temprecommendval.append(recommendval[i])
# flag = mysqlcommand.sort(temprecommendval)
# print(flag)
# for j in range(len(flag)):
#     schoolnameresult.append(tempschoolname[flag[j]])
#     Pluquresult.append(tempPluqu[flag[j]])
#     recommendvalresult.append((temprecommendval[flag[j]]))
# print(temprecommendval,tempPluqu,tempschoolname)
# print(recommendvalresult,Pluquresult,schoolnameresult)




# # mysqlcommand.recommend(batch,kemu,stuscore,mode,stu_schoolname)
# # print(type(mysqlcommand.recommend(batch,kemu,stuscore,mode,)))
# print('aaaaaabbaaaaaaaa',schoolname_chong,Pluqu_chong,recommendval)
# print('考生所在地区是：广东')
# print('考生批次是：',batch)
# print('考生文理科是',kemu)
# print('考生分数是：',stuscore)
# print('考生填写的学校是：',str(stu_schoolname))
# print('考生想要查询 1.可冲击的学校，2.稳妥的学校，3.保底的学校。考生的选择是：',mode)
# print('系统进行计算ing...')
#
# a = []
# b = []
# c = []
# for i in range(int(len(schoolname_chong))):
#     a.append(schoolname_chong[i])
# print('符合要求的学校：',a)
#
#
# for i in range(int(len(schoolname_chong))):
#     if isinstance(Pluqu_chong[i],int) or isinstance(Pluqu_chong[i],float):
#         b.append(int(100 * Pluqu_chong[i]))
#     elif isinstance(Pluqu_chong[i],str):
#         b.append(0)
#
# print('录取概率分别为：'+str(b)+'%')
#
# for i in range(int(len(schoolname_chong))):
#     c .append(recommendval[i])
# print('系统建议值（1-10分）分别为：',c)
# int10=0
# intarry = []
# # jinzhi = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
# jinzhi ={"子":0,"丑":1,"寅":2,"卯":3,"辰":4,"巳":5,"午":6,"未":7,"申":8,"酉":9,"戌":10,"亥":11}
# str = '丑丑'
# # if len(str)==1:
# #     print(jinzhi[str])
# # else:
#
# for i in range(len(str)):
#     intarry.append(jinzhi[str[i]])
# for j in range(len(intarry)):
#     int10 = int10 + intarry[j] * (12**(len(intarry)-j-1))
# print(int10)





# for dizhi, int10 in [
#     ["子", 0],
#     ["丑", 1],
#     ["寅", 2],
#     ["卯", 3],
#     ["辰", 4],
#     ["巳", 5],
#     ["午", 6],
#     ["未", 7],
#     ["申", 8],
#     ["酉", 9],
#     ["戌", 10],
#     ["亥", 11],
#     ["丑子", 12],
#     ["丑丑", 13],
#     ["丑寅", 14],
#     ["丑卯", 15],
#     ["丑寅子卯", 2019],
# ]:
#     print(type(int10))






# a = 1
# st = '666'
# print(st.isdigit())
# if a>0:
#     b = 1
# print(b)

int10 = 13
str = ''
strarry = []
jinzhi = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
if int10<=11:
    str = jinzhi[int10]
else:
    while(int10/12 > 0):
        print(int10)
        strarry.append(jinzhi[int(int10%12)])
        int10 = int(int10/12)
        print(int10)
for i in range(len(strarry)-1,-1,-1):
    str = str + strarry[i]
print(str)