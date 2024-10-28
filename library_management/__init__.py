import os

from flask import Flask

def create_app(test_config=None):
    from . import books, members, issues, transactions, home
    from .db import db, Books_table, Members_table, IssuedBooks, Transactions

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Configure SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library_management.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize SQLAlchemy
    db.init_app(app)

    # Create the database tables
    with app.app_context():
        db.create_all()

    # registering blueprints with app
    app.register_blueprint(home.bp)
    app.register_blueprint(books.bp)
    app.register_blueprint(members.bp)
    app.register_blueprint(issues.bp)
    app.register_blueprint(transactions.bp)

    return app