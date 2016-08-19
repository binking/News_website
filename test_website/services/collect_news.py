import datetime as dt
import traceback
from urllib.request import urlopen
from io import StringIO
from lxml import etree
import feedparser
from test_website.constants import *
from test_website.models.news import News
from test_website.models.topic import Topic
from test_website.extensions import (
    bcrypt,
    cache,
    db,
    login_manager,
    mail,
    migrate,
    debug_toolbar,
)


def parse_rss(url):
    rss = feedparser.parse(url)
    data = []
    for entry in rss['entries']:
        data.append([entry['title'], entry['link'], entry['summary']])
    return data


def parse_bbc_page(url):
    try_time = 0
    data = {}
    news_body = ""
    page_url = url
    path_to_text = './/div[@class="story-body__inner"]'
    path_to_time = './/div[@class="date date--v2"]'
    path_to_topic = './/a[@class="mini-info-list__section"]'
    while try_time < RETRY_TIMES:
        try:
            try_time += 1
            page = urlopen(page_url, timeout=30)
            # import ipdb;ipdb.set_trace()
            text = str(page.read())
            root = etree.parse(StringIO(text), etree.HTMLParser()).getroot()

            body_ele = root.find(path_to_text)
            time_ele = root.find(path_to_time)
            topic_ele = root.find(path_to_topic)
            for p_ele in body_ele.findall("p"):
                if not p_ele.text:
                    print(p_ele.text)
                    news_body += p_ele.text
            data.update(body=news_body,
                        time_stamp=int(time_ele.get('data-seconds', 0)),
                        topic=topic_ele.text,
                        topic_url= BBC_WEBSITE + topic_ele.get('href', '')
                        )
            print(len(data.values()))
        except ValueError as e:
            print("Parameter error")
        except Exception as e:
            import ipdb;ipdb.set_trace()
            traceback.print_exc(e)
            print("Try more %d times" % (RETRY_TIMES - try_time))
    return data


def collect_news():
    for topic, rss in RSS_SOURCES.items():
        news_kw = {}
        topic_kw = {}
        rss_data = parse_rss(rss)
        for data in rss_data:
            news_kw.update(title=data[0], source_url=data[1], abstract=data[2])
            page_info = parse_bbc_page(data[1])
            print(data[1])
            if page_info:
                print(page_info.items())
                news_kw.update(content=page_info['body'],
                               topic=page_info['topic'],
                               report_time=dt.datetime.fromtimestamp(page_info['time_stamp']))
                topic_kw.update(topic=page_info['topic'],
                                category_url=page_info['topic_url'])
            try:
                db.session.add(News(news_kw))
                db.session.add(Topic(topic_kw))
                print("Hi, write success")
            except Exception as e:
                import ipdb;ipdb.set_trace()
                traceback.print_exc(e)
                print("Write database error")

if __name__=="__main__":
    collect_news()