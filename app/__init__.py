from flask import Flask
# from flask_pymoongo import PyMongo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretKey'
# app.config['MONGO_URL'] = "mongodb://localhost:27017/app"
# mongo = PyMongo(app)

from app import routes