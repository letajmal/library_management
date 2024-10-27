from flask import render_template, Blueprint, request
import requests
from .db import db, Books_table

bp = Blueprint('books', __name__, url_prefix='/books')

def request_frappe_api(params):
    API_URL = 'https://frappe.io/api/method/frappe-library'
    try:
        # Case 1: Connection Error
        # If URL is wrong or no internet, this will fail immediately
        # and jump to except requests.exceptions.RequestException
        response = requests.get(API_URL, params=params)
        
        # Case 2: Bad Status Code
        # API might return 404, 500, etc. even though connection worked
        if response.status_code != 200:
            raise Exception(f"Failed to connect to the API, {response.status_code}")
        
        # Case 3: JSON Parse Error
        # If response isn't valid JSON, this will fail
        # and jump to except ValueError
        books = response.json().get('message', [])

        # Case 4: No Books Found
        # API returned successfully but no books matched search
        if not books:
            raise Exception("Books Not Found")

        # Success case: We have books!
        return books
        
    # Case 1: Handle connection errors
    except requests.exceptions.RequestException as e:
        raise Exception(f"API Request failed: {str(e)}")
    
    # Case 3: Handle JSON parse errors
    except ValueError as e:
        raise Exception(f"Invalid response from API: {str(e)}")

@bp.route('/', methods=('GET', 'POST'))
def index():
    # Handle POST request (form submission)
    if request.method == 'POST':
        # Extract form data with default empty strings if fields are missing
        action = request.form.get('action', '')  # Button clicked ('Search' or 'Update')
        title = request.form.get('title', '')    # Book title to search for
        authors = request.form.get('authors', '') # Author names to search for
        bookID = request.form.get('bookID', '')      # bookID to update

        # Safely convert number of books to integer
        try:
            quantity = int(request.form.get('quantity'))
            if quantity < 0:
                raise Exception  # Prevent negative quantity
        except:
            quantity = 0  # Default to 0 if conversion fails

        if action == 'Search':
            try:
                # Request books from Frappe API
                books = Books_table.query.filter(
                    Books_table.title.ilike(f"%{title}%"),
                    Books_table.authors.ilike(f"%{authors}%")
                ).all()
                # Display results if successful
                return render_template('index.html', books=books, page_uri='books')

            except Exception as e:
                # If any error occurs during API request, show error message
                return render_template('index.html', message=str(e), page_uri='books')
        
        # Handle Update action
        elif action == 'Update':
            try:
                # Request books from Frappe API
                existing_book = Books_table.query.filter_by(bookID=bookID).first()
    
                if existing_book:
                    existing_book.quantity = quantity
                    db.session.commit()
                else:
                    raise Exception("Book Not Found")
            except Exception as e:
                # If any error occurs during API request, show error message
                return render_template('index.html', message=str(e), page_uri='books')
        

    books = Books_table.query.all()
    return render_template('index.html', books=books, page_uri='books')

@bp.route('/import', methods=('GET', 'POST'))
def import_books():
    """
    Route handler for book import functionality.
    Handles both GET (display form) and POST (search/import books) requests.
    """
    
    # Handle POST request (form submission)
    if request.method == 'POST':
        # Extract form data with default empty strings if fields are missing
        action = request.form.get('action', '')  # Button clicked ('Search' or 'Import')
        title = request.form.get('title', '')    # Book title to search for
        authors = request.form.get('authors', '') # Author names to search for
        isbn = request.form.get('isbn', '')      # ISBN to search for
        publisher = request.form.get('publisher', '') # Publisher to search for

        # Safely convert number of books to integer
        try:
            number_of_books = int(request.form.get('nbooks'))
        except:
            number_of_books = 0  # Default to 0 if conversion fails
        
        # Safely convert page number to integer
        try:
            page = int(request.form.get('page'))
        except:
            page = 0  # Default to 0 if conversion fails
        
        # Build API query parameters - only include non-empty values
        params = {}
        if title: params['title'] = title           # Add title if provided
        if authors: params['authors'] = authors     # Add authors if provided
        if isbn: params['isbn'] = isbn             # Add ISBN if provided
        if publisher: params['publisher'] = publisher # Add publisher if provided
        if page: params['page'] = page             # Add page number if provided

        # Handle Search action
        if action == 'Search':
            try:
                # Request books from Frappe API
                books = request_frappe_api(params)
                # Display results if successful
                return render_template('index.html', books=books, page_uri='books_import')
            except Exception as e:
                # If any error occurs during API request, show error message
                return render_template('index.html', message=str(e), page_uri='books_import')
        
        # Handle Import action
        elif action == 'Import':
            if number_of_books <= 0:
                return render_template('index.html', message="Number of Books should be greater than 0", page_uri='books_import')
            imported_books = 0
            page = 1
            
            # Fetch books from the external API until we've imported the requested number
            while imported_books < number_of_books:
                # Make GET request to the external API
                params['page'] = page

                try:
                    # Request books from Frappe API
                    books = request_frappe_api(params)
                except Exception as e:
                    error_message = str(e)  # Convert exception to string for easier handling
                    # Check for specific messages in the exception
                    if "Books Not Found" in error_message:
                        break
                    # If any error occurs during API request, show error message
                    return render_template('index.html', message=str(e), page_uri='books_import')

                # Iterate through the books and import them
                for book in books:
                    if imported_books >= number_of_books:
                        break  # We've imported enough books

                    bookID = int(book['bookID'])

                    existing_book = Books_table.query.filter_by(bookID=bookID).first()
                    
                    if existing_book:
                        existing_book.quantity += 1
                    else:
                        new_book = Books_table(
                            bookID=bookID,
                            title=book['title'],
                            authors=book['authors'],
                            average_rating=float(book['average_rating']),
                            isbn=book['isbn'],
                            isbn13=book['isbn13'],
                            language_code=book['language_code'],
                            num_pages=int(book['  num_pages']),
                            ratings_count=int(book['ratings_count']),
                            text_reviews_count=int(book['text_reviews_count']),
                            publication_date=book['publication_date'],
                            publisher=book['publisher'],
                            quantity=1
                        )
                        db.session.add(new_book)

                    imported_books += 1
                
                # Move to the next page
                page += 1
            db.session.commit()
            return render_template('index.html', message=f'{imported_books}/{number_of_books} were imported', page_uri='books_import')

    # Handle GET request - display empty form
    return render_template('index.html', page_uri='books_import')