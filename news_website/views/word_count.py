from news_website.extensions import login_manager
from flask_login import login_user
from flask import Blueprint

blueprint = Blueprint('news', __name__, static_folder="../static")


@blueprint.route('/stat/', methods=['GET'])
def count_word():
    pass