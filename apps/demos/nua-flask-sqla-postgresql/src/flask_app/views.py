from flask import redirect, render_template, request, url_for
from psycopg2.sql import SQL
from sqlalchemy import select

from .app import app
from .extensions import db
from .model import Book


@app.route("/")
def index():
    stmt = select(Book)
    books = db.session.scalars(stmt)
    return render_template("index.html", books=books)


@app.route("/create/", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        if title:
            author = request.form["author"]
            pages_num = int(request.form["pages_num"] or 0)
            review = request.form["review"]
            connection = db_connection()
            cur = connection.cursor()
            cur.execute(
                SQL(
                    "INSERT INTO books (title, author, pages_num, review)"
                    "VALUES (%s, %s, %s, %s)"
                ),
                (title, author, pages_num, review),
            )
            connection.commit()
            cur.close()
            connection.close()
        return redirect(url_for("index"))
    return render_template("create.html")
