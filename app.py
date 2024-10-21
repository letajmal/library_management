from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
import yaml
import requests

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Load OpenAPI specification
with open("openapi.yaml", "r") as file:
    openapi_spec = yaml.safe_load(file)

# Swagger UI configuration
SWAGGER_URL = '/swagger'
API_URL = '/openapi.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'appName': "Sample REST API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Define the Books table
class Books(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

# Define the Members table
class Members(db.Model):
    member_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    debt = db.Column(db.Float, nullable=False, default=0)

# Define the RentedBooks table
class RentedBooks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/openapi.json')
def openapi_json():
    return jsonify(openapi_spec)

def book_crud(method, book_id, quantity=None):
    # Default quantity to 1 if not provided
    if quantity is None:
        quantity = 1

    existing_book = Books.query.filter_by(book_id=book_id).first()
    
    if existing_book:
        if method == 'POST':
            # If the book exists, increment the quantity
            existing_book.quantity += quantity
        elif method == 'DELETE':
            if existing_book.quantity >= quantity:
                existing_book.quantity -= quantity
                if existing_book.quantity < 0:
                    existing_book.quantity = 0  # Prevent negative quantity
            else:
                return jsonify({"error": "No stock available to decrement."}), 400
    else:
        if method == 'DELETE':
            return jsonify({"error": "Book not found."}), 404
        # If the book does not exist, create a new entry with the specified quantity
        new_book = Books(book_id=book_id, quantity=quantity)  # Use the provided quantity
        db.session.add(new_book)

    db.session.commit()
    return jsonify({"message": "Operation successful."}), 200  # Confirm successful operation


@app.route('/import_books', methods=['POST'])
def import_books():
    data = request.get_json()
    number_of_books = data.get('number_of_books', 0)
    method = request.method

    if number_of_books <= 0:
        return jsonify({"error": "Number of books must be greater than zero"}), 400

    # API endpoint details
    API_URL = 'https://frappe.io/api/method/frappe-library'
    imported_books = 0
    page = 1
    
    # Fetch books from the external API until we've imported the requested number
    while imported_books < number_of_books:
        # Make GET request to the external API
        params = {'page': page}
        response = requests.get(API_URL, params=params)
        
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch books from the external API"}), 500
        
        # Extract books from the response
        books = response.json().get('message', [])
        
        if not books:
            break  # No more books to fetch

        # Iterate through the books and import them
        for book in books:
            if imported_books >= number_of_books:
                break  # We've imported enough books

            book_id = int(book['bookID'])

            # book crud
            book_crud(method, book_id)

            imported_books += 1
        
        # Move to the next page
        page += 1

    return jsonify({"message": f"{imported_books} books imported successfully."}), 201

# CRUD operations for Books

# Read all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Books.query.all()
    return jsonify([{"book_id": book.book_id, "quantity": book.quantity} for book in books]), 200

@app.route('/books', methods=['POST', 'DELETE'])
def manage_book():
    data = request.get_json()
    method = request.method
    book_id = data.get('book_id')
    quantity = data.get('quantity', 1)  # Default to 1 if not specified

    if not book_id:
        return jsonify({"error": "Books ID is required."}), 400

    if quantity <= 0:
        return jsonify({"error": "Quantity must be greater than zero."}), 400

    return book_crud(method, book_id, quantity)

# CRUD for Members

@app.route('/members', methods=['POST', 'DELETE'])
def members_crud():
    data = request.get_json()

    # Handle POST request to create a new member
    if request.method == 'POST':
        name = data.get('name')
        if not name:
            return jsonify({"error": "Name is required"}), 400

        # Create and add a new member
        new_member = Members(name=name)
        db.session.add(new_member)
        db.session.commit()

        return jsonify({"message": "Member created successfully", "member_id": new_member.member_id}), 201

    # Handle DELETE request to delete a member
    elif request.method == 'DELETE':
        member_id = data.get('member_id')  # Retrieve the member_id from the request payload
        if not member_id:
            return jsonify({"error": "Member ID is required"}), 400

        # Check if the member exists
        member = Members.query.get_or_404(member_id)

        # Check if the member has rented books
        rented_books = RentedBooks.query.filter_by(member_id=member_id).all()
        if rented_books:
            return jsonify({"error": "Cannot delete member with rented books."}), 400

        # If no rented books, proceed with deleting the member
        db.session.delete(member)
        db.session.commit()

        return jsonify({"message": "Member deleted successfully"}), 200

# Get all members and their debts
@app.route('/members', methods=['GET'])
def get_members():
    members = Members.query.all()
    return jsonify([{"member_id": member.member_id, "name": member.name, "debt": member.debt} for member in members]), 200

if __name__ == '__main__':
    app.run(debug=True)
