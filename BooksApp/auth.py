import functools

from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'

        elif not password:
            error = 'Password is required.'

        elif db.execute(
            'SELECT id FROM users WHERE name = :name', {'name': username}
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO users (name, password) VALUES (:name, :password)',
                {'name': username,
                 'password': generate_password_hash(password)})
            db.commit()
            session['username'] = username
            return redirect(url_for('books.index'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE name = :name', {'name': username}
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'

        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['name']
            return redirect(url_for('books.index'))

        flash(error)

    if 'user_id' in session:
        return redirect(url_for('books.index'))

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' in session:
            return view(**kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('auth.login'))

    return wrapped_view
