from dataclasses import dataclass


@dataclass
class ShopWebsite:
    url: str
    name: str

@dataclass
class Product:
    price: int
    discount_price: int
    url: str
    shop_name: str

    def discount(self) -> int:
        discount_percentage = (float(self.discount_price) / float(self.price)) * 100
        return int(round(discount_percentage))
