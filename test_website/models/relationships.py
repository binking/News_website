from test_website.database import db

topics_newses = db.Table('topics_newses',
                        db.Column('topic_id', db.Integer, db.ForeignKey('topics.id')),
                        db.Column('news_id', db.Integer, db.ForeignKey('newses.id'))
                        )