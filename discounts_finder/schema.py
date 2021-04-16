from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models import Product, ShopWebsite


class ShopWebsiteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ShopWebsite


class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
