# -*- coding: utf-8 -*-
"""Public section, including homepage and signup.
 operation/ files shouldn't be related to web front
"""

from flask import Blueprint

from news_website.operations.op_news import (
    get_page,
    get_news_detail,
    get_newses_of_topic,
    get_hot_topics,
    get_number_of_newses
)
from news_website.utils import render_extensions

blueprint = Blueprint('news', __name__, static_folder="../static")


@blueprint.route("/news/<page>/", methods=["GET"])
def news_page(page=None):
    """

    :param page:
    :return:
    """

    page = int(page)
    _page_size = 3  # TODO: move into settings

    if page is None or page <= 0:
        next_page = 0
        prev_page = 1
        current = True
    else:
        next_page = page - 1
        prev_page = page + 1
        current = False

    newses = get_page(_page_size, page)
    hot_topics = get_hot_topics(5)
    return render_extensions("news/news_page.html",
                             newses=newses,
                             next_page=next_page,
                             prev_page=prev_page,
                             hot_topics=hot_topics,
                             current=current)


@blueprint.route("/news_detail/<pk>/", methods=["GET"])
def news_detail(pk):
    """

    :param pk:
    :return:
    """
    news_index = int(pk)
    news = get_news_detail(news_index)
    hot_topics = get_hot_topics(5)
    max_index = 1 if news_index == get_number_of_newses() else 0
    return render_extensions("news/news_detail.html",
                             news=news,
                             hot_topics=hot_topics,
                             max_index=max_index)

@blueprint.route("/topic/<topic>/<page>", methods=['GET'])
def topic_page(topic, page=None):
    page = int(page)
    _page_size = 3  # TODO: move into settings

    if page is None or page <= 0:
        next_page = 0
        prev_page = 1
        current = True
    else:
        next_page = page - 1
        prev_page = page + 1
        current = False
    newses = get_newses_of_topic(topic, _page_size, page)
    hot_topics = get_hot_topics(5)
    return render_extensions("news/topic_page.html",
                             newses=newses,
                             specified_topic=topic,
                             next_page=next_page,
                             prev_page=prev_page,
                             hot_topics=hot_topics,
                             current=current)