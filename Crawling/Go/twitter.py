# Xpath: https://www.guru99.com/xpath-selenium.html
from selenium import webdriver
import time
from datetime import datetime
try:
    from Go.DB import Tweet
except:
    from DB import Tweet


class Twitter:
    def __init__(self):
        self.driver = None
        self.activate()
        
        self.driver.implicitly_wait(3)
        self.article_links = None
        self.new_tweets = []

        self.xpath_name = None
        self.xpath_user_id = None
        self.xpath_content = None

    def activate(self):
        try:
            self.driver = webdriver.Chrome('/Users/ichangmin/driver/chromedriver')
        except:
            self.driver = webdriver.Chrome('/Users/changmin/Drivers/chromedriver')


    # def update_xpaths(self):
    #     # self.driver.find_elements_by_xpath("//*[contains(text(), 'My Button')]")
    #     # print(self.driver.find_element_by_xpath("//*[text()='JM']").get_attribute("class"))

    # def get_xpath():
    # /html/body/div/div/div/div[2]/main/div/div/div/div/div/div[2]/div/section/div/div/div[1]/div/div/article/div/div/div/div[2]/div[2]/div/div/div/div[1]/a/div/div[1]/div[1]/span/span
    # #react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div > div > div:nth-child(2) > div > section > div > div > div:nth-child(1) > div > div > article > div > div > div > div.css-1dbjc4n.r-18u37iz.r-d0pm55 > div.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci > div > div > div > div.css-1dbjc4n.r-1wbh5a2.r-dnmrzs > a > div

    def run(self):
        # 1. reference tweet에서 class name 가져오기
        #
        #

        self.driver.get("https://mobile.twitter.com/search?q=n.news.naver.com%2Farticle%2Fcomment%2F&src=typed_query&f=live")
        class_name = self.driver.find_element_by_xpath("//*[text()='JM']").get_attribute("class")
        print(class_name.replace(" ", "."))
        elements = self.driver.find_elements_by_css_selector("span."+class_name.replace(" ", ".") + " > " + "span."+class_name.replace(" ", "."))
        print(len(elements))
        for e in elements:
            print(e.text)


    @staticmethod
    def get_param_from_url(url, param):
        return url.split("{}=".format(param))[1].split("&")[0]

    def analyze_content(self, content):
        # print(content.text)
        a_tags = content.find_elements_by_tag_name("a")
        reply_data = []
        for a_tag in a_tags:
            url = a_tag.get_attribute("data-expanded-url")

            try:
                # TODO: except 처리 detail
                if "news.naver.com" in url:
                    comment_no = self.get_param_from_url(url, "commentNo")
                    oid = self.get_param_from_url(url, "oid")
                    aid = self.get_param_from_url(url, "aid")

                    uid = oid + aid

                    reply_data.append((uid, comment_no))

                    # print("No: {} oid: {} aid: {}".format(comment_no, oid, aid))
            except:
                print("url none")

        return reply_data





    def get_tweets(self, test=False):
        self.article_links = []
        url = "https://twitter.com/search?q=news.naver.com%2Fcomment&src=unkn&f=live&vertical=default"
        self.driver.get(url)
        time.sleep(5)
        # tweets = self.driver.find_elements_by_class_name('js-stream-item')
        tweets = self.driver.find_elements_by_css_selector('.css-4rbku5.css-18t94o4.css-901oao.r-111h2gw.r-1loqt21.r-1q142lx.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-3s2u2q.r-qvutc0')
        for t in tweets:
            print(t.get_attribute('href').split('/')[-1])
        exit(0)

        self.new_tweets = []
        print("{} tweets available".format(len(tweets)))
        for i, tweet in enumerate(tweets):
            tweet_uid = tweet.get_attribute("data-item-id")

            if len(Tweet.find(tweet_uid)) != 0:
                print("Tweet already checked")
                break

            tweet_data = {}

            username = tweet.find_element_by_class_name('username').text
            content = tweet.find_element_by_class_name('js-tweet-text')
            timestamp = tweet.find_element_by_class_name('_timestamp').get_attribute('data-time')
            date = datetime.fromtimestamp(int(timestamp))

            reply_data = self.analyze_content(content)

            tweet_data['tweet_uid'] = tweet_uid
            tweet_data['username'] = username
            tweet_data['content'] = content.get_attribute('innerHTML')
            tweet_data['date'] = date
            tweet_data['reply_data'] = reply_data
            self.new_tweets.append(tweet_data)

            # TODO: 이미지 처리 직접 글 업로드 해보면서 감 잡기

        return self.new_tweets


    def quit(self):
        self.driver.quit()

if __name__ == '__main__':
    twitter = Twitter()
    twitter.run()
    twitter.quit()
