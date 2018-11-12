import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    """Populate database with data from 'books.csv' file.
    """

    with open("books.csv") as f:
        reader = csv.reader(f)
        next(reader)
        for isbn, title, author, year in reader:
            db.execute("INSERT INTO books (isbn, title, author, publication) \
                        VALUES (:isbn, :title, :author, :publication)",
                       {"isbn": isbn, "title": title, "author": author, "publication": year})
            print(f"Added book {title}.")
        db.commit()


if __name__ == "__main__":
    main()
