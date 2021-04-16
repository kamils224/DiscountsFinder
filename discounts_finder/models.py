from db import db


class ShopWebsite(db.Model):
    __tablename__ = "shop_website"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    website = db.Column(db.String(200))


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    discount_price = db.Column(db.Integer)
    url = db.Column(db.String(200), index=True, unique=True)
    shop_id = db.Column(db.Integer, db.ForeignKey("shop_website.id"), nullable=False)
    shop = db.relationship("ShopWebsite", backref=db.backref("products", lazy=True))

    def discount(self) -> int:
        discount_percentage = (float(self.discount_price) / float(self.price)) * 100
        return int(round(discount_percentage))
