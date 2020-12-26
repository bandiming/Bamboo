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

    def activate(self):
        try:
            self.driver = webdriver.Chrome('/Users/ichangmin/Drivers/chromedriver')
        except:
            self.driver = webdriver.Chrome('/Users/changmin/Drivers/chromedriver')


    @staticmethod
    def get_param_from_url(url, param):
        return url.split("{}=".format(param))[1].split("&")[0]

    def analyze_content(self, content):
        # print(content.get_attribute('innerHTML'))
        a_tags = content.find_elements_by_tag_name("a")
        reply_data = []
        for a_tag in a_tags:
            url = a_tag.get_attribute("title")
            # print(url)

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
        self.new_tweets = []
        time.sleep(5)
        # tweets = self.driver.find_elements_by_class_name('js-stream-item')
        # tweets = self.driver.find_elements_by_css_selector(
        #     '.css-4rbku5.css-18t94o4.css-901oao.r-111h2gw.r-1loqt21.r-1q142lx.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-3s2u2q.r-qvutc0')

        tweets = self.driver.find_elements_by_css_selector(
            '.css-1dbjc4n.r-1ila09b.r-qklmqi.r-1adg3ll'
        )

        print("{} tweets available".format(len(tweets)))
        for i, tweet in enumerate(tweets):
            tweet_data = {}
            try:
                title_div = tweet.find_element_by_css_selector('.css-4rbku5.css-18t94o4.css-901oao.r-111h2gw.r-1loqt21.r-1q142lx.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-3s2u2q.r-qvutc0')
            except:
                break
            tweet_uid = title_div.get_attribute('href').split('/')[-1]

            date = tweet.find_element_by_tag_name('time').get_attribute('datetime').split('.')[0]

            if len(Tweet.find(tweet_uid)) != 0:
                print("Tweet already checked")
                break

            username = tweet.find_elements_by_css_selector('.css-901oao.css-16my406.r-1qd0xha.r-ad9z0x.r-bcqeeo.r-qvutc0')[2].text

            content = tweet.find_element_by_css_selector('.css-901oao.r-jwli3a.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-bnwqim.r-qvutc0')

            reply_data = self.analyze_content(content)
            # print(reply_data)

            tweet_data['tweet_uid'] = tweet_uid
            tweet_data['username'] = username
            tweet_data['content'] = content.get_attribute('innerHTML')
            tweet_data['date'] = date
            tweet_data['reply_data'] = reply_data
            self.new_tweets.append(tweet_data)
            print(username)
            # TODO: 이미지 처리 직접 글 업로드 해보면서 감 잡기

        return self.new_tweets

    def get_best_replies(self, article_link):
        self.driver.get(article_link)
        time.sleep(1)
        reply_boxes = self.driver.find_elements_by_class_name('u_cbox_comment')

        for box in reply_boxes:

            comment_no = box.get_attribute("data-info").split(',')[0].split(':')[1]
            content = box.find_element_by_class_name('u_cbox_contents')
            nickname = box.find_element_by_class_name('u_cbox_nick').text
            date = box.find_element_by_class_name('u_cbox_date').text
            like = box.find_element_by_class_name('u_cbox_cnt_recomm').text
            unlike = box.find_element_by_class_name('u_cbox_cnt_unrecomm').text


    def quit(self):
        self.driver.quit()

if __name__ == '__main__':
    twitter = Twitter()
    # tweets = twitter.get_tweets(test=True)
    # Tweet.create(tweets)
    tweets = twitter.get_tweets()

    # get_best_replies("https://news.naver.com/main/ranking/read.nhn?rankingType=popular_day&oid=001&aid=0011239718&date=20191127&type=1&rankingSectionId=100&rankingSeq=1")

    twitter.quit()
