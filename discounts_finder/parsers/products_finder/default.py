import re
from dataclasses import dataclass
from typing import List, Optional

from bs4 import Tag

from discounts_finder.parsers.products_finder.base import BaseProductsFinder, WebShopProduct
from discounts_finder.parsers.products_finder.exceptions import ProductDivPatternNotFound
from discounts_finder.parsers.products_finder.utils import get_image_url, remove_letters, find_image_div, \
    find_anchor_tag


@dataclass
class DivPricePair:
    div: Tag
    price_text: List[str]


def _create_product(price_pairs: DivPricePair, image_tag: Tag, anchor_tag: Tag) -> Optional[WebShopProduct]:
    prices = sorted([remove_letters(text).replace(",", ".") for text in price_pairs.price_text])
    url = anchor_tag.attrs["href"]
    image_url = get_image_url(image_tag)

    return WebShopProduct(url, image_url, prices[0], prices[1])


def _get_product_divs(price_divs: List[DivPricePair]) -> List[WebShopProduct]:
    """
    Creates product entity based on found price tags.
    """
    results = []
    for price_pair in price_divs:
        try:
            image_div = find_image_div(price_pair.div)
            anchor_tag_div = find_anchor_tag(image_div)
        except ProductDivPatternNotFound:
            continue
        results.append(_create_product(price_pair, image_div, anchor_tag_div))
    return results


class DefaultPolishProductsFinder(BaseProductsFinder):
    CURRENCY = "zł"

    def _get_discount_price_divs(self) -> List[DivPricePair]:
        divs = self.parsed_html.findAll("div")
        price_regex = re.compile(self.PRICE_PATTERN + r"\s" + self.CURRENCY)
        result_divs = []
        for div in divs:
            prices = re.findall(price_regex, div.text)
            if len(prices) == 2:
                result_divs.append(DivPricePair(div, prices))

        return result_divs

    def get_products(self) -> List[WebShopProduct]:
        div_price_pairs = self._get_discount_price_divs()
        products = _get_product_divs(div_price_pairs)
        return products


# only for testing
if __name__ == "__main__":
    morele_path = "../../../sandbox/html_samples/morele_sample.html"
    xkom_path = "../../../sandbox/html_samples/xkom_sample.html"
    sferis = "../../../sandbox/html_samples/sferis.html"

    with open(sferis, "r") as file:
        html_content = file.read()

    products_finder = DefaultPolishProductsFinder(html_content)
    result = products_finder.get_products()
    for p in result:
        print(p)
