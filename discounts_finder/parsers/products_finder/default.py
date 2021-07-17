import re
from dataclasses import dataclass
from typing import List, Optional

from bs4 import Tag

from discounts_finder.parsers.products_finder.base import BaseProductsFinder, ParsedHtmlProduct
from discounts_finder.parsers.products_finder.exceptions import ProductDivPatternNotFound
from discounts_finder.parsers.products_finder.utils import is_anchor_with_url, get_image_url, \
    remove_letters


@dataclass
class DivPricePair:
    div: Tag
    price_text: List[str]


def _get_image_div(reference_tag: Tag) -> Tag:
    # find image tag
    image_style_pattern = re.compile(r"background-image: url\(.+\);")
    img_tag_pattern = re.compile(r"https:\/\/.+")
    parent = reference_tag
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

    return image_tags[0]


def _get_anchor_tag(reference_tag: Tag):
    anchor_tag_candidate = reference_tag.parent
    while not is_anchor_with_url(anchor_tag_candidate):
        anchor_tag_candidate = anchor_tag_candidate.parent
        if anchor_tag_candidate is None:
            break

    if anchor_tag_candidate is None:
        raise ProductDivPatternNotFound("Invalid anchor tag pattern")

    return anchor_tag_candidate


def _create_product(price_pairs: DivPricePair, image_tag: Tag, anchor_tag: Tag) -> Optional[ParsedHtmlProduct]:
    prices = sorted([remove_letters(text).replace(",", ".") for text in price_pairs.price_text])
    url = anchor_tag.attrs["href"]
    image_url = get_image_url(image_tag)

    return ParsedHtmlProduct(url, image_url, prices[0], prices[1])


def _get_product_divs(price_divs: List[DivPricePair]) -> List[ParsedHtmlProduct]:
    """
    Creates product entity based on found price tags.
    """
    results = []
    for price_pair in price_divs:
        try:
            image_div = _get_image_div(price_pair.div)
            anchor_tag_div = _get_anchor_tag(image_div)
        except ProductDivPatternNotFound:
            continue
        results.append(_create_product(price_pair, image_div, anchor_tag_div))
    return results


class DefaultProductsFinder(BaseProductsFinder):
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

    def get_products(self) -> List[ParsedHtmlProduct]:
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

    products_finder = DefaultProductsFinder(html_content)
    result = products_finder.get_products()
    for p in result:
        print(p)
