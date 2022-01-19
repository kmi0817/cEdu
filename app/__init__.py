from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretKey'

from app import routes