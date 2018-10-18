import requests
import os
import pymysql
import json
import logging
import time


def dbconnection():
    host = "127.0.0.1"
    user = "root"
    password = "123456"
    database = "tiantianlexue"
    dbconn = pymysql.connect(host, user, password, database, charset="utf8")
    return dbconn


def getbooksjson(iid):
    booklisturl = "https://6tiantian.com/api/student/book/list/v2?pageNumber=1&customConfigId=custom_config_id_1&pageSize=188&token=b579c098611bac59cf72e05394f7e8b47c6c3914&tagId=%d" % iid
    r = requests.get(booklisturl)
    r_json = r.json()
    books = r_json['books']
    dbconn = dbconnection()
    cursor = dbconn.cursor()
    for book in books:
        bookid = book['id']
        type = book['type']
        coverUrl = book['coverUrl']
        coverLandscapeUrl = book['coverLandscapeUrl']
        info = book['info']
        info = dbconn.escape_string(info)
        brief = book['brief']
        # brief = dbconn.escape_string(brief)
        tagid = iid
        sql = "insert into books(bookid,type,coverUrl,coverLandscapeUrl,info,brief,tagid) values (%d,%d,'%s','%s','%s','%s',%d)" % (
            bookid, type, coverUrl, coverLandscapeUrl, info, brief, tagid)
        try:
            cursor.execute(sql)
            dbconn.commit()
            print("获取bookid %d" % bookid)
            getlesson(dbconn, bookid, type)
        except BaseException:
            dbconn.rollback()
            print("获取bookid %d 未处理" % bookid)

    dbconn.close()


def getlesson(dbconn, bookid, type):
    cursor = dbconn.cursor()
    book_lessons_url = "https://6tiantian.com/api/student/book/info?customConfigId=custom_config_id_1&token=b579c098611bac59cf72e05394f7e8b47c6c3914&bookId=%d&hasTopic=%s"
    if type == 2:
        hasTopic = "true"
    else:
        hasTopic = "false"
    q = requests.get(book_lessons_url % (bookid, hasTopic))
    json_q = q.json()
    book = json_q['book']
    lessons = book['lessons']
    for lesson in lessons:
        lessonid = lesson['id']
        info = lesson['info']
        info = dbconn.escape_string(info)
        imgLandscapeUrl = lesson['imgLandscapeUrl']
        imgPortraitUrl = lesson['imgPortraitUrl']
        if imgPortraitUrl is None:
            imgPortraitUrl = ""
        if imgLandscapeUrl is None:
            imgLandscapeUrl = ""
        sql = "insert into lessons(lessonid,bookid,imgLandscapeUrl,imgPortraitUrl,info) values (%d,%d,'%s','%s','%s')" % (
            lessonid, bookid, imgLandscapeUrl, imgPortraitUrl, info)
        try:
            cursor.execute(sql)
            dbconn.commit()
            print("      lessonid %d保存数据库成功" % lessonid)
            writelesson(lessonid, type)
        except BaseException:
            dbconn.rollback()
            print("      lessonid %d 课程未保存" % lessonid)


def writelesson(lessonid, type):
    json_dir = os.path.join(os.getcwd(), 'json')
    with open(os.path.join(json_dir, 'lessons.txt'), 'a+') as f:
        f.writelines("%d,%d\n" % (lessonid, type))
        print("        %d课程保存完毕" % lessonid)


def gettopicandquestion():
    json_dir = os.path.join(os.getcwd(), 'json')
    with open(os.path.join(json_dir, 'lessons.txt'), 'r') as f:
        lines = f.readlines()
        for line in lines:
            print(line)
            str = line.split(',')
            lessonid = int(str[0])
            type = int(str[1])
            dbconn = dbconnection()
            cursor = dbconn.cursor()
            hwtype = 0
            if type == 1:
                hwtype = 1
            elif type == 2:
                hwtype = 4
            elif type == 3:
                hwtype = 6
            elif type == 4:
                hwtype = 8
            elif type == 6:
                hwtype = 10
            lesson_url = "https://www.6tiantian.com/api/student/book/lesson/info?mode=1&hwType=%d&customConfigId=custom_config_id_1&lessonId=%d&token=b579c098611bac59cf72e05394f7e8b47c6c3914"
            try:
                q = requests.get(lesson_url % (hwtype, lessonid))
                json_q = q.json()
                homework = json_q['homework']
                topics = homework['topics']
                for topic in topics:
                    topicid = topic['id']
                    foreignTitle = topic['foreignTitle']
                    foreignTitle = dbconn.escape_string(foreignTitle)
                    nativeTitle = topic['nativeTitle']
                    imgUrl = topic['imgUrl']
                    mediaUrl = topic['mediaUrl']
                    mediaType = topic['mediaType']
                    type = topic['type']
                    sql = "insert into topics (topicid,lessonid,foreignTitle,nativeTitle,imgUrl,mediaUrl,mediaType,type)values (%d,%d,'%s','%s','%s','%s','%d',%d)" % (
                        topicid, lessonid, foreignTitle, nativeTitle, imgUrl, mediaUrl, mediaType, type)
                    cursor.execute(sql)
                    dbconn.commit()
                    print("topicid %d保存成功" % topicid)
                    questions = topic['questions']
                    for question in questions:
                        questionid = question['id']
                        imageUrl = question['imageUrl']
                        foreignText = question['foreignText']
                        foreignText = dbconn.escape_string(foreignText)
                        evalText = question['evalText']
                        evalText = dbconn.escape_string(evalText)
                        timeline = question['timeline']
                        timeline = json.dumps(timeline)
                        timeline = dbconn.escape_string(timeline)
                        clickReadInfo = question['clickReadInfo']
                        if clickReadInfo is None:
                            clickReadInfo = ""
                        clickReadInfo = json.dumps(clickReadInfo)
                        clickReadInfo = dbconn.escape_string(clickReadInfo)
                        dubConfig = question['dubConfig']
                        if dubConfig is None:
                            dubConfig = ""
                        dubConfig = json.dumps(dubConfig)
                        dubConfig = dbconn.escape_string(dubConfig)
                        nativeText = question['nativeText']
                        if nativeText is None:
                            nativeText = ""
                        nativeText = dbconn.escape_string(nativeText)
                        audioUrl = question['audioUrl']
                        type = question['type']
                        sql = "insert into questions(questionid,topicid,audioUrl,imageUrl,foreignText,nativeText,evalText,timeline,clickReadInfo,dubConfig,type)values (%d,%d,'%s','%s','%s','%s','%s','%s','%s','%s',%d)" % (
                            questionid, topicid, audioUrl, imageUrl, foreignText, nativeText, evalText, timeline,
                            clickReadInfo, dubConfig, type)
                        try:
                            cursor.execute(sql)
                            dbconn.commit()
                            print("      questionid %d保存成功" % questionid)
                        except:
                            json_dir = os.path.join(os.getcwd(), '/')
                            with open(os.path.join(json_dir, 'sql.log'), 'a+') as f:
                                f.writelines(lesson_url % (hwtype, lessonid))
                                f.writelines("\n")
            except:
                json_dir = os.path.join(os.getcwd(), '/')
                with open(os.path.join(json_dir, 'log.log'), 'a+') as f:
                    f.writelines(lesson_url % (hwtype, lessonid))
                    f.writelines("\n")
                print("出现错误%s" % lesson_url)



# category = (1,2,3,4,230,2781)
# for x in (category):
#     getbooksjson(x)

gettopicandquestion()
