from app import db
from app.routes import app
from app.models import Book,User


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Book=Book, User=User)
