import re
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Tuple, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag

from discounts_finder.parsers.utils import price_text_to_decimal, get_matching_text


@dataclass
class ProductDTO:
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


class BaseProductsFinder(metaclass=ABCMeta):
    PRICE_PATTERN = r"\d{1,3}(?:\s?\d{3})*(?:[.,]\d{2})?"
    PRICE_REGEX = re.compile(PRICE_PATTERN)

    def __init__(self, html_text: str):
        self.html_text = html_text
        self.parsed_html = BeautifulSoup(self.html_text, "html.parser")

    @abstractmethod
    def get_products(self) -> List[ProductDTO]:
        raise NotImplementedError()
