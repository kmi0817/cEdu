from app import app
from flask import render_template, request, session, jsonify
import pymongo

try :
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMs = 1000
    )
    db = mongo.cEdu
    mongo.server_info() # trigger exception if cannot connect to db
except :
    print("** error - cannot connect to DB")

@app.route('/')
def index() :
    if 'login' in session :
        login = True
    else :
        login = False
    return render_template('index.html', login=login)

# 지식 거래 장터 소개
@app.route('/hello')
def hello() :
    return '지식 거래 장터 소개'

# 동료 평가
@app.route('/peer-feedback')
def peer_feedback() :
    return '동료평가'

@app.route('/register/<subject>')
def register(subject) :
    if subject == 'specialists' :
        return '전문가 등록'
    elif subject == 'seller' :
        return '판매자 등록'
    elif subject == 'buyer' :
        return '구매자 등록'

@app.route('/intellectual-asset/<action>')
def intellectual_asset(action) :
    if action == 'apply' :
        return '지식자산 평가 신청'
    elif action == 'select' :
        return '지식자산 선별'

@app.route('/evaluation-results')
def evaluation_results() :
    return '평가결과 공개'

# 옥션
@app.route('/auction')
def auction() :
    return "옥션"

# 마켓
@app.route('/market')
def market() :
    return "마켓"

# ODI
@app.route('/odi')
def odi() :
    return "ODI"

# 아이디어 장터 메뉴
@app.route('/idea/<submenu>')
def idea(submenu) :
    # sessino check
    if 'login' in session :
        login = True
    else :
        login = False

    # idea routes
    if submenu == 'market' :
        return '아이디어 마켓'
    elif submenu == 'challenge' :
        return '아이디어 도전'
    elif submenu == 'basket' :
        return '아이디어 바구니'
    elif submenu == 'community' :
        return render_template('idea/community.html', login=login)

# NFT 생성
@app.route('/nft')
def nft() :
    return 'NFT 생성'

# 판매자
@app.route('/seller')
def seller() :
    return '판매자'

# 구매자
@app.route('/buyer')
def buyer() :
    return 'buyer'


# login, logout
@app.route('/loginout', methods=['POST', 'DELETE'])
def loginout() :
    if request.method == 'POST' :
        values = request.get_json(force=True)
        try :
            results = db.users.find_one({ 'email': values['email'] }) # read from db

            if results['password'] == values['password'] : # check if password matched
                session['login'] = values['email']
                return 'login successful'
            else :
                return 'login failed'
            
        except Exception : # if cannot read from db
            return 'login failed'

    elif request.method == 'DELETE' :
        session.pop('login', None)
        return 'logout successful'

# users - create, delete, update user
@app.route('/users', methods=['POST', 'DELETE', 'PATCH'])
def users() :
    if request.method == 'POST' :
        values = request.get_json(force=True)

        # check if email is duplicated
        try :
            db.users.find_one({ 'email': values['email'] })
            return 'duplicated'
        except Exception :
            pass

        # add a new user
        user = {
            'email': values['email'],
            'password': values['password']
        }
        try :
            results = db.users.insert_one(user)
            print(f'signup id: {results.inserted_id}')
            return 'signup successful'
        except Exception:
            return 'singup failed'

    elif request.method == 'DELETE' :
        return 'delete user'
    elif request.method == 'PATCH' :
        return 'update user'

@app.route('/models')
def models() :
    test_data = [
        {
            "id": 1, "title": "Test Community!",
            "body": "Data widgets are used to present data of a specified type on the page. Such widgets manage the space allocated for their data and provide functionality for its access and configuration."
        },
        {
            "id": 2, "title": "Test 2",
            "body": "Data widgets are used to present data of a specified type on the page. Such widgets manage the space allocated for their data and provide functionality for its access and configuration."
        },
        {
            "id": 3, "title": "Test 3 Community!",
            "body": "Data widgets are used to present data of a specified type on the page. Such widgets manage the space allocated for their data and provide functionality for its access and configuration."
        },
        {
            "id": 4, "title": "Test 4",
            "body": "Data widgets are used to present data of a specified type on the page. Such widgets manage the space allocated for their data and provide functionality for its access and configuration."
        },
        {
            "id": 5, "title": "Test Community!",
            "body": "Data widgets are used to present data of a specified type on the page. Such widgets manage the space allocated for their data and provide functionality for its access and configuration."
        },
        {
            "id": 6, "title": "Test 2",
            "body": "Data widgets are used to present data of a specified type on the page. Such widgets manage the space allocated for their data and provide functionality for its access and configuration."
        },
        {
            "id": 7, "title": "Test 3 Community!",
            "body": "Data widgets are used to present data of a specified type on the page. Such widgets manage the space allocated for their data and provide functionality for its access and configuration."
        },
        {
            "id": 8, "title": "Test 4",
            "body": "Data widgets are used to present data of a specified type on the page. Such widgets manage the space allocated for their data and provide functionality for its access and configuration."
        }
    ]
    return jsonify(test_data)

# temporary routes for TEST
@app.route('/temp')
def temp_index() :
    return render_template('temp/index2.html')

@app.route('/temp/community')
def temp_community() :
    return render_template('temp/community2.html')