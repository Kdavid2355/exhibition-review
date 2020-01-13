import requests
from bs4 import BeautifulSoup
import re
import json
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://bjk:helloworld@heewon-fyhwo.gcp.mongodb.net/test?retryWrites=true&w=majority"
)
db = client.bjk
# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {"Host": "search.naver.com"}
rank = 0
# url1 = 'https://search.naver.com/p/csearch/content/qapirender.nhn?key=PerformListAPI&where=nexearch&pkid=269&_callback=jQuery1124007947377311697013_1577775357992&q=++%EA%B3%B5%EC%97%B0&so=&start='

data = requests.get(
    "https://search.naver.com/p/csearch/content/qapirender.nhn?key=PerformListAPI&where=nexearch&pkid=269&_callback=jQuery1124007947377311697013_1577775357992&q=++%EA%B3%B5%EC%97%B0&so=&start=1",
    headers=headers,
)
# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.

regex = re.compile(r"\((.*)\)")
match = regex.search(data.text)
gr = match.group(1)
json_data = json.loads(gr)
html_data = json_data["list"][0]["html"]
soup = BeautifulSoup(html_data, "html.parser")
exhibition = soup.select(".list_thumb")


for ex in exhibition:
    img = ex.find("img")
    name = img.get("alt")
    img_src = img.get("src")
    rank += 1
    print(rank, name, img_src)

    doc = {"rank": rank, "name": name, "img": img_src}

    db.exhibitions.insert_one(doc)
