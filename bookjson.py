import requests
import os
import pymongo


def getbooklist():
    booklisturl = "https://www.6tiantian.com/api/student/book/list/v2?pageNumber=1&customConfigId=custom_config_id_1&pageSize=18&token=b579c098611bac59cf72e05394f7e8b4e06e4f16&tagId=1"
    r = requests.get(booklisturl)
    json = r.json()
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    mydb = myclient['tiantianlexue']
    booklist = mydb["booklist"]
    y = booklist.find_one()
    if y:
        print("文档已经存")
    else:
        x = booklist.insert_one(json)
        print(x)
    return json


booklist = getbooklist()
books = booklist['books']
myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient['tiantianlexue']
booklessons = mydb["booklessons"]
y = booklessons.find_one()
if y is None:
    for book in books:
        id = book['id']
        type = book['type']
        if type == 2:
            hasTopic = "true"
        else:
            hasTopic = "false"
        book_lessons_url = "https://www.6tiantian.com/api/student/book/info?customConfigId=custom_config_id_1&token=b579c098611bac59cf72e05394f7e8b4e06e4f16&bookId=%d&hasTopic=%s"
        r = requests.get(book_lessons_url % (id, hasTopic))
        booklessons.insert_one(r.json())
        print(r.json())
else:
    print("全部的书已经有了")
