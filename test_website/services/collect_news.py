import datetime as dt
import traceback, sys, os, time
from urllib.request import urlopen
from socket import error as SocketError
from io import StringIO
from lxml import etree
import feedparser

from os.path import dirname, join, abspath
PREFIX = abspath(join(dirname(abspath(__file__)), '../'))
PARENT = abspath(join(dirname(abspath(__file__)), '../../'))
if PREFIX not in sys.path:
    sys.path.append(PREFIX)
    sys.path.append(PARENT)

from test_website.app import create_app
from test_website.settings import DevConfig, ProdConfig
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

def _get_time_from_page(root):
    default_time = dt.datetime.now()
    time_str = ""
    paths_to_time = ['.//div[@class="date date--v2"]',
                    './/p[@class="date date--v1"]']
    path_to_time = './/time[@data-timestamp-inserted="true"]'
    for time_path in paths_to_time:
        time_ele = root.find(time_path)
        if (time_ele is not None) and (time_ele.get('data-seconds', 0)):
            print("Effiecient time path is ", time_path)
            time_str = time_ele.get("data-seconds", "")
    if not time_str:
        time_ele = root.find(path_to_time)
        if time_ele is not None:
            print("Effiecient time path is", path_to_time)
            time_str = time_ele.get("timestamp", "")
    if time_str:
        default_time = dt.datetime.fromtimestamp(int(time_str))
    return default_time

def _get_content_from_page(root):
    default_content = ""
    paths_to_text = ['.//div[@class="story-body__inner"]',
                    './/div[@class="story-body sp-story-body gel-body-copy"]',
                    './/div[@class="map-body"]']
    for text_path in paths_to_text:
        body_ele = root.find(text_path)
        if body_ele is not None:
            print("Effiecient body path is ", text_path)
            for p_ele in body_ele.findall("p"):
                if p_ele.text:
                    default_content += p_ele.text
    return default_content

def _get_topic_from_page(root):
    path_to_topic = './/a[@class="mini-info-list__section"]'
    default_topic = "Others"
    default_topic_url = ""
    topic_ele = root.find(path_to_topic)
    if topic_ele is not None:
        default_topic = topic_ele.text
        default_topic_url = topic_ele.get("href", "")
    return default_topic, default_topic_url

def parse_bbc_page(url):
    try_time = 0
    sleep_time = 0
    data = {}
    page_url = url

    while try_time < RETRY_TIMES:
        try:
            try_time += 1
            page = urlopen(page_url, timeout=10)
            # import ipdb;ipdb.set_trace()
            text = str(page.read())
            root = etree.parse(StringIO(text), etree.HTMLParser()).getroot()
            topic_info = _get_topic_from_page(root)
            data.update(body=_get_content_from_page(root),
                        report_time=_get_time_from_page(root),
                        topic=topic_info[0],
                        topic_url= BBC_WEBSITE + topic_info[1]
                        )
            break
        # print(len(data.values()))
        except AttributeError as e:
            traceback.print_exc()
            print("Attribute error")
            break
        except SocketError as e:
            traceback.print_exc()
            print("Try more %d times" % (RETRY_TIMES - try_time))
        except Exception as e:
            # import ipdb;ipdb.set_trace()
            traceback.print_exc()
            print("Try more %d times" % (RETRY_TIMES - try_time))
        time.sleep(pow(2, sleep_time + 1))
        sleep_time += 1

    return data


def collect_news():
    """
   :param data: list of lists --> [title, link, summary]
   :param RSS_SOURCE: dict of {topic, rss_url}
   :function: collect articles and save them into database
   """
    for topic, rss in RSS_SOURCES.items():
        rss_data = parse_rss(rss)
        for data in rss_data:
            print(data[1])
            existed_news = News.query.filter_by(source_url=data[1]).first()
            if existed_news:
                print("Existed article, omit.....")
                break
            page_info = parse_bbc_page(data[1])
            if page_info:
                try:
                    news_acrticle = News(title=data[0],
                                         source_url=data[1],
                                         abstract=data[2],
                                         content=page_info['body'],
                                         report_time=page_info['report_time'])
                    assigned_topic = Topic.query.filter_by(topic=page_info['topic']).first()
                    if assigned_topic:
                        # the topic existed, assign the news to this topic
                        assigned_topic.newses.append(news_acrticle)
                    else:
                        new_topic = Topic(topic=page_info['topic'], category_url=page_info['topic_url'])
                        new_topic.newses.append(news_acrticle)
                        db.session.add(new_topic)
                    db.session.commit()
                    print("Hi, write success ($_$) ")
                except Exception as e:
                    print("Terrible !!! (>_<)")
                    traceback.print_exc()


if __name__=="__main__":
    if os.environ.get("TEST_WEBSITE_ENV") == 'prod':
        app = create_app(ProdConfig)
    else:
        app = create_app(DevConfig)

    with app.app_context():
        print("I am In")
        collect_news()