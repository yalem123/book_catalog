import os
from . import create_app
from .models import Book, User
from . import db, bcrypt
from forms import RegistrationForm, LoginForm
from flask import jsonify, redirect, request, abort, render_template, url_for,flash
from flask_login import login_user, current_user, logout_user, login_required



app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.route("/")
def index():
    books = Book.query.all()
    return render_template("index.html", books=books)


@app.route("/book/list", methods=["GET"])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_json() for book in books])


@app.route("/book/<int:isbn>", methods=["GET"])
def get_book(isbn):
    book = Book.query.get(isbn)
    if book is None:
        abort(404)
    return render_template("book.html", isbn=isbn)


@app.route("/delete/<int:isbn>", methods=["POST"])
def delete(isbn):
    book = Book.query.get(isbn)
    if book is None:
        abort(404)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("index"))


@app.route('/add_book/', methods=['POST'])
def add_book():
    if not request.form:
        abort(400)
    book = Book(
        title=request.form.get('title'),
        author=request.form.get('author'),
        Geners=request.form.get('Geners')
    )
    db.session.add(book)
    db.session.commit()
    return redirect(url_for("index"))


@app.route('/update_book/<int:isbn>', methods=['POST'])
def update_book(isbn):
    if not request.form:
        abort(400)
    book = Book.query.get(isbn)
    if book is None:
        abort(404)
    book.title = request.form.get('title', book.title)
    book.author = request.form.get('author', book.author)
    book.Geners = request.form.get('Geners', book.Geners)
    db.session.commit()
    return redirect(url_for("index"))
@app.route("/home")
def home():
    return render_template('home.html', posts=User)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'your account has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
