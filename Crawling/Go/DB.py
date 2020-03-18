import mysql.connector
import os
import time

username = os.environ['BAMBOO_USER']
passwd = os.environ['BAMBOO_PASSWORD']
dbname = os.environ['BAMBOO_DB']

db = mysql.connector.connect(
    host='localhost',
    passwd=passwd,
    database=dbname,
    user=username
)


def now():
    return time.strftime('%Y-%m-%d %H:%M:%S')

def date_to_now(date):
    #"2019.12.19. 09:45:51"
    split = [x.strip() for x in date.split('.')]  # ['2019', '12', '19', '09:45:51']
    year = split[0]
    month = split[1]
    day = split[2]

    hms = split[3].split(':')
    hour = hms[0]
    minutes = hms[1]
    if len(hms) == 3:
        seconds = hms[2]
    else:
        seconds = "00"
    return "{}-{}-{} {}:{}:{}".format(year, month, day, hour, minutes, seconds)


class Article:
    @staticmethod
    def find(uid):
        query = "SELECT * FROM articles WHERE (uid = {})".format(uid)
        cursor = db.cursor(dictionary=True)
        cursor.execute(query)

        return cursor.fetchall()

    @staticmethod
    def create(section, title, oid, aid, uid, date):
        # database.new_article(section, title, oid, aid, uid, date)
        cursor = db.cursor()
        created_at = now()
        sql = "INSERT INTO articles (title, uid, aid, oid, section, date, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (title, uid, aid, oid, section, date, created_at, created_at)
        cursor.execute(sql, val)
        db.commit()

        print("new article inserted.")

    def replies(self, uid, Reply):
        art = self.find(uid)
        replies = Reply.where(article_id=art.id)

        query = "SELECT * FROM replies WHERE (replies.article_id = {})".format(art.id)
        cursor = db.cursor(dictionary=True)
        cursor.execute(query)

        return cursor.fetchall()


class Reply:
    @staticmethod
    def find(article_uid, comment_no):
        query = "SELECT * FROM replies WHERE (article_uid = {} AND comment_no = {})".format(article_uid, comment_no)
        cursor = db.cursor(dictionary=True)
        cursor.execute(query)

        return cursor.fetchall()

    @staticmethod
    def create(data):
        article_uid = data["article_uid"]
        comment_id = data["comment_no"]
        content = data["content"]
        nickname = data["nickname"]
        date = data["date"]


        # database.new_article(section, title, oid, aid, uid, date)
        cursor = db.cursor()
        created_at = now()
        sql = "INSERT INTO replies (article_uid, comment_no, content, nickname, date, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (article_uid, comment_id, content, nickname, date, created_at, created_at)
        cursor.execute(sql, val)
        db.commit()

        print("new reply inserted.")

        History.create(data, first=True)


class History:
    @staticmethod
    def create(data, first=False):

        article_uid = data["article_uid"]
        comment_no = data["comment_no"]
        likes = data["likes"]
        hates = data["hates"]

        cursor = db.cursor()
        if first:
            created_at = date_to_now(data["date"])
            likes = 0
            hates = 0
            print(created_at)

        else:
            created_at = now()
        sql = "INSERT INTO histories (article_uid, comment_no, likes, hates, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (article_uid, comment_no, likes, hates, created_at, created_at)
        cursor.execute(sql, val)
        db.commit()


class Tweet:
    def __init__(self):
        self.tweet_id = None
        self.username = None
        self.content = None
        self.date = None
        self.comment_no = None
        self.article_uid = None

    @staticmethod
    def find(tweet_uid):
        query = "SELECT * FROM tweets WHERE (tweet_uid = {})".format(tweet_uid)
        cursor = db.cursor(dictionary=True)
        cursor.execute(query)

        return cursor.fetchall()

    @staticmethod
    def create(data):
        tweet_uid = data['tweet_uid']
        username = data['username']
        content = data['content']
        date = data['date']
        reply_data = data['reply_data']

        for article_uid, comment_no in reply_data:  # article id => uid

            cursor = db.cursor()
            created_at = now()
            sql = "INSERT INTO tweets (comment_no, article_uid, tweet_uid, username, content, date, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (comment_no, article_uid, tweet_uid, username, content, date, created_at, created_at)
            cursor.execute(sql, val)
            db.commit()
            

# cursor = db.cursor()
# sql = "INSERT INTO customer (name, address) VALUES (%s, %s)"
# val = [("good", "sinchon")]
# cursor.executemany(sql, val)
# db.commit()
# print(cursor.rowcount, "records inserted.")


if __name__ == '__main__':
    from selenium import webdriver
    from naver import Naver

    print(Tweet.find("12072200552613724183"))

    '''
    naver_crawler = Naver()
    naver_crawler.get_rank_articles()

    for i, link in enumerate(naver_crawler.rank_articles):
        section = naver_crawler.links_with_section[i][1]
        title = naver_crawler.titles[i]
        oid = naver_crawler.get_param_from_url(link, "oid")
        aid = naver_crawler.get_param_from_url(link, "aid")
        uid = oid + aid
        date = naver_crawler.get_param_from_url(link, "date")

        database.new_article(section, title, oid, aid, uid, date)

    naver_crawler.quit()
    '''

