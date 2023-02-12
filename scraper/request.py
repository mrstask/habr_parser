from requests_html import HTMLSession

session = HTMLSession()
r = session.get('https://habr.com/ru/all/')
div_container = r.html.find('.tm-articles-list', first=True)
articles = div_container.find('.tm-articles-list__item')
for article in articles:
    title = article.find('.tm-article-snippet__title-link', first=True).text
    link = article.find('.tm-article-snippet__title-link', first=True).attrs[
        'href']
    print(title, link)
