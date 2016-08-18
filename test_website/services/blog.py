import markdown
from flask import Markup

from test_website.models.news import News
from test_website.models.topic import Topic


def get_news_detail(pk):
    """
    Returns the details of one specific post

    :param pk:
    :return:
    """

    news = News.query.filter_by(id=int(pk)).first()
    news_blob = {
        'id': news.id,
        'title': news.title,
        'content': news.content,
        'report': news.report_time.strftime('%Y-%m-%d at %H:%M'),
        'topics': news.topics
    }

    return news_blob


def get_page(page_size, page_num):
    """
    Returns a page of slugs

    :param page_size:
    :param page_num:
    :return:
    """

    newses = News.query.order_by(News.created_at.desc()).offset(page_num * page_size).limit(page_size).all()
    newses_blob = []
    for news in newses:
        newses_blob.append({
            'id': news.id,
            'abstract': news.abstract,
            'report': news.report_time.strftime('%Y-%m-%d at %H:%M'),
            'topics': news.topics
        })

    return newses_blob


def get_top_tags(n):
    """
    Returns N top tags
    :param n:
    :return:
    """

    raise NotImplementedError


def get_tagged_posts(tag, limit):
    """
    Gets the most recent limit posts with a certain tag
    :param tag:
    :param limit:
    :return:
    """

    raise NotImplementedError
