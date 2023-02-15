import uvicorn

from fastapi import FastAPI
from scraper.db_handlers import get_articles
app = FastAPI()

@app.get("/articles")
async def get_articles():
    """
    Get a list of articles.
    """
    articles = get_articles()
    return articles

@app.get("/articles/{article_id}")
async def get_article(article_id: int):
    """
    Get a specific article by ID.
    """
    article = get_article_by_id(article_id)
    return article

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
