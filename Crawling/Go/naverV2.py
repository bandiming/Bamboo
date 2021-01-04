# 201226
from selenium import webdriver
from data.presses import PRESSES
import time
from DB import Article, Reply, History


class Press:
    def __init__(self, name, section_num):
        self.name = name
        self.section_num = section_num
        self.ranking_url = "https://news.naver.com/main/ranking/office.nhn?officeId={}".format(section_num)


class Naver:
    def __init__(self):
        self.driver = None
        self.presses = []
        self.init_presses()
        self.activate()
        
        self.driver.implicitly_wait(3)


        self.article_links = []

        self.article_table = Article()
        self.reply_table = Reply()
        self.history_table = History()



    def init_presses(self):
        for press in PRESSES:
            self.presses.append(Press(press[1], press[0]))

    def activate(self):
        try:
            self.driver = webdriver.Chrome('/Users/ichangmin/driver/chromedriver')
        except:
            self.driver = webdriver.Chrome('/Users/changmin/Drivers/chromedriver')

    def update_article_urls(self, num=10):
        self.article_links = []

        for press in self.presses:
            self.driver.get(press.ranking_url)
            self.driver.implicitly_wait(1)

            elements = self.driver.find_elements_by_css_selector(".list_content > a")[:num]

            urls = [e.get_attribute('href') for e in elements]
            # TODO: db 여기서 확인하기

            self.article_links += urls

    def get_uids(self, url):
        #https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=001&oid=088&aid=0000678594

        split_url = url.split("&")

        oid, aid, sid = None, None, None

        for word in split_url:
            if "oid" in word:
                oid = word.split("=")[1]
            elif "aid" in word:
                aid = word.split("=")[1]
            elif "sid" in word:
                sid = word.split("=")[1]

        return oid, aid, sid

    def get_best_replies(self, oid, aid):
        pass

    # 기사 링크에서
    def get_article_data(self):
        title = self.driver.find_element_by_id("articleTitle").text
        date = self.driver.find_element_by_class_name("t11").text
        split_date = date.split(" ")
        date = split_date[0].replace(".", "")

        article_time = split_date[1]

        return title, date, article_time

    def parse_replies(self, oid, aid, sid):
        url = "https://news.naver.com/main/ranking/read.nhn?m_view=1&includeAllCount=true&mode=LSD&mid=sec&sid1={}&oid={}&aid={}".format(sid, oid, aid)
        self.driver.get(url)
        self.driver.implicitly_wait(1)

        replies_count = int(self.driver.find_element_by_class_name("u_cbox_count").text.replace(",", ""))
        num_clicks = int(replies_count/20)

        # 리플 20개씩 로드 됨
        for _ in range(num_clicks):
            self.driver.find_element_by_css_selector("a.u_cbox_btn_more").click()
            self.driver.implicitly_wait(1)

        reply_boxes = self.driver.find_elements_by_class_name('u_cbox_comment_box')

        count = 0
        for reply_box in reply_boxes:
            try:
                count += 1
                content = reply_box.find_element_by_class_name("u_cbox_contents").text
                print(content)
                print("")
            except:
                # 삭제된 댓글
                continue


        print("\n 총 {} 개의 리플 중 {}개 파싱".format(replies_count, count))


    def run(self, article_num=10):
        # 1. 랭킹 확인
        # 2. 기사 uid 확인 후 기존 데이터 없으면 insert (oid, aid, uid, title, time)
        # 3. 댓글 크롤링: comment num 확인하고 없으면 insert
        # 4. 좋아요 / 싫어요 row 추가

        self.update_article_urls(num=article_num)
        for url in self.article_links:
            self.driver.get(url)
            self.driver.implicitly_wait(1)

            oid, aid, sid = self.get_uids(url)
            uid = oid + aid
            result = self.article_table.find(uid)

            if len(result) == 0:
                title, date, article_time = self.get_article_data()
                Article.create("", title, oid, aid, uid, sid, date, article_time)

            self.parse_replies(oid, aid, sid)












    @staticmethod
    def analyze_reply(article_link, reply):
        try:
            comment_no = reply.get_attribute("data-info").split(',')[0].split(':')[1]
            content = reply.find_element_by_class_name('u_cbox_contents').text
            nickname = reply.find_element_by_class_name('u_cbox_nick').text
            date = reply.find_element_by_class_name('u_cbox_date').text
            likes = reply.find_element_by_class_name('u_cbox_cnt_recomm').text
            hates = reply.find_element_by_class_name('u_cbox_cnt_unrecomm').text

            reply_dict = {
                "comment_no": comment_no,
                "content": content,
                "nickname": nickname,
                "date": date,
                "likes": likes,
                "hates": hates
            }

        except:
            reply_dict = None  # 정치댓글 막힌 경우?
            print("Fail Crawling", article_link)

        return reply_dict


    def get_best_replies(self, article_link):
        self.driver.get(article_link)

        time.sleep(1)
        reply_boxes = self.driver.find_elements_by_class_name('u_cbox_comment')

        self.replies = reply_boxes

    def update_reply_likes(self):
        # TODO: save best replies likes data for rank articles

        pass

    def quit(self):
        self.driver.quit()



if __name__ == '__main__':
    naver = Naver()
    naver.run(article_num=3)
    naver.quit()
