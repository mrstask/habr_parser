from requests_html import HTMLSession

from scraper.database import save_hubs_to_db, Hub, Article, save_articles_to_db


def get_hubs_from_page(session: HTMLSession, page: int = 1):
    r = session.get(f'https://habr.com/ru/hubs/page{page}/')
    div_container = r.html.find('.tm-hubs-list', first=True)
    hubs = div_container.find('.tm-hubs-list__hub')
    data = [extract_data_from_hub(hub) for hub in hubs]
    save_hubs_to_db(data)


def extract_data_from_hub(hub):
    title = hub.find('.tm-hub__title', first=True).text
    description = hub.find('.tm-hub__description', first=True).text
    pictogram = hub.find('.tm-entity-image__pic', first=True).attrs[
        'src']
    link = hub.find('.tm-hub__title', first=True).attrs[
        'href']
    return Hub(title, description, link, pictogram)


def get_articles_from_flow_page(flow_name: str, page: int = 1):
    r = retry_get(f'https://habr.com/ru/flows/{flow_name}/page{page}/')
    articles = r.html.find('.tm-articles-list__item')
    data = [extract_data_from_article(article) for article in articles]
    save_articles_to_db(data)


def extract_data_from_article(article):
    article_id = article.attrs['id']
    try:
        article_link = article.find('.tm-article-snippet__title-link', first=True).attrs[
                'href']
    except AttributeError:
        article_link = None
    return Article(article_id, article_link)


if __name__ == '__main__':
    for i in range(4368, 6024):
        print(f'Page {i}')
        get_articles_from_flow_page('develop', i)
