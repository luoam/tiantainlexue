# coding=utf-8
import requests
import os
import json

booklisturl = "https://www.6tiantian.com/api/student/book/list/v2?pageNumber=1&customConfigId=custom_config_id_1&pageSize=18&token=b579c098611bac59cf72e05394f7e8b4e06e4f16&tagId=1"
book_lessons_url = "https://www.6tiantian.com/api/student/book/info?customConfigId=custom_config_id_1&token=b579c098611bac59cf72e05394f7e8b4e06e4f16&bookId=%d&hasTopic=%s"

r = requests.get(booklisturl)
m = r.json()
cwd = os.getcwd()
json_dir = os.path.join(os.path.dirname(cwd), 'json')
with open(os.path.join(json_dir, 'booklist.json'), 'w') as f:
    f.write(r.text)

k = m['books']
for i in range(len(k)):
    m = k[i]
    id = m['id']
    type = m['type']
    if type == 2:
        hasTopic = "true"
    else:
        hasTopic = "false"
    q = requests.get(book_lessons_url % (id, hasTopic))
    json_books_dir = os.path.join(json_dir, "books")
    if not os.path.exists(json_books_dir):
        os.mkdir(json_books_dir)
    with open(os.path.join(json_books_dir, '%s.json' % id), 'w') as f:
        f.write(q.text)
        print('下载完毕', book_lessons_url % (id, hasTopic))

    lessons_json = q.json()
    book = lessons_json['book']
    lessons = book['lessons']
    print(lessons)
    bookid = book['id']
    json_book_dir = os.path.join(json_books_dir, str(bookid))
    if not os.path.exists(json_book_dir):
        os.mkdir(json_book_dir)
    if type == 2:
        topics = lessons['topics']

        hwType = 4
        for topic in topics:
            topicid = topic['id']
            lessonid = topic['lessonId']
            lesson_url = "https://www.6tiantian.com/api/student/book/lesson/info?mode=1&topicId=%d&hwType=%d&customConfigId=custom_config_id_1&lessonId=%d&token=b579c098611bac59cf72e05394f7e8b4e06e4f16"
            lesson_r = requests.get(lesson_url % (topicid, hwType, lessonid))
            with open(os.path.join(json_book_dir, '%d_%d.json' % (lessonid, topicid)), 'w') as f:
                f.write(q.text)
                print('     下载完毕', lesson_url % (topicid, hwType, lessonid))
    elif type == 1:
        hwType = 1
        for lesson in lessons:
            lessonid = lesson['id']
            lesson_url ="https://www.6tiantian.com/api/student/book/lesson/info?mode=1&hwType=%d&customConfigId=custom_config_id_1&lessonId=%d&token=b579c098611bac59cf72e05394f7e8b4e06e4f16"
            lesson_r = requests.get(lesson_url % (hwType, lessonid))
            with open(os.path.join(json_book_dir, '%d.json' % (lessonid)), 'w') as f:
                f.write(q.text)
                print('     下载完毕', lesson_url % (hwType, lessonid))

    elif type == 3:
        hwType = 6
        for lesson in lessons:
            lessonid = lesson['id']
            lesson_url ="https://www.6tiantian.com/api/student/book/lesson/info?mode=1&hwType=%d&customConfigId=custom_config_id_1&lessonId=%d&token=b579c098611bac59cf72e05394f7e8b4e06e4f16"
            lesson_r = requests.get(lesson_url % (hwType, lessonid))
            with open(os.path.join(json_book_dir, '%d.json' % (lessonid)), 'w') as f:
                f.write(q.text)
                print('     下载完毕', lesson_url % (hwType, lessonid))
    elif type == 6:
        hwType = 10
        for lesson in lessons:
            lessonid = lesson['id']
            lesson_url ="https://www.6tiantian.com/api/student/book/lesson/info?mode=1&hwType=%d&customConfigId=custom_config_id_1&lessonId=%d&token=b579c098611bac59cf72e05394f7e8b4e06e4f16"
            lesson_r = requests.get(lesson_url % (hwType, lessonid))
            with open(os.path.join(json_book_dir, '%d.json' % (lessonid)), 'w') as f:
                f.write(q.text)
                print('     下载完毕', lesson_url % (hwType, lessonid))
