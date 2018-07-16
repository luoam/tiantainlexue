import requests
import os
import pymysql
import json


def dbconnection():
    host = "127.0.0.1"
    user = "root"
    password = "123456"
    database = "tiantianlexue"
    dbconn = pymysql.connect(host, user, password, database, charset="utf8")
    return dbconn


def getbooksjson():
    booklisturl = "https://www.6tiantian.com/api/student/book/list/v2?pageNumber=1&customConfigId=custom_config_id_1&pageSize=18&token=b579c098611bac59cf72e05394f7e8b4e06e4f16&tagId=1"
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
        print(id, type, coverUrl, coverLandscapeUrl, info)
        sql = "insert into books(bookid,type,coverUrl,coverLandscapeUrl,info) values (%d,%d,'%s','%s','%s')" % (
            bookid, type, coverUrl, coverLandscapeUrl, info)
        try:
            cursor.execute(sql)
            dbconn.commit()
            print("bookid %d" % bookid)
            getlesson(dbconn, bookid, type)
        except:
            print("bookid %d error" % bookid)
        finally:
            pass
    dbconn.close()


def getlesson(dbconn, bookid, type):
    cursor = dbconn.cursor()
    book_lessons_url = "https://www.6tiantian.com/api/student/book/info?customConfigId=custom_config_id_1&token=b579c098611bac59cf72e05394f7e8b4e06e4f16&bookId=%d&hasTopic=%s"
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
            print("lessonid %d" % lessonid)
            writelesson(lessonid, type)
        except:
            print("lessonid %d error" % lessonid)
            print(sql)


def writelesson(lessonid, type):
    json_dir = os.path.join(os.getcwd(), 'json')
    print(json_dir)
    with open(os.path.join(json_dir, 'lessons.txt'), 'a+') as f:
        f.writelines("%d,%d\n" % (lessonid, type))
        print("%dok" % lessonid)


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
            elif type == 6:
                hwtype = 10
            lesson_url = "https://www.6tiantian.com/api/student/book/lesson/info?mode=1&hwType=%d&customConfigId=custom_config_id_1&lessonId=%d&token=b579c098611bac59cf72e05394f7e8b4e06e4f16"
            q = requests.get(lesson_url % (hwtype, lessonid))
            try:
                json_q = q.json()
                homework = json_q['homework']
                topics = homework['topics']
                for topic in topics:
                    topicid = topic['id']
                    print(topicid)
                    foreignTitle = topic['foreignTitle']
                    foreignTitle = dbconn.escape_string(foreignTitle)
                    imgUrl = topic['imgUrl']
                    mediaUrl = topic['mediaUrl']
                    mediaType = topic['mediaType']
                    sql = "insert into topics (topicid,lessonid,foreignTitle,imgUrl,mediaUrl,mediaType)values (%d,%d,'%s','%s','%s',%d)" % (
                        topicid, lessonid, foreignTitle, imgUrl, mediaUrl, mediaType)
                    cursor.execute(sql)
                    dbconn.commit()
                    print("topicid %d" % topicid)
                    questions = topic['questions']
                    for question in questions:
                        questionid = question['id']
                        foreignText = question['foreignText']
                        foreignText = dbconn.escape_string(foreignText)
                        evalText = question['evalText']
                        evalText = dbconn.escape_string(evalText)
                        timeline = question['timeline']
                        timeline = json.dumps(timeline)
                        timeline = dbconn.escape_string(timeline)
                        clickReadInfo = question['clickReadInfo']
                        clickReadInfo = json.dumps(clickReadInfo)
                        clickReadInfo = dbconn.escape_string(clickReadInfo)
                        nativeText = question['nativeText']
                        if nativeText is None:
                            nativeText=""
                        nativeText = dbconn.escape_string(nativeText)
                        audioUrl = question['audioUrl']
                        sql = "insert into questions(questionid,topicid,foreignText,evalText,timeline,clickReadInfo,audioUrl,nativeText)values (%d,%d,'%s','%s','%s','%s','%s','%s')" % (
                            questionid, topicid, foreignText, evalText, timeline, clickReadInfo,audioUrl,nativeText)
                        try:
                            cursor.execute(sql)
                            dbconn.commit()
                            print("questionid %d" % questionid)
                        except:
                            print(sql)
            except:
                print(q.url)


# getbooksjson()

gettopicandquestion()
