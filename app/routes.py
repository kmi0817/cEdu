from datetime import datetime
from app import app
from flask import render_template, request, session, jsonify, redirect, url_for
import pymongo
from slugify import slugify
from bson.objectid import ObjectId

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
        values = request.form
        print(values)
        try :
            results = db.users.find_one({ 'email': values['email'] }) # read from db

            if results['password'] == values['password'] : # check if password matched
                session['login'] = values['email']
                return '<script>location.href="/";</script>'
            else :
                return '<script>alert("일치하는 회원 정보가 없습니다.");history.go(-1);</script>'
            
        except Exception : # if cannot read from db
            return '<script>alert("로그인에 실패했습니다.");history.go(-1);</script>'

    elif request.method == 'DELETE' :
        session.pop('login', None)
        return 'logout successful'

# users - create, delete, update user
@app.route('/users', methods=['POST', 'DELETE', 'PATCH'])
def users() :
    if request.method == 'POST' :
        values = request.form

        # check if email is duplicated
        if db.users.find_one({ 'email': values['email'] }) :
            print(db.users.find_one({ 'email': values['email'] }))
            return 'duplicated'

        # add a new user
        user = {
            'email': values['email'],
            'password': values['password']
        }
        try :
            results = db.users.insert_one(user)
            print(f'signup id: {results.inserted_id}')
            return redirect(url_for(index))
        except Exception:
            return 'singup failed'

    elif request.method == 'DELETE' :
        return 'delete user'
    elif request.method == 'PATCH' :
        return 'update user'


@app.route('/community')
def community() :
    if 'login' in session :
        login = True
    else :
        login = False

    # Read from community
    communities = db.community.find({}, {'_id': 0})
    communities_data = {}
    for index, result in enumerate(communities) :
        communities_data[index+1] = result

    # Read from project
    projects = db.project.find({}, {'_id': 0})
    projects_data = {}
    for index, result in enumerate(projects) :
        projects_data[index+1] = result
    return render_template('community.html', login=login, communities=communities_data, projects=projects_data)


@app.route('/community/<slug>', methods=['GET', 'DELETE'])
def community_slug(slug) :
    if request.method == 'GET' :
        if 'login' in session :
            login = True
        else :
            login = False

        results = db.community.find_one({ 'slug': slug, 'category': 'community' })
        return render_template('show_slug.html', login=login, results=results)

    elif request.method == 'DELETE' :
        try :
            db.project.delete_one({ '_id': ObjectId(slug), 'category': 'community' })
            print(f'*** community {slug} deleted')
        except Exception as exception :
            print(exception)
        return 'HI'

@app.route('/project/<slug>', methods=['GET', 'DELETE'])
def project_slug(slug) :
    if request.method == 'GET' :
        if 'login' in session :
            login = True
        else :
            login = False
        results = db.project.find_one({ 'slug': slug, 'category': 'project' })
        return render_template('show_slug.html', login=login, results=results)

    elif request.method == 'DELETE' :
        try :
            db.project.delete_one({ '_id': ObjectId(slug), 'category': 'project' })
            print(f'*** project {slug} deleted')
        except Exception as exception :
            print(exception)
        return 'HI'

@app.route('/write', methods=['GET', 'POST'])
def write() :
    if request.method == 'GET' :
        if 'login' in session :
            login = True
        else :
            login = False
        return render_template('write.html', login=login)

    elif request.method == 'POST' :
        try :
            values = request.form
            print(values)
            writing = {
                'title': values['title'],
                'description': values['description'],
                'slug': slugify(values['title']),
                'category': values['category'],
                'created': datetime.now()
            }

            if values['category'] == 'community' :
                db.community.insert_one(writing) # community collection inserted
                return redirect(url_for('community_slug', slug=slugify(values['title'])))
            elif values['category'] == 'project' :
                db.project.insert_one(writing) # project collection inserted
                return redirect(url_for('project_slug', slug=slugify(values['title'])))


        except Exception as exception :
            print(f'*** error - {exception}')
            return 'failed'