from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import URLType

from discounts_finder.app import db


class ShopWebsite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    website = db.Column(db.String(50))
