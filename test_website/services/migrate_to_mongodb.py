import os
from flask_pymongo import PyMongo

from os.path import dirname, join, abspath
PREFIX = abspath(join(dirname(abspath(__file__)), '../'))
PARENT = abspath(join(dirname(abspath(__file__)), '../../'))
if PREFIX not in sys.path:
    sys.path.append(PREFIX)
    sys.path.append(PARENT)

from test_website.app import create_app, create_mongo_app
from test_website.settings import DevConfig, ProdConfig
from test_website.extensions import db, mongo
from test_website.models.news import News
from test_website.models.user import User
from test_website.models.topic import Topic

def migrate_mysql_to_mongodb():
    all_users = User.query.all()
    all_news = News.query.all()
    pass


if __name__=="__main__":
    if os.environ.get("TEST_WEBSITE_ENV") == 'prod':
        mysql_app = create_app(ProdConfig)
        mongo_app = create_mongo_app(ProdConfig)
    else:
        mysql_app = create_app(DevConfig)
        mongo_app = create_mongo_app(DevConfig)

    with mysql_app.app_context(), mongo_app.app_context():
        print("I am In")
        migrate_mysql_to_mongodb()