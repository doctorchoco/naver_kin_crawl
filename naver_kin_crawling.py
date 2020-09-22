import os
import sys
import urllib.request
import requests
from bs4 import BeautifulSoup
import json


client_id = ""
client_secret = ""

keyword = "심리상담"
encText = urllib.parse.quote(keyword)
option ="&display=100"
url = "https://openapi.naver.com/v1/search/kin?query=" + encText  +option # json 결과


request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)

response = urllib.request.urlopen(request)
rescode = response.getcode()

print("hello")
if(rescode==200):
    response_body = response.read()
    # print(response_body.decode('utf-8'))
    # json으로 변경
    res_json = json.loads(response_body.decode('utf-8'))
    # link 뽑기
    num_data=res_json["display"]
    print(num_data)
    for obj in res_json["items"] :
        link = obj["link"]
        # print("link", link)
        # link 다시 크롤링
        data = {'display': '100'}
        res = requests.get(link,data=data)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 질문 내용 = q / 답변 = a
        q = soup.select('#content > div.question-content > div > div.c-heading._questionContentsArea.c-heading--default-old > div.c-heading__content')
        a = soup.select('#answer_1 > div._endContents.c-heading-answer__content > div._endContentsText.c-heading-answer__content-user')
        
        # content에 내용 없는 경우 예외 처리
        if q != [] :
            print("q", q[0].text)
        else :
            # 임시로 타이틀만
            print('q', obj["title"])
        if a != [] :
            print('a', a[0].text)
else:
    print("Error Code:" + rescode)
