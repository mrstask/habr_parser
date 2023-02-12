from requests import RequestException, ReadTimeout
from requests_html import HTMLSession

from scraper.settings import headers

session = HTMLSession()
session.headers.update(headers)


def retry_get(url, retries=3, timeout=5):
    for i in range(retries):
        try:
            response = session.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except (RequestException, ReadTimeout) as e:
            if i:
                i -= 1
            else:
                raise e


