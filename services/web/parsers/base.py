import re
from abc import ABCMeta, abstractmethod
from typing import List, Tuple, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag

from models import ProductDTO
from utils import remove_letters, price_text_to_decimal, get_matching_text


class BaseProductsFinder(metaclass=ABCMeta):

    PRICE_PATTERN = r"\d{1,3}(?:\s?\d{3})*(?:[.,]\d{2})?\s?zł"
    PRICE_REGEX = re.compile(PRICE_PATTERN)

    def __init__(self, html_content: str):
        self.html_content = html_content
        self.common_fields = self._get_common_fields()

    @abstractmethod
    def _get_common_fields(self) -> List[Tag]:
        raise NotImplemented()

    @abstractmethod
    def _parse_product_tag(self, tag: Tag) -> ProductDTO:
        raise NotImplemented()

    @abstractmethod
    def _get_price_section(self, parent_tags: List[Tag]) -> List[Tag]:
        raise NotImplemented()

    @abstractmethod
    def get_products(self) -> List[ProductDTO]:
        raise NotImplemented()


class DefaultProductsFinder(BaseProductsFinder):
    def _get_common_fields(self) -> List[Tuple[Tag, List[Tag]]]:
        """Returns groups of html tags on the same level.

        Returns:
            List[FieldsTree]: List of FieldsTree which contains 'parent' and 'children' fields.
        """
        soup = BeautifulSoup(self.html_content, "html.parser")
        root = soup.findChildren(recursive=False)

        to_visit = [root]
        common_fields = []

        while len(to_visit) > 0:
            current_div = to_visit.pop()
            for parent in current_div:
                children = parent.findChildren(recursive=False)
                if len(children) > 0:
                    common_fields.append((parent, children))
                to_visit.append(children)
        return common_fields

    def _get_price_section(self) -> Optional[Tag]:
        parent_tags = sorted(
            self.common_fields, key=lambda field: len(field[1]), reverse=True
        )

        for parent, children in parent_tags:
            price_spans = parent.find_all("span", text=self.PRICE_REGEX)
            if len(price_spans):
                return parent
        else:
            return None

    def _parse_product_tag(self, tag: Tag) -> ProductDTO:
        div_content_text = tag.get_text(separator="\n")

        content_lines = div_content_text.split("\n")
        found_prices = get_matching_text(content_lines, self.PRICE_PATTERN)

        if len(found_prices) == 2:
            # get sorted prices
            price_values = sorted(
                [price_text_to_decimal(text_price) for _, text_price in found_prices],
                key=lambda value: float(value),
            )
            # remove prices from description
            indexes_to_remove = [index for index, _ in found_prices]
            content_lines = [
                line
                for index, line in enumerate(content_lines)
                if index not in indexes_to_remove
            ]

            return ProductDTO(
                "\n".join(content_lines),
                "example.com",
                price_values[1],
                price_values[0],
            )

        return None

    def get_products(self) -> List[ProductDTO]:
        price_section = self._get_price_section()

        products = []
        for tag in price_section:
            product = self._parse_product_tag(tag)
            if product is not None:
                products.append(product)
        return products


# only for testing
if __name__ == "__main__":
    xkom_path = "../../../sandbox/html_samples/xkom_sample.html"

    with open(xkom_path, "r") as file:
        html_content = file.read()

    products_finder = DefaultProductsFinder(html_content)

    result = products_finder.get_products()

    for p in result:
        print(p)
        print()