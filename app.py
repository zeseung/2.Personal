from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.bookmarkingtogether           # 'bookmarkingtogether'라는 이름의 db를 만듭니다.

# HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')


@app.route('/post', methods=['GET'])
def listing():
    # author_give 클라이언트가 준 author를 가져오기 // 카테고리별로 가져오게 하기
    category_receive = request.args.get('category_give')
    # author의 값이 받은 author와 일치하는 document 찾기 & _id 값은 출력에서 제외하기
    result = list(db.bookmarkDB_test.find({'category':category_receive},{'_id':0}))
    # articles라는 키 값으로 내려주기
    return jsonify({'result':'success', 'bookmarkDB_test':result})
    # 코멘트는 북마크 고유 아이디를 기준으로 붙여서 가져오기 (나중에 물어보자)

#모르겠다... 다시 해보자
# for in a.id_list
#    a_id =a.id
#    comments = db.find (article_id)
#    a.comments= comments

# SELECT tb1.sales, tb1.products, tb.id FROM tb1 INNER JOIN tb ON tb1.id = tb.id WHERE tb1.content_id=1;

# SELECT STADIUM.STADIUM_NAME, STADIUM.STADIUM_ID, STADIUM.SEAT_COUNT, STADIUM.HOMETEAM_ID, TEAM.TEAM_NAME
# FROM STADIUM LEFT OUTER JOIN TEAM
# ON STADIUM.HOMETEAM_ID = TEAM.TEAM_ID
# ORDER BY STADIUM.HOMETEAM_ID;

# select bookmarkDB_test._id FROM commentDB_test inner join  bookmarkDB on commentDB_test = bookmarkDB_test._id Where commentDB_test.bookmarkId;
# 이건 잘못 찾은 듯.. mongoDB 조인으로 다시 검색

# db.bookmarkDB_test.aggregate([
# { $lookup:
#        { from: "commentDB_test",
#          localField: "_id",
#          foreignField: "bookmarkId",
#          as: "comment_docs"
#        }
#   },
#   { $out : "bookmarkpluscomment" }
# ])
# 이것도 아니네.... 파이썬에서 mongoDB 조인으로 다시 검색

# API 역할을 하는 부분
@app.route('/post', methods=['POST'])
def bookmarking():
# 클라이언트로부터 데이터를 받는 부분 // 북마크를 등록하면 저장 (좋아요 숫자는 0으로 시작)
    category_receive = request.form['category_give']
    likeCount_receive = request.form['likeCount_give']
    title_receive = request.form['title_give']
    url_receive = request.form['url_give']

# meta tag를 스크래핑 하는 부분 (이미지만 가져오게 될 듯 // 이미지가 없는 경우 대체 이미지 노출 - 이건 자바스크립트로 하면 되려나?)

    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    url_image = og_image['content']

# mongoDB에 넣는 부분
    bookmark = {'category': category_receive, 'likeCount': likeCount_receive, 'title': title_receive, 'url': url_receive, 'image': url_image}
    '''
    bookmark = {'category': category_receive, 'likeCount': likeCount_receive, 'title': title_receive, 'url': url_receive}
    db.bookmarkDB_test.insert_one(bookmark)

    return jsonify({'result': 'success'})

@app.route('/comment', methods=['POST'])
def commenting():
# 코멘트를 남기면 북마크 별로 저장 (mongoDB 고유 아이디는 어떻게 쌓지?)
    bookmarkId_receive = request.form['bookmarkId_give']
    nickname_receive = request.form['nickname_give']
    contents_receive = request.form['contents_give']

#mongoDB에 넣는 부분
    comment = {'bookmarkId': bookmarkId_receive, 'nickname': nickname_receive, 'contents': contents_receive}
    db.commentDB_test.insert_one(comment)

    return jsonify({'result': 'success'})
'''
@app.route('/like', methods=['POST'])
def likecounting():
# 좋아요를 누르면 bookmarkDB의 likeCount에 +1씩 쌓음 (이걸 이렇게 하는 것이 맞나? - 이건 자바스크립트로 하면 되려나?)
'''

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)