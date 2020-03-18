import time
from Go.DB import Article, Reply, History, Tweet
from Go.naver import Naver
from Go.twitterV2 import Twitter
import datetime


class Crawler:
    def __init__(self):
        self.naver = Naver()
        self.twitter = Twitter()
        self.article = Article()

    def activate(self):
        self.naver.activate()
        self.twitter.activate()

    def quit(self):
        self.twitter.quit()
        self.naver.quit()

    def update_replies(self, article, article_link, uid):
        print("update replies")

        self.naver.get_best_replies(article_link)
        for reply in self.naver.replies:
            reply_data = self.naver.analyze_reply(article_link, reply)
            if reply_data is None:
                continue

            reply_data["article_uid"] = uid
            re = Reply.find(uid, reply_data["comment_no"])

            if len(re) == 0:
                Reply.create(reply_data)

            History.create(reply_data)

    def check_articles(self, num=10):
        self.naver.get_rank_articles(num=num)
        for i in range(len(self.naver.rank_articles)):
            article_link, section = self.naver.links_with_section[i]
            title = self.naver.titles[i]
            uid = self.naver.uid(article_link)

            article = Article.find(uid)

            print("crawling", article_link)

            if len(article) == 0:
                oid = self.naver.get_param_from_url(article_link, "oid")
                aid = self.naver.get_param_from_url(article_link, "aid")
                date = self.naver.get_param_from_url(article_link, "date")

                self.article.create(section, title, oid, aid, uid, date)
                print("new article inserted")
            else:
                print("found article!")

            self.update_replies(article, article_link, uid)

    def check_tweets(self):
        new_tweets = self.twitter.get_tweets()
        print("{} new tweets".format(len(new_tweets)))
        for tweet in new_tweets:
            Tweet.create(tweet)
            print("1 tweet inserted")


if __name__ == '__main__':
    crawler = Crawler()
    while True:
        hour = datetime.datetime.now().hour
        if 2 < hour < 5:
            time.sleep(600)
            continue

        crawler.check_articles(10)  # update article, replies
        crawler.check_tweets()

        crawler.quit()

        print("waiting..")
        time.sleep(600)
        crawler.activate()

