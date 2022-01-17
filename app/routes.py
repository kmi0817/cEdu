from app import app
from flask import render_template, request, session

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


# process 관련 (로그인, 로그아웃, 회원가입 등)
@app.route('/process/<action>', methods=['POST', 'DELETE'])
def loginout(action) :
    if action == 'loginout' :
        if request.method == 'POST' :
            values = request.get_json(force=True)
            id = values['id']
            password = values['password']

            if id == 'asd@asd.com' and password == 'asd' :
                session['login'] = id
                return 'login successful'
            else :
                return 'login failed'

        elif request.method == 'DELETE' :
            session.clear()
            return 'logout successful'

    elif action == 'signup' :
        values = request.get_json(force=True)
        print(values)
        return 'signup temp OK'


# temporary routes for TEST
@app.route('/temp')
def temp_index() :
    return render_template('temp/index2.html')

@app.route('/temp/community')
def temp_community() :
    return render_template('temp/community2.html')