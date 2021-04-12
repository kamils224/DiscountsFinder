import re
from dataclasses import dataclass
from typing import List, Any, Optional, Tuple

from bs4 import Tag

from discounts_finder.parsers.exceptions import ProductDivPatternNotFound
from discounts_finder.parsers.models import ProductDTO
from discounts_finder.parsers.products_finder.base import BaseProductsFinder


@dataclass
class ProductTagExtractor:
    price_content: List[Tuple[Tag, List[str]]] = None
    image: Tag = None
    url: Tag = None


class DefaultProductsFinder(BaseProductsFinder):
    CURRENCY = "zł"

    @dataclass
    class DivPricePair:
        div: Tag
        price_text: List[str]

    def _get_discount_price_divs(self) -> List[DivPricePair]:
        divs = self.parsed_html.findAll("div")
        price_regex = re.compile(self.PRICE_PATTERN + r"\s" + self.CURRENCY)
        result_divs = []
        for div in divs:
            prices = re.findall(price_regex, div.text)
            if len(prices) == 2:
                result_divs.append(self.DivPricePair(div, prices))

        return result_divs

    def _build_product_div(self, price_div: Tag):
        # find image tag
        image_style_pattern = re.compile(r"background-image: url\(.+\);")
        img_tag_pattern = re.compile(r"https:\/\/.+")
        parent = price_div
        image_tags = parent.findAll("div", attrs={"style": image_style_pattern})
        image_tags.extend(parent.findAll("img", attrs={"src": img_tag_pattern}))
        while len(image_tags) == 0:
            parent = parent.parent
            if parent is None:
                break
            image_tags = parent.findAll("div", attrs={"style": image_style_pattern})
            image_tags.extend(parent.findAll("img", attrs={"src": img_tag_pattern}))

        if len(image_tags) != 1:
            raise ProductDivPatternNotFound("Invalid image tag pattern")

        image_tag = image_tags[0]

        # find details url
        anchor_tag_candidate = image_tag.parent
        while anchor_tag_candidate.name != "a":
            anchor_tag_candidate = anchor_tag_candidate.parent
            if anchor_tag_candidate is None:
                break

        if anchor_tag_candidate is None:
            raise ProductDivPatternNotFound("Invalid anchor tag pattern")

        return image_tags[0]

    def _get_product_divs(self, price_divs: List[DivPricePair]):
        for content in price_divs:
            product_div = self._build_product_div(content.div)
            print(product_div)

    def get_products(self) -> Any:
        div_price_pairs = self._get_discount_price_divs()
        self._get_product_divs(div_price_pairs)
        return div_price_pairs


# only for testing
if __name__ == "__main__":
    morele_path = "../../../sandbox/html_samples/morele_sample.html"
    xkom_path = "../../../sandbox/html_samples/xkom_sample.html"

    with open(morele_path, "r") as file:
        html_content = file.read()

    products_finder = DefaultProductsFinder(html_content)
    result = products_finder.get_products()
