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
        login = session['login']
    else :
        login = False
    return render_template('index.html', login=login)

# 지식거래장터 소개
@app.route('/info')
def into() :
    if 'login' in session :
        login = session['login']
    else :
        login = False
    return render_template('info.html', login=login)

# 동급평가
@app.route('/peer')
def peer() :
    if 'login' in session :
        login = session['login']
    else :
        login = False
    return render_template('evaluation/peer.html', login=login)
# 가치평가
@app.route('/value')
def value() :
    if 'login' in session :
        login = session['login']
    else :
        login = False

    ns = db.n.find()
    techContributions = db.techContributions.find()
    
    return render_template('evaluation/value.html', login=login, ns=ns, techContributions=techContributions)

# 옥션
@app.route('/auction')
def auction() :
    if 'login' in session :
        login = session['login']
    else :
        login = False

    tempList = [x for x in range(5)]
    return render_template('auction.html', login=login, tempList=tempList)

# 마켓
@app.route('/market')
def market() :
    if 'login' in session :
        login = session['login']
    else :
        login = False

    tempList = [x for x in range(5)]
    return render_template('market.html', login=login, tempList=tempList)

# 커뮤니티
@app.route('/community')
def community() :
    if 'login' in session :
        login = session['login']
    else :
        login = False

    # Read from community
    communities = db.communities.find({ 'category': 'community' }, {'_id': 0})
    communities_data = {}
    for index, result in enumerate(communities) :
        result['description'] = result['description'][:150] + '...' # make description 150 chars (substr)
        communities_data[index+1] = result

    # Read from project
    projects = db.communities.find({ 'category': 'project' }, {'_id': 0})
    projects_data = {}
    for index, result in enumerate(projects) :
        result['description'] = result['description'][:150] + '...' # make description 150 chars (substr)
        projects_data[index+1] = result
    return render_template('community/community.html', login=login, communities=communities_data, projects=projects_data)


@app.route('/community/<slug>', methods=['GET', 'DELETE'])
def community_slug(slug) :
    if request.method == 'GET' :
        if 'login' in session :
            login = session['login']
        else :
            login = False

        posting = db.communities.find_one({ 'slug': slug, 'category': 'community' })
        comments = db.comments.find({ 'posting_id': str(posting['_id']) })
        if comments is None :
            return render_template('community/show_slug.html', login=login, posting=posting)
        else :
            return render_template('community/show_slug.html', login=login, posting=posting, comments=comments)

    elif request.method == 'DELETE' :
        try :
            db.communities.delete_one({ '_id': ObjectId(slug), 'category': 'community' })
            print(f'*** community {slug} deleted')
        except Exception as exception :
            print(exception)
        return 'HI'

@app.route('/project/<slug>', methods=['GET', 'DELETE'])
def project_slug(slug) :
    if request.method == 'GET' :
        if 'login' in session :
            login = session['login']
        else :
            login = False
        posting = db.communities.find_one({ 'slug': slug, 'category': 'project' })
        comments = db.comments.find({ 'posting_id': str(posting['_id']) })
        if comments is None :
            return render_template('community/show_slug.html', login=login, posting=posting)
        else :
            return render_template('community/show_slug.html', login=login, posting=posting, comments=comments)

    elif request.method == 'DELETE' :
        try :
            db.communities.delete_one({ '_id': ObjectId(slug), 'category': 'project' })
            print(f'*** project {slug} deleted')
        except Exception as exception :
            print(exception)
        return 'HI'

@app.route('/write', methods=['GET', 'POST'])
def write() :
    if request.method == 'GET' :
        if 'login' in session :
            login = session['login']
        else :
            login = False
        return render_template('community/write.html', login=login)

    elif request.method == 'POST' :
        values = request.form
        print(values)
        writing = {
            'title': values['title'],
            'description': values['description'],
            'slug': slugify(values['title']),
            'category': values['category'],
            'created': datetime.now(),
            'writer': values['writer']
        }

        try :
            db.communities.insert_one(writing) # project collection inserted
            if values['category'] == 'community' :
                return redirect(url_for('community_slug', slug=slugify(values['title'])))
            elif values['category'] == 'project' :
                return redirect(url_for('project_slug', slug=slugify(values['title'])))

        except Exception as exception :
            print(f'*** error - {exception}')
            return 'failed'

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_slug(id) :
    if request.method == 'GET' :
        if 'login' in session :
            login = session['login']
        else :
            login = False

        print(f'*** id: {id}')
        results = db.communities.find_one({ '_id': ObjectId(id) })
        print(results)
        return render_template('community/edit.html', login=login, results=results)

    elif request.method == 'POST' :
        values = request.form
        print(values)
        writing = {
            'title': values['title'],
            'description': values['description'],
            'slug': slugify(values['title']),
            'category': values['category'],
            'created': datetime.now(),
            'writer': values['writer']
        }

        try :
            db.communities.find_one_and_update({ '_id': ObjectId(id) }, {"$set": writing}) # update
            if values['category'] == 'community' :
                return redirect(url_for('community_slug', slug=slugify(values['title'])))
            elif values['category'] == 'project' :
                return redirect(url_for('project_slug', slug=slugify(values['title'])))

        except Exception as exception :
            print(f'*** error - {exception}')
            return 'failed'

@app.route('/comment', methods=['POST'])
def comment() :
    if request.method == 'POST' :
        values = request.form
        comment = {
            'comment': values['comment'],
            'created': datetime.now(),
            'writer': values['writer'],
            'posting_id': values['posting_id']
        }

        try :
            db.comments.insert_one(comment) # insert
            if values['category'] == 'community' :
                return redirect(url_for('community_slug', slug=slugify(values['slug'])))
            elif values['category'] == 'project' :
                return redirect(url_for('project_slug', slug=slugify(values['slug'])))

        except Exception as exception :
            print(f'*** error - {exception}')
            return 'falied'

@app.route('/comment/<id>', methods=['POST'])
def comment_id(id) :
    if request.method == 'POST' :
        try :
            db.comments.delete_one({ '_id': ObjectId(id) })
            return redirect(url_for('community_slug', slug=slugify(request.form['posting_slug'])))

        except Exception as exception :
            print(f'*** error - {exception}')
            return 'falied'




# login, logout
@app.route('/loginout', methods=['POST', 'DELETE'])
def loginout() :
    if request.method == 'POST' :
        values = request.form
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
            return '<script>alert("중복된 이메일입니다.");history.go(-1);</script>'

        # add a new user
        user = {
            'email': values['email'],
            'password': values['password'],
            'created': datetime.now()
        }
        try :
            results = db.users.insert_one(user)
            print(f'signup id: {results.inserted_id}')
            return '<script>location.href="/";</script>'
        except Exception:
            return 'singup failed'

    elif request.method == 'DELETE' :
        return 'delete user'
    elif request.method == 'PATCH' :
        return 'update user'

@app.route('/insert-data', methods=['GET'])
def insert_data() :
    if request.method == 'GET' :
        return render_template('insert_data.html')
@app.route('/insert-data/<id>', methods=['POST'])
def insert_data_id(id) :
    form = request.form
    if id == "1" :
        data = {
            'ipc': form['ipc'],
            'description': form['description'],
            'avg': float(form['avg']),
            'q1': int(form['q1']),
            'q2': int(form['q2']),
            'q3': int(form['q3'])
        }
        try :
            db.n.insert_one(data) # insert
        except Exception : # if cannot read from db
            print("** " + Exception)
    
    elif id == "2" :
        data = {
            'code': form['code'],
            'code_desc': form['code_desc'],
            'rate1': float(form['rate1']),
            'rate2': float(form['rate2']),
            'rate3': float(form['rate3'])
        }
        try :
            db.techContributions.insert_one(data) # insert
        except Exception : # if cannot read from db
            print("** " + Exception)
    return redirect(url_for('insert_data'))
