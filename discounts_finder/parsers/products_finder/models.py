from dataclasses import dataclass
from decimal import Decimal

import marshmallow_dataclass


@dataclass
class ParsedHtmlProduct:
    url: str
    image_url: str
    discount_price: Decimal
    price: Decimal

    @property
    def discount(self) -> int:
        discount_ratio = 1 - (float(self.discount_price) / float(self.price))
        return int(round(discount_ratio * 100))

    def __str__(self):
        return f"url: {self.url}\n" \
               f"image: {self.image_url}\n" \
               f"price: {self.price}\n" \
               f"discount_price: {self.discount_price}\n" \
               f"discount : {self.discount}%"


ProductSchema = marshmallow_dataclass.class_schema(ParsedHtmlProduct)
