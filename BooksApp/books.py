import os
import requests

from flask import (Blueprint, flash, g, jsonify, redirect,
                   render_template, request, session, url_for)
from werkzeug.exceptions import abort

from BooksApp.auth import login_required
from BooksApp.db import db
from BooksApp.utils import json_Goodreads

bp = Blueprint('books', __name__)


@bp.route('/')
def index():
    return render_template('books/index.html')


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        return render_template('books/search.html')

    isbn = request.args.get('isbn')
    title = request.args.get('title')
    author = request.args.get('author')

    books = db.execute('SELECT * FROM books WHERE \
                        (isbn ILIKE :isbn AND title ILIKE :title AND author ILIKE :author)',
                       {'isbn': f'{isbn}%', 'title': f'{title}%', 'author': f'{author}%'}).fetchall()
    return render_template('books/search.html', books=books)


@bp.route('/books/<isbn>', methods=['GET', 'POST'])
@login_required
def book(isbn, user=0):
    # Make sure book exists.
    book = db.execute('SELECT * FROM books WHERE isbn = :isbn',
                      {'isbn': isbn}).fetchone()
    if book is None:
        return render_template('error.html', message='No such book.')

    reviews = db.execute('SELECT review, rating, isbn, name FROM reviews \
                        JOIN users ON users.id = reviews.user_id \
                        JOIN books ON books.id = reviews.book_id \
                        WHERE isbn = :isbn', {'isbn': isbn}).fetchall()
    # (if available) the average rating and number of ratings from Goodreads.
    for review in reviews:
        if review['name'] == session['username']:
            user = 1

    resGoodreads = json_Goodreads(isbn)
    return render_template('books/book.html',
                           book=book, reviews=reviews,
                           user=user, resGoodreads=resGoodreads)


@bp.route('/books/<isbn>/<book_id>/addreview', methods=['POST'])
@login_required
def add_review(isbn, book_id):
    rating = request.form['rating']
    review = request.form['review']
    user_id = session['user_id']

    db.execute('INSERT INTO reviews (book_id, user_id, rating, review) \
                VALUES (:book_id, :user_id, :rating, :review)',
               {'book_id': book_id, 'user_id': user_id, 'rating': rating, 'review': review})
    db.commit()

    return render_template('books/review.html')


@bp.route('/api/<isbn>')
def get_api(isbn):
    # Make sure book exists.
    book = db.execute('SELECT * FROM books WHERE isbn = :isbn',
                      {'isbn': isbn}).fetchone()
    if book is None:
        return render_template('error.html', message='No such book.'), 404

    resGoodreads = json_Goodreads(isbn)
    return jsonify(title=book['title'],
                   author=book['author'],
                   year=book['publication'],
                   isbn=book['isbn'],
                   review_count=resGoodreads['work_ratings_count'],
                   average_score=resGoodreads['average_rating'])
