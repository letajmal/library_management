from flask import Flask, render_template, Blueprint, request
import requests
from .db import db, Books_table

bp = Blueprint('members', __name__, url_prefix='/members')

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
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
    
    members = Members_table.query.all()
    return render_template('index.html', books=books, page_uri='books')