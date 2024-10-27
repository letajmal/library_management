from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

# Define the Books table
class Books_table(db.Model):
    __tablename__ = 'books'  # Set the name of the table explicitly
    bookID = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(db.String(255), nullable=False)
    average_rating = db.Column(db.Float)
    isbn = db.Column(db.String(10))
    isbn13 = db.Column(db.String(13))
    language_code = db.Column(db.String(3))
    num_pages = db.Column(db.Integer)
    ratings_count = db.Column(db.Integer)
    text_reviews_count = db.Column(db.Integer)
    publication_date = db.Column(db.String(10)) 
    publisher = db.Column(db.String(255))
    quantity = db.Column(db.Integer)

# Define the Members table
class Members_table(db.Model):
    __tablename__ = 'members'  # Set the name of the table explicitly
    member_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    debt = db.Column(db.Float, nullable=False, default=0)

# Define the RentedBooks table
class IssuedBooks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookID = db.Column(db.Integer, db.ForeignKey('books.bookID'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookID = db.Column(db.Integer, db.ForeignKey('books.bookID'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(10), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)