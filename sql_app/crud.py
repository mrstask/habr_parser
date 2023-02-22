from sqlalchemy.orm import Session
from sqlalchemy import and_

from . import models, schemas
from .models import Hub, Article, Tag


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email,
                          hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


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
    # return session.query(Article).filter(
    #     and_(Article.content == ''),
    #     and_(Article.link.notlike('%company%'))
    # ).limit(limit)
    return session.query(Article).limit(limit).all()
