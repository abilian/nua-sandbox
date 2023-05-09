"""Example adapted from:

https://www.digitalocean.com/community/tutorials/how-to-use-a-postgresql-database-in-a-flask-application
"""

from .extensions import db
from .model import Book

BOOKS = [
    ("A Tale of Two Cities", "Charles Dickens", 489, "A great classic!"),
    ("Anna Karenina", "Leo Tolstoy", 864, "Another great classic!"),
]


def register_cli(app):
    @app.cli.command("init-db")
    def init_db():
        """Initialize database (create table if needed)."""
        db.create_all()
        for title, author, pages, review in BOOKS:
            book = Book(title=title, author=author, pages_num=pages, review=review)
            db.session.add(book)
        db.session.commit()
