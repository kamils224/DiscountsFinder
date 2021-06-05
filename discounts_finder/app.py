import logging

from flask import Flask
from flask_restful import Api
from flask_script import Manager

from celery_init import make_celery
from mongo import mongo
from ma import ma

app = Flask(__name__)
app.config.from_object("config.Config")

marshmallow = ma.init_app(app)
api = Api(app)
mongo.init_app(app)

manager = Manager(app)
celery = make_celery()


if __name__ == '__main__':
    manager.run()
