import re
from decimal import Decimal
from typing import List, Tuple

from bs4 import Tag
from validator_collection import validators


def remove_letters(text: str) -> str:
    return re.sub(r"[^\d.,]", "", text)


def price_text_to_decimal(text: str) -> Decimal:
    return Decimal(remove_letters(text).replace(",", "."))


def is_anchor_with_url(tag: Tag) -> bool:
    return tag.name == "a" and "href" in tag.attrs


def get_url_from_css(style_text: str) -> str:
    # input format: url('https://example.com');
    url = style_text.split("url('")[1][:-3]
    return validators.url(url)


def get_url_from_src(tag: Tag) -> str:
    # input format: <img class="..." src="..."/>
    url = tag.attrs["src"]
    return validators.url(url)


def get_image_url(tag: Tag) -> str:
    if tag.name == "img":
        return get_url_from_src(tag)
    elif tag.name == "div":
        background_image_style = tag.attrs["style"]
        return get_url_from_css(background_image_style)
    raise ValueError("Image url not found")


def get_matching_text(text_samples: List[str], pattern: str) -> List[Tuple[int, str]]:
    matches = [re.match(pattern, text_sample) for text_sample in text_samples]
    matched_text = [
        (index, match.group(0)) for index, match in enumerate(matches) if match
    ]
    return matched_text
