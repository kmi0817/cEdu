from app import app
from flask import render_template, request, session
import requests

@app.route('/')
def index() :
    if 'login' in session :
        login = True
    else :
        login = False
    return render_template('index.html', login=login)

@app.route('/loginout', methods=['POST', 'DELETE'])
def loginout() :
    if request.method == 'POST' :
        values = request.get_json(force=True)
        id = values['id']
        password = values['password']

        if id == "asd@asd.com" and password == "asd" :
            session['login'] = id
            return "login successful"
        else :
            return "login failed"

    elif request.method == 'DELETE' :
        session.clear()
        return "logout successful"
