# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint

from test_website.services.news import get_page, get_news_detail
from test_website.utils import flash_errors, render_extensions

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

    return render_extensions("news/news_page.html",
                             newses=newses,
                             next_page=next_page,
                             prev_page=prev_page,
                             current=current)


@blueprint.route("/news_detail/<pk>/", methods=["GET"])
def news_detail(pk):
    """

    :param pk:
    :return:
    """

    news = get_news_detail(int(pk))
    return render_extensions("news/news_detail.html", news=news)