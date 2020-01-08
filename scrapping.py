import requests
from bs4 import BeautifulSoup
import re
import json

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbexhibition

# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {'Host' : 'search.naver.com'}
rank = 0
url1 = 'https://search.naver.com/p/csearch/content/qapirender.nhn?key=PerformListAPI&where=nexearch&pkid=269&_callback=jQuery1124007947377311697013_1577775357992&q=++%EA%B3%B5%EC%97%B0&so=&start='
for i in range(1,5):
    data = requests.get(url1 + str(i))
#data = requests.get('https://search.naver.com/p/csearch/content/qapirender.nhn?key=PerformListAPI&where=nexearch&pkid=269&_callback=jQuery1124007947377311697013_1577775357992&q=++%EA%B3%B5%EC%97%B0&so=&start=1', headers=headers)
# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.

    regex = re.compile(r'\((.*)\)')
    match = regex.search(data.text)
    gr = match.group(1)
    json_data = json.loads(gr)
    html_data = json_data['list'][0]['html']
    soup = BeautifulSoup(html_data, 'html.parser')
# img src 뽑아오기
#형식
# < div
# class ="list_title" >
#
# < strong >
# < a
# nocr
# onclick = "return goOtherCR(this, 'a=nco_x0i*1.ptit&r=1&i=18112ABF_000000000000&u=' + urlencode(this.href));"
#
#
# class ="tit" href="?where=nexearch&sm=tab_etc&pkid=269&os=9354179&query=%EC%97%B0%EA%B7%B9%20%EA%B7%B9%EC%A0%81%EC%9D%B8%20%ED%95%98%EB%A3%BB%EB%B0%A4%20%EB%93%9C%EB%A6%BC%EC%95%84%ED%8A%B8%EC%84%BC%ED%84%B0" > 극적인 하룻밤 - 서울 < / a >
#
# < / strong >
# < span
#
#
# class ="period" > 19.03.01.~오픈런 < / span >
#
# < span
#
#
# class ="list_cate" >
#
# < a
# nocr
# onclick = "return goOtherCR(this, 'a=nco_x0i*1.phall&r=1&i=18112ABF_000000000000&u=' + urlencode(this.href));"
# href = "?where=nexearch&sm=tab_etc&query=%EB%8C%80%ED%95%99%EB%A1%9C%20%EB%93%9C%EB%A6%BC%EC%95%84%ED%8A%B8%EC%84%BC%ED%84%B0%204%EA%B4%80" > 대학로
# 드림아트센터
# 4
# 관 < / a >
# < / span >
# < / div >
# < div
#
#
# class ="btn_box" >
#
# < a
# nocr
# onclick = "return goOtherCR(this, 'a=nco_x0i*1.nreserve&r=1&i=18112ABF_000000000000&u=' + urlencode(this.href));"
# href = "https://booking.naver.com/booking/12/bizes/216684?area=bni"
#
#
# class ="reserve" target="_blank" >
#
# < span
#
#
# class ="btn_icon" > < / span > < span class ="btn_name" > 예매 < / span >
#
# < / a >
# < / div >

#############################
# (입맛에 맞게 코딩)
#############################

    exhibition = soup.select('.list_title ')


    for ex in exhibition:
        a_tag = ex.find_all('a')
        if a_tag is not None:
            name = a_tag[0].text
            img = soup.find("img")
            img_src = img.get("src")
            rank += 1
            print(rank, name, img_src)

            doc = {
                'rank' : rank,
                'name' : name,
                'img' : img_src
            }

            db.exhibitions.insert_one(doc)





