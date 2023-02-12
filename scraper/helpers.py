from typing import Optional
from requests import RequestException, ReadTimeout
from requests_html import AsyncHTMLSession

from scraper.settings import headers


async def retry_get(url: str, retries: Optional[int] = 3,
                    timeout: Optional[int] = 5):
    """
    A function that performs an asynchronous GET request to the specified URL,
     with optional retries and timeout.
    If the request fails, the function will retry up to `retries` times, with a
    `timeout` specified in seconds.

    :param url: The URL to perform the GET request to.
    :param retries: The number of retries to perform before raising an
    exception. Defaults to 3.
    :param timeout: The number of seconds to wait for a response before raising
    a ReadTimeout exception. Defaults to 5.
    :return: A `Response` object containing the response to the GET request.
    :raises: RequestException if the request failed, ReadTimeout if the request
    timed out.
    """
    asession = AsyncHTMLSession()
    asession.headers.update(headers)

    for i in range(retries):
        try:
            response = await asession.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except (RequestException, ReadTimeout) as e:
            if i:
                i -= 1
            else:
                raise e
