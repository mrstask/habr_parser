from sqlalchemy import and_

from scraper.database import Hub, Article, Tag


def save_hubs(session, hubs: list):
    """Save hub data to database"""
    for hub in hubs:
        existing_hub = session.query(Hub).filter_by(link=hub.link).first()
        if existing_hub is None:
            session.add(hub)
    session.commit()
    session.close()


def save_articles(session, article_data: list):
    """Save article data to database"""
    for article in article_data:
        existing_article = session.query(Article).filter_by(
            article_id=article.article_id).first()
        if existing_article is None:
            session.add(article)
    session.commit()
    session.close()


def save_article(session, article):
    existing_article = session.query(Article).filter_by(
        article_id=article.article_id).first()
    if existing_article is None:
        session.add(article)


def get_tags(session, tags):
    tag_objects = []
    for tag in tags:
        existing_tag = session.query(Tag).filter_by(name=tag).first()
        if existing_tag:
            tag_objects.append(existing_tag)
        else:
            save_tag(session, tag)
            tag_objects.append(
                session.query(Tag).filter_by(name=tag).first())
    return tag_objects


def save_tag(session, tag):
    session.add(Tag(name=tag))
    session.commit()


def get_tags_by_tag_ids(session, tag_names):
    return session.query(Tag).filter(Tag.tag_name.in_(tag_names)).all()


def update_article(session, article):
    existing_article = session.query(Article).filter_by(
        article_id=article.article_id).first()
    if existing_article is not None:
        existing_article.content = article.content
        existing_article.title = article.title
        existing_article.date = article.date
        existing_article.tags = article.tags
        session.commit()


def get_articles(session, limit: int = 10):
    return session.query(Article).filter(
        and_(Article.content == ''),
        and_(Article.link.notlike('%company%'))
    ).limit(limit)
