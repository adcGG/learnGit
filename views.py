from __future__ import unicode_literals
from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponse,HttpRequest,JsonResponse
from .models import MySQLCommand
from .models import GMCommand
from .models import AHP
from django.views.decorators.csrf import csrf_exempt
import ast
from flask import jsonify,render_template

import json

# mysqlcommand = MySQLCommand()
# mysqlcommand.connectMysql()

# Create your views here.
@csrf_exempt
def schoolSearch(request):
    SearchscorelineMsg = []
    SearchMsg = {}
    SearchMsgcpl = {}
    if (request.method == 'POST'):
        mysqlcommand = MySQLCommand()
        mysqlcommand.connectMysql()
        # sql = "SELECT * FROM gkschoolscoreline"
        cursor = mysqlcommand.conn.cursor()
        postbody = request.body.decode('utf-8')
        schoolinfo = ast.literal_eval(postbody)
        schoolname = schoolinfo['SchoolName']
        sqlschoolSearch = "SELECT * FROM gkschoolinfo WHERE schoolname = '"+schoolname+"'"
        sqlschoolScorelineSearch = "SELECT * FROM gkschoolscoreline WHERE schoolname = '"+schoolname+"'"
        
        cursor.execute(sqlschoolSearch)
        mysqlcommand.conn.commit()
        schoolRecord = cursor.fetchone()
        
        cursor.execute(sqlschoolScorelineSearch)
        mysqlcommand.conn.commit()        
        schoolscoreRecord = cursor.fetchall()
        print(schoolscoreRecord,type(schoolscoreRecord))
        mysqlcommand.closeMysql()
        if schoolscoreRecord == ():
            SearchscorelineMsg.append({'staus':0})
        else:
            for i in range(int(len(schoolscoreRecord))):
                SearchscorelineMsg.append(
                    {
                        'staus':1,
                        'schoolname': schoolscoreRecord[i][1],
                        'kemu': schoolscoreRecord[i][2],
                        'year': schoolscoreRecord[i][3],
                        'minscore': schoolscoreRecord[i][4],
                        'maxscore': schoolscoreRecord[i][5],
                        'averscore': schoolscoreRecord[i][6],
                        'luqunum': schoolscoreRecord[i][7],
                        'luqubatch': schoolscoreRecord[i][8],
                    }
                )

        if schoolRecord == None:
            SearchMsg = {
                'staus':0,
            }
        else:
            SearchMsg = {
                'staus':1,
                'schoollishu':schoolRecord[1],
                'schoollocal':schoolRecord[2],
                'academician':schoolRecord[3],
                'doctor': schoolRecord[4],
                'master': schoolRecord[5],
                'schoolconnlocal': schoolRecord[6],
                'schoolphone': schoolRecord[7],
                'schoolemail': schoolRecord[8],
                'schoolweb': schoolRecord[9],
                'schooltype1': schoolRecord[10],
                'schooltype2': schoolRecord[11],
                'abstract': schoolRecord[12],
                'shizipower': schoolRecord[13],
                'jiuye': schoolRecord[14],
                'schoolname': schoolRecord[15],

            }

        # myschoolscorelinelist.append(
        #     {
        #         'schoolname': pageResult[i][1],
        #         'kemu': pageResult[i][2],
        #         'year': pageResult[i][3],
        #         'minscore': pageResult[i][4],
        #         'maxscore': pageResult[i][5],
        #         'averscore': pageResult[i][6],
        #         'luqunum': pageResult[i][7],
        #         'luqubatch': pageResult[i][8],
        #     }
        SearchMsgcpl={
            'SearchMsg':SearchMsg,
            'SearchscorelineMsg':SearchscorelineMsg,
        }
        print(SearchscorelineMsg)
        return JsonResponse(SearchMsgcpl, safe=False)


@csrf_exempt
def login(request):
    loginMsg = {}
    if (request.method == 'POST'):
        isOkPsw ={}
        registerSuced = {}
        registerMsg = {}
        mysqlcommand = MySQLCommand()
        mysqlcommand.connectMysql()
        # sql = "SELECT * FROM gkschoolscoreline"
        cursor = mysqlcommand.conn.cursor()
        postbody = request.body.decode('utf-8')
        logininfo = ast.literal_eval(postbody)
        print(logininfo)
        username = logininfo['loginUserName']
        userpassword = logininfo['loginUserPsw']

        table = "user"
        key = "username"

        if username=='':
            loginMsg['userNameEmpty'] = 0
            print(loginMsg)
            return JsonResponse(loginMsg, safe=False)
        if userpassword=='':
            loginMsg['userNameEmpty'] = 1
            loginMsg['userPswEmpty'] = 0
            print(loginMsg)
            return JsonResponse(loginMsg,safe=False)
        else:
            loginMsg['userNameEmpty'] = 1
            loginMsg['userPswEmpty'] = 1

        # value = "'" + str(username) + "','" + str(userpassword) + "'"
        value = str(username)+"','"+str(userpassword)
        if mysqlcommand.select(table, key, username) == ():
            loginMsg['userLoginSuced'] = 0
            print(loginMsg)
            return JsonResponse(loginMsg,safe=False)
        elif mysqlcommand.select(table, key, username)[0][2]==userpassword:
            loginMsg['userLoginSuced'] = 1
            loginMsg['userName'] = username
            print(loginMsg)
            return JsonResponse(loginMsg,safe=False)
        else:
            loginMsg['userLoginSuced'] = 0
            print(loginMsg)
            return JsonResponse(loginMsg,safe=False)


    # return render(request, 'login/login.html')

@csrf_exempt
def schoolrecommend(request):
    if(request.method == 'POST'):
        mysqlcommand = MySQLCommand()
        mysqlcommand.connectMysql()
        concat = request.POST
        postbody = request.body.decode('utf-8')
        stuinfo = ast.literal_eval(postbody)
        print(stuinfo)
        batch = stuinfo['batch']
        kemu = stuinfo['kemu']
        stuscore = stuinfo['score']
        schoolrecommendmsg0 = []
        schoolrecommendmsg1 = []
        schoolrecommendmsg2 = []
        schoolrecommendmsg3 = []
        schoolrecommendmsg = {}
        isempty = {}
        # try:

        if batch == ''or kemu == '' or stuscore=='' or not stuscore.isdigit():
            allmsg = 0
            schoolrecommendmsg0 = {
                'allmsg': allmsg,
            }
            return JsonResponse(schoolrecommendmsg0, safe=False)
        # except:
        else:
            allmsg = 1
            stuscore = int(stuscore)
            stu_schoolname = None
            mode = 5
            schoolname, Pluqu,recommendval = mysqlcommand.recommend(batch, kemu, stuscore, mode,stu_schoolname)
            mode1 = 1
            schoolresult, Pluquresult, recommendvalresult = mysqlcommand.sortschool(schoolname, Pluqu,
                                                                                    recommendval, mode1)
            if len(schoolresult) == 0:
                isempty['msg1staus'] = 0
            else:
                isempty['msg1staus'] = 1
            for i in range(len(schoolresult)):

                schoolrecommendmsg1.append({
                    'staus':1,
                    'allmsg':allmsg,
                    'schoolname_chongji':schoolresult[i],
                    'Pluqu_chongji':str(round(100*Pluquresult[i],2))+'%',
                    'recommendvalchongji':str(round(recommendvalresult[i],2)),

                })
            mode2 = 2
            schoolresult, Pluquresult, recommendvalresult = mysqlcommand.sortschool(schoolname, Pluqu,
                                                                                    recommendval, mode2)
            if len(schoolresult) == 0:
                isempty['msg2staus'] = 0
            else:
                isempty['msg2staus'] = 1
            for j in range(len(schoolresult)):


                schoolrecommendmsg2.append({
                    'staus':1,
                    'allmsg': allmsg,
                    'schoolname_wentuo':schoolresult[j],
                    'Pluqu_wentuo':str(round(100*Pluquresult[j],2))+'%',
                    'recommendvalwentuo':str(round(recommendvalresult[j],2)),
                })

            mode3 = 3
            schoolresult, Pluquresult, recommendvalresult = mysqlcommand.sortschool(schoolname, Pluqu,
                                                                                    recommendval, mode3)
            if len(schoolresult) == 0:
                isempty['msg3staus'] = 0
            else:
                isempty['msg3staus'] = 1
            for k in range(len(schoolresult)):

                schoolrecommendmsg3.append({
                    'staus': 1,
                    'allmsg': allmsg,
                    'schoolname_baodi':schoolresult[k],
                    'Pluqu_baodi':str(round(100*Pluquresult[k],2))+'%',
                    'recommendvalbaodi':str(round(recommendvalresult[k],2)),
                })
            print('schoolrecommendmsg1',schoolrecommendmsg1)
            print('schoolrecommendmsg2', schoolrecommendmsg2)
            print('schoolrecommendmsg3', schoolrecommendmsg3)
            schoolrecommendmsg = {
                'schoolrecommendmsg1': schoolrecommendmsg1,
                'schoolrecommendmsg2': schoolrecommendmsg2,
                'schoolrecommendmsg3': schoolrecommendmsg3,
                'isempty':isempty,
            }
            return JsonResponse(schoolrecommendmsg ,safe=False)

@csrf_exempt
def luqu(request):
    if(request.method == 'POST'):
        mysqlcommand = MySQLCommand()
        mysqlcommand.connectMysql()
        concat = request.POST
        postbody = request.body.decode('utf-8')
        stuinfo = ast.literal_eval(postbody)
        batch = stuinfo['batch']
        kemu = stuinfo['kemu']
        stuscore = stuinfo['score']

        try:
            if batch == ''or kemu == '' or stuscore=='' or not stuscore.isdigit():
                allmsg = 0
                luqumsg = {
                    'allmsg': allmsg,
                }
            return JsonResponse(luqumsg, safe=False)
        except:
            allmsg = 1
            stuscore = int(stuscore)
            stu_schoolname = stuinfo['targetschool']
            mode=4
            schoolname_target, Pluqu_target, recommendval = mysqlcommand.recommend(batch, kemu, stuscore, mode,stu_schoolname)
            if schoolname_target==[]:
                schoolname_target.append('请检查是否填对学校名称或者是否填对批次')
            if Pluqu_target == []:
                Pluqu_target.append(0)
            if recommendval == []:
                recommendval.append(0)
            luqumsg = {
                'allmsg':allmsg,
                'schoolname_target':schoolname_target[0],
                'Pluqu_target':str(round(100*Pluqu_target[0],2))+'%',
                'recommendval':str(round(recommendval[0],2)),
            }
            return JsonResponse(luqumsg, safe=False)

@csrf_exempt
def wishfill(request):
    if(request.method == 'POST'):
        mysqlcommand = MySQLCommand()
        mysqlcommand.connectMysql()
        concat = request.POST
        postbody = request.body.decode('utf-8')
        stuinfo = ast.literal_eval(postbody)
        print(concat)
        print(postbody)
        print(stuinfo)
        batch = stuinfo['batch']
        kemu = stuinfo['kemu']
        stuscore = stuinfo['score']
        try:
            if batch == ''or kemu == '' or stuscore=='' or not stuscore.isdigit():
                allmsg = 0
                wishfillmsg = {
                    'allmsg': allmsg,
                }
            return JsonResponse(wishfillmsg, safe=False)
        except:
            allmsg = 1
            stuscore = int(stuscore)
            chongjischool1 = stuinfo['chongji1']
            wentuoschool1 = stuinfo['wentuo1']
            baodischool1 = stuinfo['baodi1']
            chongjischool2 = stuinfo['chongji2']
            wentuoschool2 = stuinfo['wentuo2']
            baodischool2 = stuinfo['baodi2']
            Pluqu_chongji2 = []
            Pluqu_chongji1 = []
            Pluqu_wentuo1 = []
            Pluqu_wentuo2 = []
            Pluqu_baodi1 = []
            Pluqu_baodi2 = []
            schoolname_chongji1 = []
            schoolname_chongji2 = []
            schoolname_wentuo1 = []
            schoolname_wentuo2 = []
            schoolname_baodi1 = []
            schoolname_baodi2 = []
            wishfill_chongji1msg = ''
            wishfill_chongji2msg = ''
            wishfill_wentuo1msg = ''
            wishfill_wentuo2msg = ''
            wishfill_baodi1msg = ''
            wishfill_baodi2msg = ''

            if chongjischool1 !='':
                mode=4
                schoolname_chongji1, Pluqu_chongji1, recommendval = mysqlcommand.recommend(batch, kemu, stuscore, mode,
                                                                                       chongjischool1)
                if schoolname_chongji1 == []:
                    schoolname_chongji1.append('请检查是否填对学校名称或者是否填对批次')
                if Pluqu_chongji1 == []:
                    Pluqu_chongji1.append(0)
                if Pluqu_chongji1[0]>0.5 and Pluqu_chongji1[0]<0.8:
                    wishfill_chongji1msg = '符合可冲击院校概率要求'
                else:
                    wishfill_chongji1msg = '不符合可冲击院校概率要求，建议替换！'
            else:
                Pluqu_chongji1.append(0)
                schoolname_chongji1.append('请检查是否填对学校名称')

            if chongjischool2 !='':
                mode=4
                schoolname_chongji2, Pluqu_chongji2, recommendva2 = mysqlcommand.recommend(batch, kemu, stuscore, mode,
                                                                                       chongjischool2)
                if schoolname_chongji2 == []:
                    schoolname_chongji2.append('请检查是否填对学校名称或者是否填对批次')
                if Pluqu_chongji2 == []:
                    Pluqu_chongji2.append(0)
                if Pluqu_chongji2[0]>0.5 and Pluqu_chongji2[0]<0.8:
                    wishfill_chongji2msg = '符合可冲击院校概率要求'
                else:
                    wishfill_chongji2msg = '不符合可冲击院校概率要求，建议替换！！'
            else:
                Pluqu_chongji2.append(0)
                schoolname_chongji2.append('请检查是否填对学校名称')

            if Pluqu_chongji1[0]<Pluqu_chongji2[0]:
                chongji_last_msg = '排序合理'
            else:
                chongji_last_msg = '排序不合理,请检查或修改该项志愿的填报'


            if wentuoschool1 != '':
                mode=4
                schoolname_wentuo1, Pluqu_wentuo1, recommendval1 = mysqlcommand.recommend(batch, kemu, stuscore, mode,
                                                                                       wentuoschool1)
                if schoolname_wentuo1 == []:
                    schoolname_wentuo1.append('请检查是否填对学校名称或者是否填对批次')
                if Pluqu_wentuo1 == []:
                    Pluqu_wentuo1.append(0)
                if Pluqu_wentuo1[0]>0.8 and Pluqu_wentuo1[0]<0.9:
                    wishfill_wentuo1msg = '符合较稳妥院校概率要求'
                else:
                    wishfill_wentuo1msg = '不符合较稳妥院校概率要求，建议替换！'
            else:
                Pluqu_wentuo1.append(0)
                schoolname_wentuo1.append('请检查是否填对学校名称')

            if wentuoschool2 != '':
                mode=4
                schoolname_wentuo2, Pluqu_wentuo2, recommendval1 = mysqlcommand.recommend(batch, kemu, stuscore, mode,
                                                                                       wentuoschool2)
                if schoolname_wentuo2 == []:
                    schoolname_wentuo2.append('请检查是否填对学校名称或者是否填对批次')
                if Pluqu_wentuo2 == []:
                    Pluqu_wentuo2.append(0)
                if Pluqu_wentuo2[0]>0.8 and Pluqu_wentuo2[0]<0.9:
                    wishfill_wentuo2msg = '符合较稳妥院校概率要求'
                else:
                    wishfill_wentuo2msg = '不符合较稳妥院校概率要求，建议替换！'
            else:
                Pluqu_wentuo2.append(0)
                schoolname_wentuo2.append('请检查是否填对学校名称')

            if Pluqu_wentuo1[0]<Pluqu_wentuo2[0]:
                wentuo_last_msg = '排序合理'
            else:
                wentuo_last_msg = '排序不合理,请检查或修改该项志愿的填报'

            if baodischool1 != '':
                mode=4
                schoolname_baodi1, Pluqu_baodi1, recommendval1 = mysqlcommand.recommend(batch, kemu, stuscore, mode,
                                                                                       baodischool1)
                if schoolname_baodi1 == []:
                    schoolname_baodi1.append('请检查是否填对学校名称或者是否填对批次')
                if Pluqu_baodi1 == []:
                    Pluqu_baodi1.append(0)
                if Pluqu_baodi1[0]>0.9 and Pluqu_baodi1[0]<=1:
                    wishfill_baodi1msg = '符合保底院校概率要求'
                else:
                    wishfill_baodi1msg = '不符合保底院校概率要求，建议替换！'
            else:
                Pluqu_baodi1.append(0)
                schoolname_baodi1.append('请检查是否填对学校名称')

            if baodischool2!= '':
                mode=4
                schoolname_baodi2, Pluqu_baodi2, recommendval1 = mysqlcommand.recommend(batch, kemu, stuscore, mode,
                                                                                       baodischool2)
                if schoolname_baodi2 == []:
                    schoolname_baodi2.append('请检查是否填对学校名称或者是否填对批次')
                if Pluqu_baodi2 == []:
                    Pluqu_baodi2.append(0)
                if Pluqu_baodi2[0]>0.9 and Pluqu_baodi2[0]<=1:
                    wishfill_baodi2msg = '符合保底院校概率要求'
                else:
                    wishfill_baodi2msg = '不符合保底院校概率要求，建议替换！'
            else:
                Pluqu_baodi2.append(0)
                schoolname_baodi2.append('请检查是否填对学校名称')

            if Pluqu_baodi1[0]<Pluqu_baodi2[0]:
                baodi_last_msg = '排序合理'
            else:
                baodi_last_msg = '排序不合理，请检查或修改该项志愿的填报'

            wishfillmsg = {
                'allmsg':allmsg,
                'schoolname_chongji1':schoolname_chongji1[0],
                'schoolname_chongji2':schoolname_chongji2[0],
                'Pluqu_chongji1':str(round(100*Pluqu_chongji1[0],2))+'%',
                'Pluqu_chongji2':str(round(100*Pluqu_chongji2[0],2))+'%',
                'wishfill_chongji1msg':wishfill_chongji1msg,
                'wishfill_chongji2msg': wishfill_chongji2msg,
                'wishfill_wentuo1msg': wishfill_wentuo1msg,
                'wishfill_wentuo2msg': wishfill_wentuo2msg,
                'wishfill_baodi1msg': wishfill_baodi1msg,
                'wishfill_baodi2msg': wishfill_baodi2msg,
                'schoolname_wentuo1': schoolname_wentuo1[0],
                'schoolname_wentuo2': schoolname_wentuo2[0],
                'Pluqu_wentuo1': str(round(100*Pluqu_wentuo1[0],2))+'%',
                'Pluqu_wentuo2': str(round(100*Pluqu_wentuo2[0],2))+'%',
                'schoolname_baodi1': schoolname_baodi1[0],
                'schoolname_baodi2': schoolname_baodi2[0],
                'Pluqu_baodi1': str(round(100*Pluqu_baodi1[0],2))+'%',
                'Pluqu_baodi2': str(round(100*Pluqu_baodi2[0],2))+'%',
                'chongji_last_msg':chongji_last_msg,
                'wentuo_last_msg':wentuo_last_msg,
                'baodi_last_msg':baodi_last_msg,
            }
            return JsonResponse(wishfillmsg, safe=False)


@csrf_exempt
def schoolscoreline(request):
    # if (request.method == 'GET'):
    #     postbody = request.body.decode('utf-8')
    #     pageinfo = {}
    #     try:
    #         pageinfo = ast.literal_eval(postbody)
    #     except:
    #         pageinfo['pageSize']='None'
    #         pageinfo['pageNum']='NoneNum'
    #     pageSize = pageinfo['pageSize']
    #     pageNum = pageinfo['pageNum']  # 传递参数到这里来
    #     print('pageNum:', pageNum, 'pageSize', pageSize)
    #     pagMsg = {
    #         'pageNum:': pageNum,
    #         'pageSize': pageSize,
    #     }
    #     return JsonResponse(pagMsg, safe=False)
    # cursor.execute(sql)
    # mysqlcommand.conn.commit()
    # result = cursor.fetchall()
    #
    # concat = request.POST
    # postbody = request.body.decode('utf-8')
    # stuinfo = ast.literal_eval(postbody)
    # batch = stuinfo['batch']
    if (request.method == 'POST'):
        mysqlcommand = MySQLCommand()
        mysqlcommand.connectMysql()
        # sql = "SELECT * FROM gkschoolscoreline"
        cursor = mysqlcommand.conn.cursor()
        postbody = request.body.decode('utf-8')
        pageinfo = ast.literal_eval(postbody)
        sqltotalrecord ="SELECT COUNT(*) FROM gkschoolscoreline"#开始计算总页数
        cursor.execute(sqltotalrecord)
        mysqlcommand.conn.commit()
        totalRecord = cursor.fetchone()
        pageSize = pageinfo['pageSize']
        totalPageNum = int((totalRecord[0]+pageSize-1)/pageSize)#结束
        pageNum = pageinfo['pageNum']         #传递参数到这里来
        print('pageNum:',pageNum,'pageSize',pageSize)
        if pageNum <= 0:
            pageNum=1
        elif pageNum>totalPageNum:
            pageNum=totalPageNum
        prePageNum = (pageNum-1)*pageSize
        sqlSelectPage = "SELECT * FROM gkdb.gkschoolscoreline limit "+str(prePageNum)+","+str(pageSize)
        print(sqlSelectPage)
        cursor.execute(sqlSelectPage)
        mysqlcommand.conn.commit()
        pageResult = cursor.fetchall()
        mysqlcommand.closeMysql()
        myschoolscorelinelist = []
        for i in range(int(len(pageResult))):
            myschoolscorelinelist.append(
                {
                    'schoolname':pageResult[i][1],
                    'kemu':pageResult[i][2],
                    'year':pageResult[i][3],
                    'minscore':pageResult[i][4],
                    'maxscore':pageResult[i][5],
                    'averscore': pageResult[i][6],
                    'luqunum':pageResult[i][7],
                    'luqubatch': pageResult[i][8],
                }
            )
        if pageNum<=1:
            prevPage = 1
        else:
            prevPage = pageNum-1
        if pageNum >= totalPageNum:
            nextPage = totalPageNum
        else:
            nextPage = pageNum+1
        pageMsg = {
            'pageSize':pageSize,
            'totalRecord':totalRecord[0],
            'totalPageNum': totalPageNum,
            'pageNum': pageNum,
            'prevPage':prevPage,
            'nextPage':nextPage,
        }
        schoolscorelineMsg={
            'myschoolscorelinelist':myschoolscorelinelist,
            'pageMsg':pageMsg,
        }
        return JsonResponse(schoolscorelineMsg, safe=False)
@csrf_exempt
def schoolinfo(request):
    if (request.method == 'POST'):
        mysqlcommand = MySQLCommand()
        mysqlcommand.connectMysql()
        # sql = "SELECT * FROM gkschoolscoreline"
        cursor = mysqlcommand.conn.cursor()
        postbody = request.body.decode('utf-8')
        pageinfo = ast.literal_eval(postbody)
        sqltotalrecord = "SELECT COUNT(*) FROM gkschoolinfo"  # 开始计算总页数
        cursor.execute(sqltotalrecord)
        mysqlcommand.conn.commit()
        totalRecord = cursor.fetchone()
        pageSize = pageinfo['pageSize']
        totalPageNum = int((totalRecord[0] + pageSize - 1) / pageSize)  # 结束
        pageNum = pageinfo['pageNum']  # 传递参数到这里来
        print('pageNum:', pageNum, 'pageSize', pageSize)
        if pageNum <= 0:
            pageNum = 1
        elif pageNum > totalPageNum:
            pageNum = totalPageNum
        prePageNum = (pageNum - 1) * pageSize
        sqlSelectPage = "SELECT * FROM gkdb.gkschoolinfo limit " + str(prePageNum) + "," + str(pageSize)
        print(sqlSelectPage)
        cursor.execute(sqlSelectPage)
        mysqlcommand.conn.commit()
        pageResult = cursor.fetchall()
        mysqlcommand.closeMysql()
        myschoolinfolist = []
        for i in range(int(len(pageResult))):
            myschoolinfolist.append(
                {
                    'schoolname':pageResult[i][15],
                    'schoollocal':pageResult[i][2],
                    'schooltype1':pageResult[i][10],
                    'schooltype2':pageResult[i][11],
                    'schoolweb':pageResult[i][9],
                    'schoolphone':pageResult[i][7],
                }
            )
        if pageNum<=1:
            prevPage = 1
        else:
            prevPage = pageNum-1
        if pageNum >= totalPageNum:
            nextPage = totalPageNum
        else:
            nextPage = pageNum+1
        pageMsg = {
            'pageSize':pageSize,
            'totalRecord':totalRecord[0],
            'totalPageNum': totalPageNum,
            'pageNum': pageNum,
            'prevPage':prevPage,
            'nextPage':nextPage,
        }
        schoolinfoMsg = {
            'myschoolinfolist':myschoolinfolist,
            'pageMsg':pageMsg,
        }
    return JsonResponse(schoolinfoMsg, safe=False)

@csrf_exempt
def schoolrank(request):

    if (request.method == 'POST'):
        mysqlcommand = MySQLCommand()
        mysqlcommand.connectMysql()
        # sql = "SELECT * FROM gkschoolscoreline"
        cursor = mysqlcommand.conn.cursor()
        postbody = request.body.decode('utf-8')
        pageinfo = ast.literal_eval(postbody)

        sqltotalrecord ="SELECT COUNT(*) FROM gkschoolrank"#开始计算总页数
        cursor.execute(sqltotalrecord)
        mysqlcommand.conn.commit()
        totalRecord = cursor.fetchone()
        pageSize = pageinfo['pageSize']
        totalPageNum = int((totalRecord[0]+pageSize-1)/pageSize)#结束
        pageNum = pageinfo['pageNum']         #传递参数到这里来
        if pageNum <= 0:
            pageNum=1
        elif pageNum>totalPageNum:
            pageNum=totalPageNum
        prePageNum = (pageNum-1)*pageSize
        sqlSelectPage = "SELECT * FROM gkschoolrank limit "+str(prePageNum)+","+str(pageSize)
        cursor.execute(sqlSelectPage)
        mysqlcommand.conn.commit()
        pageResult = cursor.fetchall()
        mysqlcommand.closeMysql()
        # sql = "SELECT * FROM gkschoolrank"
        # cursor = mysqlcommand.conn.cursor()
        # cursor.execute(sql)
        # mysqlcommand.conn.commit()
        # result = cursor.fetchall()
        # cursor.close()
        # mysqlcommand.closeMysql()
        schoolranklist = []
        for i in range(int(len(pageResult))):
            schoolranklist.append({
                'rank':pageResult[i][1],
                'schoolname':pageResult[i][2],
                'rankscore':pageResult[i][3],
                'startrank':pageResult[i][4],
                'level':pageResult[i][5],
            })
        if pageNum<=1:
            prevPage = 1
        else:
            prevPage = pageNum-1
        if pageNum >= totalPageNum:
            nextPage = totalPageNum
        else:
            nextPage = pageNum+1
        pageMsg = {
            'pageSize':pageSize,
            'totalRecord':totalRecord[0],
            'totalPageNum': totalPageNum,
            'pageNum': pageNum,
            'prevPage':prevPage,
            'nextPage':nextPage,
        }
        schoolrankMsg ={
            'pageMsg':pageMsg,
            'schoolranklist':schoolranklist,
        }


    return JsonResponse(schoolrankMsg, safe=False)

@csrf_exempt
def register(request):
    if (request.method == 'POST'):
        isOkPsw ={}
        registerSuced = {}
        registerMsg = {}
        mysqlcommand = MySQLCommand()
        mysqlcommand.connectMysql()
        # sql = "SELECT * FROM gkschoolscoreline"
        cursor = mysqlcommand.conn.cursor()
        postbody = request.body.decode('utf-8')
        logininfo = ast.literal_eval(postbody)
        print(logininfo)
        username = logininfo['registerUserName']
        userpassword = logininfo['registerUserPsw']
        userpassword2 = logininfo['registerUserPsw2']
        if userpassword == userpassword2 :
            isOkPsw = {'OK': 1}
        else:
            isOkPsw = {'OK': 0}
            registerMsg = {
                'isOkPsw':isOkPsw,
                'registerSuced':registerSuced,
            }
            return JsonResponse(registerMsg, safe=False)
        table = "user"
        key = "username,userpassword"
        key2 = "username"
        # value = "'wangzhe','123456'"
        value = "'" + str(username) + "','" + str(userpassword) + "'"
        value2 = str(username)
        if mysqlcommand.select(table, key2, value2) == ():
            mysqlcommand.insertall(table, key, value)
            registerSuced = {
                'isSuced':1,
            }
            registerMsg = {
                'isOkPsw': isOkPsw,
                'registerSuced': registerSuced,
            }
            return JsonResponse(registerMsg, safe=False)
        else:
            registerSuced = {
                'isSuced': 0,
            }
            registerMsg = {
                'isOkPsw': isOkPsw,
                'registerSuced': registerSuced,
            }
            return JsonResponse(registerMsg, safe=False)


def logout(request):
    pass
    return redirect('/index/')
