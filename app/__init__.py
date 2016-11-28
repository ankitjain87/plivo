#!flask/bin/python
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku

import redis

import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI

heroku = Heroku(app)
cache = redis.Redis(config.REDIS_URL)
db = SQLAlchemy(app)


from app.urls import mod
app.register_blueprint(mod)


