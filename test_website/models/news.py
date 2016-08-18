import datetime
from test_website.extensions import db
from test_website.models.relationships import topics_newses
from test_website.database import (
    Column,
    Model,
    SurrogatePK,
)


class News(SurrogatePK, Model):

    __tablename__ = 'newses'

    title = db.Column(db.Text, default='')
    abstract = db.Column(db.Text, default='')
    content = db.Column(db.Text, default='')
    source_url = db.Column(db.Text, default='')
    topics = db.relationship('Topic', secondary=topics_newses, backref='newses_br', lazy='dynamic')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    report_time = db.Column(db.DateTime, default=datetime.datetime.now())
    status = db.Column(db.Integer, default=1)
    # tags = db.relationship('Tag', secondary=tags_posts, backref=db.backref('posts_br', lazy='dynamic'))

    def __init__(self, title, slug, body, **kwargs):
        db.Model.__init__(self, title=title, slug=slug, body=body, **kwargs)