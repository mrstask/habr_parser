import asyncio
import pickle

from rabbitmq_connection import consume_messages, populate_queue
from scraper.database import session
from scraper.db_handlers import get_articles, update_article, get_tags
from scraper.helpers import retry_get
from scraper.settings import base_url

from requests_html import HTMLResponse


def parse_article(article: object, resp: HTMLResponse) -> object:
    """
    Parses an article's title, tags, date, and content from the provided HTML
    response.

    :param article: the article object to be updated
    :param resp: the HTML response of the article's page
    :return: the updated article object
    """
    article_container = resp.html.find('article', first=True)

    article.title = resp.html.find('h1.tm-article-snippet__title',
                                   first=True).text
    article.tags = process_tags(
        resp.html.find('div.tm-article-snippet__hubs', first=True).links)
    article.date = resp.html.find('span.tm-article-snippet__datetime-published',
                                  first=True).text
    article.content = article_container.find('div#post-content-body',
                                             first=True).html
    return article


def process_tags(tags: list) -> list:
    """
    Returns the list of tags from the provided list of tag links.

    :param tags: the list of tag links
    :return: the list of tags
    """
    if tags:
        return get_tags(session, [tag.split('/')[-2] for tag in tags])


async def process_article(article: object) -> object:
    """
    Processes an article by retrieving its HTML response, parsing its content,
     and updating it in the database.

    :param article: the article object to be processed
    :return: the processed article object
    """
    resp = await retry_get(base_url + article.link)
    session.add(article)
    article = parse_article(article, resp)
    update_article(session, article)
    print(article.title)
    return article


def is_not_processed(article: object) -> bool:
    """
    Returns True if the article's content is None, False otherwise.

    :param article: the article object to be checked
    :return: True if the article's content is None, False otherwise
    """
    return article.content is None


def is_not_company_blog(article: object) -> bool:
    """
    Returns True if the article's link does not contain the word "company",
    False otherwise.

    :param article: the article object to be checked
    :return: True if the article's link does not contain the word "company",
    False otherwise
    """
    return 'company' not in article.link


async def process_articles():
    """Manual queue from database and process articles"""
    for article in get_articles(session):
        if is_not_processed(article) and is_not_company_blog(article):
            article = await process_article(article)
            print(article.title)


def callback(ch, method, properties, body):
    link = pickle.loads(body)
    asyncio.run(process_article(link))


if __name__ == '__main__':
    populate_queue('articles', get_articles(session))
    consume_messages('articles', callback)
