from scraper.database import session
from scraper.db_handlers import get_articles, update_article, get_tags
from scraper.helpers import retry_get
from scraper.settings import base_url


def parse_article(article, resp):
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


def process_tags(tags):
    if tags:
        return get_tags(session, [tag.split('/')[-2] for tag in tags])


def process_article(article):
    resp = retry_get(base_url + article.link)
    article = parse_article(article, resp)
    update_article(session, article)
    return article


def is_not_processed(article):
    return article.content is None


def is_not_company_blog(article):
    return 'company' not in article.link


if __name__ == '__main__':
    for article in get_articles(session):
        if is_not_processed(article) and is_not_company_blog(article):
            article = process_article(article)
            print(article.title)
