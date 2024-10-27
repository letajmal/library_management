from flask import Flask, render_template, Blueprint, request
import requests
from .db import db, Members_table, IssuedBooks

bp = Blueprint('members', __name__, url_prefix='/members')

@bp.route('/', methods=('GET', 'POST'))
def index():
    # Handle POST request to create a new member
    if request.method == 'POST':
        action = request.form.get('action', '')  # Button clicked ('Search' or 'Update')

        if action == 'Add':
            name = request.form.get('name', '')
            if name:
                try:
                    # Create and add a new member
                    new_member = Members_table(name=name)
                    db.session.add(new_member)
                    db.session.commit()
                except Exception as e:
                    return render_template('index.html', message=str(e), page_uri='members')
        
        elif action == 'Delete':
            member_id = request.form.get('member_id', '')
            if member_id:
                try:
                    # Delete Member
                    # Check if the member exists
                    member = Members_table.query.get(member_id)
                    if member == None:
                      raise Exception(f"User with Member ID: {member_id} not found")

                    # Check if the member has rented books
                    rented_books = IssuedBooks.query.filter_by(member_id=member_id).all()
                    if rented_books:
                        raise Exception("Cannot delete member with rented books.")

                    # If no rented books, proceed with deleting the member
                    db.session.delete(member)
                    db.session.commit()
                except Exception as e:
                    return render_template('index.html', message=str(e), page_uri='members')
    
    members = Members_table.query.all()
    return render_template('index.html', members=members, page_uri='members')