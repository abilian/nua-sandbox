"""Example adapted from:

https://www.digitalocean.com/community/tutorials/how-to-use-a-postgresql-database-in-a-flask-application
"""
from psycopg2.sql import SQL

from .app import app
from .extensions import db


BOOKS = [
    ("A Tale of Two Cities", "Charles Dickens", 489, "A great classic!"),
    ("Anna Karenina", "Leo Tolstoy", 864, "Another great classic!"),
]



@app.cli.command("init-db")
def init_db():
    """Initialize database (create table if needed)."""
    db.create_all()
    # TODO
    # insert books
