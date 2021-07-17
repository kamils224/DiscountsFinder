from typing import List

from requests_html import HTMLSession

from discounts_finder.parsers.products_finder.base import ParsedHtmlProduct
from discounts_finder.parsers.products_finder.default import DefaultProductsFinder


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


def get_products_from_url(url: str) -> List[ParsedHtmlProduct]:
    html = get_dynamic_html(url)
    products_finder = DefaultProductsFinder(html)
    return products_finder.get_products()


if __name__ == '__main__':
    print(get_dynamic_html("https://www.x-kom.pl/g-6/c/15-monitory.html"))
