from flask import render_template, Blueprint

bp = Blueprint('home', __name__)

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')