from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
from flask_script import Manager

from db import db, migrate
from ma import ma
from resources import Products

app = Flask(__name__)
app.config.from_object("config.Config")

api = Api(app)
api.add_resource(Products, '/api/products')

db.init_app(app)
migrate.init_app(app, db)
marshmallow = ma.init_app(app)

manager = Manager(app)
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
