from flask import Flask, render_template, Blueprint, request, flash
import requests

bp = Blueprint('books', __name__, url_prefix='/books')

def raise_exception(error):
    return render_template('books_import.html', error = error)

def request_frappe_api(params):
    API_URL = 'https://frappe.io/api/method/frappe-library'
    response = requests.get(API_URL, params=params)
            
    if response.status_code != 200:
        return raise_exception(f"Failed to connect to the API, {response.status_code}")
    
    # Extract books from the response
    books = response.json().get('message', [])

    if not books:
        return raise_exception("Books Not Found")

    return books

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/import', methods=('GET', 'POST'))
def import_books():
    if request.method == 'POST':
        action = request.form.get('action', '')
        title = request.form.get('title', '')
        authors = request.form.get('authors', '')
        isbn = request.form.get('isbn', '')
        publisher = request.form.get('publisher', '')

        try:
            number_of_books = int(request.form.get('nbooks'))
        except:
            number_of_books = 0

        try:
            page = int(request.form.get('page'))
        except:
            page = 0
        
        params = {}
        if title: params['title'] = title
        if authors: params['authors'] = authors
        if isbn: params['isbn'] = isbn
        if publisher: params['publisher'] = publisher
        if page: params['page'] = page


        if action == 'Search':
            books = request_frappe_api(params)
            return render_template('books_import.html', books = books)

        elif action == 'Import':
            # if number_of_books <= 0:
            #     return raise_exception("Number of Books should be greater than 0")
            # imported_books = 0
            # page = 1
            
            # # Fetch books from the external API until we've imported the requested number
            # while imported_books < number_of_books:
            #     # Make GET request to the external API
            #     params['page'] = page
            #     response = requests.get(API_URL, params=params)
                
            #     if response.status_code != 200:
            #         return jsonify({"error": "Failed to fetch books from the external API"}), 500
                
            #     # Extract books from the response
            #     books = response.json().get('message', [])
                
            #     if not books:
            #         break  # No more books to fetch

            #     # Iterate through the books and import them
            #     for book in books:
            #         if imported_books >= number_of_books:
            #             break  # We've imported enough books

            #         book_id = int(book['bookID'])

            #         # book crud
            #         book_crud(method, book_id)

            #         imported_books += 1
                
            #     # Move to the next page
            #     page += 1
            return render_template('books_import.html')

    # if number_of_books <= 0:
    #     return jsonify({"error": "Number of books must be greater than zero"}), 400

    return render_template('books_import.html')

# title, authors, isbn, publisher and page

def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))