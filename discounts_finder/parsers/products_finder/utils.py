import re
from typing import List, Tuple

from bs4 import Tag
from validator_collection import validators

from discounts_finder.parsers.products_finder.exceptions import (
    ProductDivPatternNotFound,
)


def remove_letters(text: str) -> str:
    return re.sub(r"[^\d.,]", "", text)


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


def find_image_div(reference_tag: Tag) -> Tag:
    image_style_pattern = re.compile(r"background-image: url\(.+\);")  # find image tag
    img_tag_pattern = re.compile(r"https://.+")
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


def find_anchor_tag(reference_tag: Tag) -> Tag:
    anchor_tag_candidate = reference_tag.parent
    while not is_anchor_with_url(anchor_tag_candidate):
        anchor_tag_candidate = anchor_tag_candidate.parent
        if anchor_tag_candidate is None:
            break

    if anchor_tag_candidate is None:
        raise ProductDivPatternNotFound("Invalid anchor tag pattern")

    return anchor_tag_candidate
