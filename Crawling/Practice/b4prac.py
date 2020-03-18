# -*- coding: utf-8 -*-
# 댓글을 달 빈 리스트를 생성합니다.
#https://m.blog.naver.com/PostView.nhn?blogId=codingspecialist&logNo=221336552535&categoryNo=100&proxyReferer=https%3A%2F%2Fwww.google.com%2F

'''
https://m.news.naver.com/comment/list.nhn?commentNo=1940463305&gno=news025,0002951467&mode=LSD=sec&sid1=001&oid=025&aid=0002951467
https://m.news.naver.com/comment/list.nhn?commentNo=1940466355&gno=news025,0002951467&mode=LSD=sec&sid1=001&oid=025&aid=0002951467
https://m.news.naver.com/comment/list.nhn?commentNo=1940467415&gno=news025,0002951467&mode=LSD=sec&sid1=001&oid=025&aid=0002951467

https://m.news.naver.com/comment/list.nhn?commentNo=1940364675&gno=news025,0002951467&mode=LSD=sec&sid1=001&oid=025&aid=0002951467
https://m.news.naver.com/comment/list.nhn?commentNo=1940361585&gno=news025,0002951467&mode=LSD=sec&sid1=001&oid=025&aid=0002951467
'''

import json



List = []
# 라이브러리를 로드합니다.
from bs4 import BeautifulSoup
import requests
import re
import sys
import pprint

# 네이버 뉴스 url을 입력합니다.
url = "https://m.news.naver.com/read.nhn?aid=0000003428&oid=629&sid1=101"

oid = url.split("oid=")[1].split("&")[0]
aid = url.split("aid=")[1]


def cont_to_dict(cont):
    string = str(cont)

    index = string.index('(')
    result = string[index+1:-2]

    result_json = json.loads(result)

    return result_json

result_dict = None


# 파싱하는 단계입니다.
r = requests.get(url)
print(r.content)
soup = BeautifulSoup(r.content, "html.parser")

# print(soup.find_all('span'))









