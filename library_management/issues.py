from flask import render_template, Blueprint, request
from .db import db, Books_table, Members_table, IssuedBooks, Transactions

bp = Blueprint('issues', __name__, url_prefix='/issues')

@bp.route('/', methods=('GET', 'POST'))
def index():
    # Handle POST request to create a new Issue
    if request.method == 'POST':
        action = request.form.get('action', '')  # Button clicked ('Issue' or 'Return')
        member_id = request.form.get('member_id', '')
        bookID = request.form.get('bookID', '')

        # Safely convert number of books to integer
        try:
            quantity = int(request.form.get('quantity'))
            if quantity < 0:
                raise Exception("Quantity must be larger than 0")  # Prevent negative quantity

            if member_id:
                member_record = Members_table.query.get(member_id)
                if member_record == None:
                    raise Exception(f"User with Member ID: {member_id} not found")
                if member_record.debt >= 500:
                    raise Exception(f"User with Member ID: {member_id} has an outstanding debt more than or equal to Rs.500")
            else:
                raise Exception(f"Member ID is required")

            if bookID:
                book_record = Books_table.query.get(bookID)
                if book_record == None:
                    raise Exception(f"Book ID: {bookID} not found")
            else:
                raise Exception(f"Book ID is required")

            debt = quantity * 10

            # Find the issued book record
            issued_book_record = IssuedBooks.query.filter_by(member_id=member_id, bookID=bookID).first()
            
            if action == 'Issue':
                if book_record.quantity < quantity:
                    raise Exception(f"Not enough stock for book ID {bookID}")

                total_debt = member_record.debt + debt
                if total_debt >= 500:
                    raise Exception("Issue is not allowed because the debt will exceed the RS.500 limit")

                if issued_book_record == None:
                    # Create an entry in IssuedBooks
                    issued_book = IssuedBooks(member_id=member_id, bookID=bookID, quantity=quantity)
                    db.session.add(issued_book)
                else:
                    issued_book_record.quantity += quantity

                # Decrement stock in Books
                book_record.quantity -= quantity
            
            elif action == 'Return':
                if issued_book_record == None:
                    raise Exception("No Issue Record found")

                if issued_book_record.quantity < quantity:
                    raise Exception(f"Not enough rented quantity for book ID {bookID}")

                # Decrement quantity in IssuedBooks
                issued_book_record.quantity -= quantity

                # Increase stock in Books
                book_record.quantity += quantity
                
                # Remove the rented book record if the quantity goes to 0
                if issued_book_record.quantity == 0:
                    db.session.delete(issued_book_record)

                total_debt = member_record.debt - debt
                if total_debt < 0:
                    total_debt = 0

            # Updating debt
            member_record.debt = total_debt

            # Create a new transaction
            transaction = Transactions(bookID=bookID, member_id=member_id, quantity=quantity, action=action)
            db.session.add(transaction)

            # Commit the session
            db.session.commit()

        except Exception as e:
            return render_template('index.html', message=str(e), page_uri='issues')

    issues = IssuedBooks.query.all()
    return render_template('index.html', issues=issues, page_uri='issues')