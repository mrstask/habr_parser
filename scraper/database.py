# from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
# from sqlalchemy.orm import declarative_base, relationship
#
# from sqlalchemy.orm import sessionmaker
#
# Base = declarative_base()
#
#
# class Hub(Base):
#     __tablename__ = 'hubs'
#
#     link = Column(String, primary_key=True)
#     title = Column(String)
#     description = Column(String)
#     pictogram = Column(String)
#
#     def __init__(self, title, description, link, pictogram):
#         self.title = title
#         self.description = description
#         self.link = link
#         self.pictogram = pictogram
#
#
# class Tag(Base):
#     __tablename__ = 'tags'
#
#     tag_id = Column(Integer, primary_key=True)
#     name = Column(String)
#
#
# class ArticleTag(Base):
#     __tablename__ = 'article_tags'
#
#     article_id = Column(Integer, ForeignKey('articles.article_id'),
#                         primary_key=True)
#     tag_id = Column(Integer, ForeignKey('tags.tag_id'), primary_key=True)
#
#
# class Article(Base):
#     __tablename__ = 'articles'
#
#     article_id = Column(Integer, primary_key=True)
#     title = Column(String)
#     content = Column(String)
#     link = Column(String)
#     date = Column(String)
#     tags = relationship("Tag", secondary="article_tags")
#
#     def __init__(self, title, content, link, date, tags):
#         self.title = title
#         self.content = content
#         self.link = link
#         self.date = date
#         self.tags = tags
#
#
# engine = create_engine('sqlite:///hubs.db')
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()
