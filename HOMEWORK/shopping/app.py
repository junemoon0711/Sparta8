from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

# HTML을 주는 부분


@app.route('/')
def home():
    return render_template('index.html')

# API 역할을 하는 부분


@app.route('/orders', methods=['POST'])
def write_order():
    # name_receive로 클라이언트가 준 name 가져오기
    name_receive = request.form['name_give']
    count_receive = request.form['count_give']
    address_receive = request.form['address_give']
    phone_receive = request.form['phone_give']

    # DB에 삽입할 order 만들기
    order = {
        'name': name_receive,
        'count': count_receive,
        'address': address_receive,
        'phone': phone_receive,
    }
    # orders에 order 저장하기, 10번 작업
    db.orders.insert_one(order)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': '오더가 성공적으로 주문되었습니다.'})

    # API 역할을 하는 부분


@app.route('/orders', methods=['GET'])
def read_orders():
   # 1. DB에서 리뷰 정보 모두 가져오기
    orders = list(db.orders.find({}, {'_id': 0}))     # 5,6번 작업
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'orders': orders})     # 7번 작업


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
