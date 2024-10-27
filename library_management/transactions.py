from flask import render_template, Blueprint
from .db import Transactions

bp = Blueprint('transactions', __name__, url_prefix='/transactions')

@bp.route('/', methods=['GET'])
def index():
    transactions = Transactions.query.all()
    return render_template('index.html', transactions=transactions)