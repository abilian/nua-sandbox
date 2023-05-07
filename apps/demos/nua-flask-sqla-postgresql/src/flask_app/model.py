# "CREATE TABLE books ("
# "id serial PRIMARY KEY, "
# "title varchar (150) NOT NULL, "
# "author varchar (50) NOT NULL, "
# "pages_num integer NOT NULL, "
# "review text, "
# "date_added date DEFAULT CURRENT_TIMESTAMP);"
from datetime import datetime

from sqlalchemy.orm import Mapped


class Book:
    id: Mapped[int]
    title: Mapped[str]
    author: Mapped[str]
    pages_num: Mapped[int]
    review: Mapped[str]
    date_added: Mapped[datetime]
