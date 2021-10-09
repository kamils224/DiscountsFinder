from typing import List

from requests_html import HTMLSession

from discounts_finder.parsers.products_finder.base import BaseProductsFinder
from discounts_finder.parsers.products_finder.default import DefaultProductsFinder
from discounts_finder.parsers.products_finder.models import WebShopProduct


def get_dynamic_html(url: str, timeout: int = 60) -> str:
    """Downloads html dynamic content generated from javascript.

    Args:
        url (str): target url
        timeout (int, optional): Response render timeout in seconds. Keeps dynamic content alive. Defaults to 20.

    Returns:
        str: Generated html page.
    """
    session = HTMLSession()
    response = session.get(url)

    response.html.render(timeout=timeout)
    dynamic_html = response.html.html
    session.close()

    return dynamic_html


def get_products_from_url(url: str, products_finder: BaseProductsFinder = None) -> List[WebShopProduct]:
    """
    Return products found in the given url.
    Args:
        url (str): target url
        products_finder (BaseProductsFinder): if None, then DefaultProductsFinder is used

    Returns:
        List[WebShopProduct]: List of parsed products.
    """
    html = get_dynamic_html(url)
    if products_finder is None:
        products_finder = DefaultProductsFinder(html)
    return products_finder.get_products()
