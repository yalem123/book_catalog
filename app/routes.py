import os
from . import create_app
from .models import Book,User
from . import db
from forms import RegistrationForm, LoginForm
from flask import jsonify, redirect, request, abort, render_template, url_for,flash

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.route("/")
def index():
    books = Book.query.all()
    return render_template("layout.html", books=books)


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
    return redirect(url_for("layout"))


@app.route('/add_book/', methods=['POST'])
def add_book():
    if not request.form:
        abort(400)
    book = Book(
        title=request.form.get('title'),
        author=request.form.get('author'),
        price=request.form.get('price')
    )
    db.session.add(book)
    db.session.commit()
    return redirect(url_for("layout"))


@app.route('/update_book/<int:isbn>', methods=['POST'])
def update_book(isbn):
    if not request.form:
        abort(400)
    book = Book.query.get(isbn)
    if book is None:
        abort(404)
    book.title = request.form.get('title', book.title)
    book.author = request.form.get('author', book.author)
    book.price = request.form.get('price', book.price)
    db.session.commit()
    return redirect(url_for("layout"))
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
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)