from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class WebShopProduct:
    url: str
    image_url: str
    discount_price: str
    price: str

    @property
    def discount(self) -> int:
        discount_ratio = 1 - (float(self.discount_price) / float(self.price))
        return int(round(discount_ratio * 100))
