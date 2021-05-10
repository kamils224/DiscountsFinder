from celery import Celery
from flask import Flask
from flask_restful import Api
from flask_script import Manager

from mongo import mongo
from ma import ma

app = Flask(__name__)
app.config.from_object("config.Config")

marshmallow = ma.init_app(app)
api = Api(app)
mongo.init_app(app)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

manager = Manager(app)

if __name__ == "__main__":
    manager.run()
