from selenium import webdriver
from time import sleep

driver = webdriver.Chrome('/Users/ichangmin/Drivers/chromedriver')
driver.implicitly_wait(3)

driver.get('https://m.news.naver.com/comment/list.nhn?commentNo=1940463305&gno=news025,0002951467&mode=LSD=sec&sid1=001&oid=025&aid=0002951467')


def crawl():
    class_lists = driver.find_elements_by_class_name('u_cbox_area')
    lists = []
    for l in class_lists:
        try:
            content = l.find_element_by_class_name('u_cbox_text_wrap').text
            like = l.find_element_by_class_name('u_cbox_cnt_recomm').text
            unlike = l.find_element_by_class_name('u_cbox_cnt_unrecomm').text
            lists.append(content)

        except:
            print("크롤링 실패")
    return lists

def show_lists(lists):
    for l in lists:
        print(l)


button = driver.find_elements_by_css_selector("a[data-param='favorite']")[0]

button.click()
sleep(3)
lists = crawl()
show_lists(lists)

print('----\n')

button = driver.find_elements_by_css_selector("a[data-param='new']")[0]
button.click()
sleep(3)
lists = crawl()
show_lists(lists)
