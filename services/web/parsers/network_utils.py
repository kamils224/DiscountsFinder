from requests_html import HTMLSession


def get_dynamic_html(url: str, timeout: int = 20) -> str:
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