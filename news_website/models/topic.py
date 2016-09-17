import datetime
from news_website.extensions import db
from news_website.models.relationships import topics_newses
from news_website.database import (
    Model,
    SurrogatePK,
)


class Topic(SurrogatePK, Model):

    __tablename__ = 'topics'

    topic = db.Column(db.Text, default='')
    category_url = db.Column(db.Text, default='')
    newses = db.relationship('News', secondary=topics_newses, backref=db.backref('topics_br', lazy='dynamic'))
    creat_at = db.Column(db.DateTime, default=datetime.datetime.now())
    status = db.Column(db.Integer, default=1)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)