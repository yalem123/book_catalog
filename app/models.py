from . import db
from flask_login import UserMixin




class User(UserMixin,db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
   
    
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Book(db.Model):
    __tablename__ = 'books'
    isbn = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    Geners = db.Column(db.String(100), nullable=False)
   
    
    def __repr__(self):
        return f"Book('{self.isbn}', '{self.author}', '{self.title}', '{self.Geners}')"
    
        

    
       
        

   