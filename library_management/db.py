from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

# Define the Books table
class Books(db.Model):
    __tablename__ = 'books'  # Set the name of the table explicitly
    book_id = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(db.String(255), nullable=False)
    average_rating = db.Column(db.Float)
    isbn = db.Column(db.String(10))
    isbn13 = db.Column(db.String(13))
    language_code = db.Column(db.String(3))
    num_pages = db.Column(db.Integer)
    ratings_count = db.Column(db.Integer)
    text_reviews_count = db.Column(db.Integer)
    publication_date = db.Column(db.Date)
    publisher = db.Column(db.String(255))
    quantity = db.Column(db.Integer)
