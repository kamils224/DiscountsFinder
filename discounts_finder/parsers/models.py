from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ProductDTO:
    description: str
    url: str
    price: Decimal
    discount_price: Decimal

    @property
    def discount(self) -> int:
        discount_ratio = 1 - (float(self.discount_price) / float(self.price))
        return int(round(discount_ratio * 100))

    def __str__(self):
        return f"Description: {self.description}, \
        price: {self.price}, \
        discount_price: {self.discount_price}, \
        discount : {self.discount}%"
