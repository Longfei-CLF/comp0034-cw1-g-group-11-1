from flask import Blueprint, render_template

# main_bp = Blueprint('main', __name__, url_prefix='/main')
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html', title="Home")