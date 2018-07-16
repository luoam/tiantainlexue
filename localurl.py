import pymysql
from threading import Thread
from multiprocessing import Process


def dbconnection():
    host = "127.0.0.1"
    user = "root"
    password = "123456"
    database = "tiantianlexue"
    dbconn = pymysql.connect(host, user, password, database, charset="utf8")
    return dbconn

def booksurl():
    dbconn = dbconnection()
    cursor = dbconn.cursor()
    sql = "select coverUrl,coverLandscapeUrl from books"
    cursor.execute(sql)
    results = cursor.fetchall()
    for result in results:
        coverUrl = result[0]
        coverLandscapeUrl = result[1]
        sql = "insert into urls (url)values ('%s')"%coverUrl
        sqll = "insert into urls (url) values ('%s')"%coverLandscapeUrl
        try:
            cursor.execute(sql)
            cursor.execute(sqll)
            dbconn.commit()
            print("okbooks")
        except:
            print("error")
    dbconn.close()

def lessonsurl():
    dbconn = dbconnection()
    cursor = dbconn.cursor()
    sql = "select imgLandscapeUrl,imgPortraitUrl from lessons"
    cursor.execute(sql)
    results = cursor.fetchall()
    for result in results:
        imgLandscapeUrl = result[0]
        imgPortraitUrl = result[1]
        try:
            if len(imgLandscapeUrl)>5:
                sql ="insert into urls(url) values ('%s')"%imgLandscapeUrl
                cursor.execute(sql)
            if len(imgPortraitUrl)>5:
                sql ="insert into urls(url) values ('%s')"%imgPortraitUrl
                cursor.execute(sql)
            dbconn.commit()
            print("oklessons")
        except:
            print("error")

def questionsurl():
    dbconn = dbconnection()
    cursor = dbconn.cursor()
    sql = "select audioUrl from questions"
    cursor.execute(sql)
    results = cursor.fetchall()
    for result in results:
        audioUrl=result[0]
        if len(audioUrl)>5:
            try:
                sql = "insert into urls (url) values ('%s')"%audioUrl
                cursor.execute(sql)
                dbconn.commit()
                print("okquestions")
            except:
                print("error")

def topicsurl():
    dbconn = dbconnection()
    cursor = dbconn.cursor()
    sql = "select imgUrl,mediaUrl from topics"
    cursor.execute(sql)
    results = cursor.fetchall()
    for result in results:
        imgurl=result[0]
        mediaUrl=result[1]
        if len(imgurl)>5:
            try:
                sql = "insert into urls (url) values ('%s')"%imgurl
                cursor.execute(sql)
                dbconn.commit()
                print("oktopic")
            except:
                print("error")

        if len(mediaUrl)>5:
            try:
                sql = "insert into urls (url) values ('%s')"%mediaUrl
                cursor.execute(sql)
                dbconn.commit()
                print("oktopic")
            except:
                print("error")



#booksurl()
#lessonsurl()


# questionsurl()
# topicsurl()
t3 = Process(target=booksurl)
t4 = Process(target=lessonsurl)
t1 = Process(target=questionsurl)
t2 = Process(target=topicsurl)

t3.start()
t4.start()
t1.start()
t2.start()