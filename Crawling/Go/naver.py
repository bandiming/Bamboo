from selenium import webdriver
import time


class Naver:
    def __init__(self):
        self.driver = None
        self.activate()
        
        self.driver.implicitly_wait(3)

        self.sections = {'politics': 100, 'economy': 101, 'society': 102}
        self.selector = '#wrap > table > tbody > tr > td.content > div > div.ranking > ol > li.ranking_item > div.ranking_text > div.ranking_headline > a'

        self.rank_articles = None

        # TODO: test 용으로 만들긴 함. 필요한지 추후 판단
        self.links_with_section = None
        self.titles = None
        self.replies = None

    def activate(self):
        try:
            self.driver = webdriver.Chrome('')
        except:
            self.driver = webdriver.Chrome('')

    @staticmethod
    def analyze_reply(article_link, reply):
        try:
            comment_no = reply.get_attribute("data-info").split(',')[0].split(':')[1]
            content = reply.find_element_by_class_name('u_cbox_contents').text
            nickname = reply.find_element_by_class_name('u_cbox_nick').text
            date = reply.find_element_by_class_name('u_cbox_date').text
            likes = reply.find_element_by_class_name('u_cbox_cnt_recomm').text
            hates = reply.find_element_by_class_name('u_cbox_cnt_unrecomm').text

            reply_dict = {"comment_no": comment_no,
                          "content": content,
                          "nickname": nickname,
                          "date": date,
                          "likes": likes,
                          "hates": hates}

        except:
            reply_dict = None  # 정치댓글 막힌 경우?
            print("Fail Crawling", article_link)

        return reply_dict

    def uid(self, url):
        oid = self.get_param_from_url(url, "oid")
        aid = self.get_param_from_url(url, "aid")
        uid = oid + aid

        return uid

    def get_rank_articles(self, num=10):
        article_links = []
        links_with_section = []
        article_titles = []
        for section, section_num in self.sections.items():
            url = "https://news.naver.com/main/ranking/popularDay.nhn?rankingType=popular_day&sectionId={}".format(section_num)
            self.driver.get(url)
            time.sleep(1)
            titles = self.driver.find_elements_by_css_selector(self.selector)

            for i, title in enumerate(titles):
                # https://news.naver.com/main/ranking/read.nhn?rankingType=popular_day&oid=001&aid=0011239719&date=20191127&type=1&rankingSectionId=100&rankingSeq=1
                article_link = title.get_attribute("href")
                aid = self.get_param_from_url(article_link, "aid")
                oid = self.get_param_from_url(article_link, "oid")
                date = self.get_param_from_url(article_link, "date")

                article_links.append(article_link)
                links_with_section.append((article_link, str(section_num)))
                article_titles.append(title.text)
                # print("----------")
                # print(title.text)
                # print(article_link)

                if i >= num - 1:
                    break

        self.rank_articles = article_links

        self.links_with_section = links_with_section
        self.titles = article_titles

        return article_links

    @staticmethod
    def get_param_from_url(url, param):
        return url.split("{}=".format(param))[1].split("&")[0]

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
    links = naver.get_rank_articles()
    naver.quit()
