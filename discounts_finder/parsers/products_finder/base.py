import re
from abc import ABC, abstractmethod
from typing import List

from bs4 import BeautifulSoup

from discounts_finder.parsers.products_finder.models import WebShopProduct


class BaseProductsFinder(ABC):
    PRICE_PATTERN = r"\d{1,3}(?:\s?\d{3})(?:[.,]\d{2})?"
    PRICE_REGEX = re.compile(PRICE_PATTERN)

    def __init__(self, html_text: str):
        self.html_text = html_text
        self.parsed_html = BeautifulSoup(self.html_text, "html.parser")

    @abstractmethod
    def get_products(self) -> List[WebShopProduct]:
        raise NotImplementedError()
