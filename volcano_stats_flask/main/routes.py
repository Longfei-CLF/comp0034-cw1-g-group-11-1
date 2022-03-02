from flask import Blueprint

# main_bp = Blueprint('main', __name__, url_prefix='/main')
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return "This is the authentication section of the web app"