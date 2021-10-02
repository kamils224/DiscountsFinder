from marshmallow_dataclass import class_schema

from discounts_finder.parsers.products_finder.models import WebShopProduct

WebShopProductSchema = class_schema(WebShopProduct)


class WebProductSerializer(WebShopProductSchema):
    # Extend serializer here
    pass
