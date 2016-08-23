import markdown
from flask import Markup
from sqlalchemy import func, desc

from test_website.models.news import News
from test_website.models.relationships import topics_newses
from test_website.models.topic import Topic
from test_website.extensions import db

def get_news_detail(pk):
    """
    Returns the details of one specific post

    :param pk:
    :return: news_blob: {
        'id':,
        'title':,
        'content':,
        'report_time':,
        'topics':,
    }
    """

    news = News.query.filter_by(id=int(pk)).first()
    news_blob = {
        'id': news.id,
        'title': news.title,
        'content': news.content,
        'report_time': news.report_time.strftime('%Y-%m-%d %H:%M'),
        'topics': news.topics,
    }

    return news_blob


def get_page(page_size, page_num):
    """
    Returns a page of slugs

    :param page_size:
    :param page_num:
    :return:
    """

    newses = News.query.order_by(News.report_time.desc()).offset(page_num * page_size).limit(page_size).all()
    newses_blob = []
    for news in newses:
        newses_blob.append({
            'id': news.id,
            'title': news.title,
            'abstract': news.abstract,
            'report_time': news.report_time.strftime('%Y-%m-%d %H:%M'),
            'topics': news.topics
        })

    return newses_blob


def get_hot_topics(n):
    """
    Returns N top tags
    :param n:
    :return:
    """
    # SELECT count(newses.id) AS qty FROM newses
    # GROUP BY newses.id = topics_newses.news_id
    # AND topics.id = topics_newses.topic_id
    # ORDER BY qty DESC
    # results = db.session.query(
    #    func.count(News.id).label('qty')
    #    ).group_by(News.topics
    #    ).order_by(desc('qty')).all()
    # import ipdb;ipdb.set_trace()
    topic_freq = {}
    all_topics = db.session.query(Topic.topic).all()
    for topic in all_topics:
        t = topic.topic
        print(t)
        newses = News.query.filter(News.topics.any(topic=t)).all()
        topic_freq[t] = len(newses)
    results = sorted(topic_freq.items(), key=lambda x:x[1], reverse=True)[:n]
    return results


def get_number_of_newses():
    return len(News.query.all())

def get_newses_of_topic(topic, page_size, page_num):
    """
    Gets the most recent limit posts with a certain tag
    :param tag:
    :param limit:
    :return:
    """
    newses_of_given_topic = News.query.order_by(
        News.report_time.desc()
    ).filter(News.topics.any(topic=topic)).offset(page_num * page_size).limit(page_size).all()
    return newses_of_given_topic
