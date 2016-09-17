import re, time, traceback, os
import threading
import datetime as dt
from urllib.request import urlopen
# from queue import Queue
from lxml import html
import feedparser
from sqlalchemy.exc import SQLAlchemyError
from news_website.utils import retry
from news_website.operations.tools import NewsUrlCache
from news_website.app import create_app
from news_website.settings import OSxConfig, TestConfig
from news_website.constants import *
from news_website.models.news import News
from news_website.models.topic import Topic
from news_website.extensions import db
# news_cache = NewsUrlCache(100)
"""
from os.path import dirname, join, abspath
PREFIX = abspath(join(dirname(abspath(__file__)), '../'))
PARENT = abspath(join(dirname(abspath(__file__)), '../../'))
if PREFIX not in sys.path:
    sys.path.append(PREFIX)
    sys.path.append(PARENT)
"""


def parse_rss(url):
    rss = feedparser.parse(url)
    data = []
    for entry in rss['entries']:
        data.append([entry['title'], entry['link'], entry['summary']])
    return data


def _get_time_from_page(root):
    time_str = ""
    paths_to_time = ['.//div[@class="date date--v2"]',
                     './/p[@class="date date--v1"]']
    path_to_time = './/time[@data-timestamp-inserted="true"]'
    for time_path in paths_to_time:
        time_ele = root.find(time_path)
        if time_ele and (time_ele.get('data-seconds', 0)):
            # print("Efficient time path is ", time_path)
            time_str = time_ele.get("data-seconds", "")
    if not time_str:
        time_ele = root.find(path_to_time)
        if time_ele:
            # print("Efficient time path is", path_to_time)
            time_str = time_ele.get("timestamp", "")
    if time_str:
        return dt.datetime.fromtimestamp(int(time_str))
    return


def _get_title_from_page(root):
    default_title = ""
    title_ele = root.xpath('.//h1')
    if title_ele:
        return title_ele[0].text
    return default_title


def _get_content_from_page(root):
    content = ""
    paths_to_text = [
        './/div[@class="story-body__inner"]',
        './/div[@class="story-body sp-story-body gel-body-copy"]',
        './/div[@class="map-body"]',
        './/div[@class="map-body display-feature-phone-only"]']
    for text_path in paths_to_text:
        body_ele = root.find(text_path)
        if body_ele:
            # content = body_eles[0].text_content()
            for p_ele in body_ele.xpath("p"):
                p_text = p_ele.text_content()
                if p_text:
                    content += p_text + "\n\n"
            break
    return content


def _get_topic_from_page(root):
    path_to_topic = './/a[@class="mini-info-list__section"]'
    default_topic = "Others"
    default_topic_url = ""
    topic_ele = root.find(path_to_topic)
    if topic_ele:
        default_topic = topic_ele.text
        default_topic_url = topic_ele.get("href", "")
    return default_topic, default_topic_url


@retry(RETRY_TIMES)
def parse_news_page(url):
    data = {}
    root = html.parse(url)
    topic_info = _get_topic_from_page(root)
    data.update(
        title=_get_title_from_page(root),
        body=_get_content_from_page(root),
        report_time=_get_time_from_page(root),
        topic=topic_info[0],
        topic_url=BBC_WEBSITE + topic_info[1]
    )

    return data


def is_news_url(url):
    news_url_re = re.compile(r'(' + '|'.join(NEWS_URL_REXPR) + ')', re.VERBOSE | re.IGNORECASE)
    if re.search(news_url_re, url):
        return True
    return False


def regularize_url(url):
    if url.startswith('http'):
        return url
    else:
        return "http://www.bbc.com" + url


@retry(RETRY_TIMES)
def extract_news_urls_from_page(url):
    """
    Given url, extract all urls for news article.
    Be care: the article should be omitted if its content is ""
    How-to: news'url starts with "/news/", "/sport/" or "http://www.bbc.com/", ends with number
    :param url: given url to process
    :return: list of news urls
    """
    urls_list = []
    page = urlopen(url, timeout=10)
    text = str(page.read())
    root = html.fromstring(text)
    a_tags = root.xpath(".//a[@href]")
    for tag in a_tags:
        link = tag.get("href")
        if is_news_url(link):
            urls_list.append(regularize_url(link))
    return urls_list


def is_news_existed(url):
    """
    Adjust whether the url was existed database
    :param url: url to scrap
    :return: True / False
    """
    # if url in news_cache:
    #    return True
    existed_news = News.query.filter_by(source_url=url).first()
    if existed_news:  # not existed in cache, but in database
        return True
    return False


def save_info_by_url(url):
    """
    Parse url and save info into database
    :param url:
    :return: Success/Failed
    """
    if is_news_existed(url):  # url already existed
        # news_cache.push(url)
        # urls_to_parse
        print("*"*8, "Url existed", "*"*8)
        return
    url_info = parse_news_page(url)
    if url_info["body"] == "":  # this is not news url
        print("*"*8, "Invalid Url", "*"*8)
        return
    news_article = News(
        title=url_info['title'],
        source_url=url,
        content=url_info['body'],
        report_time=url_info['report_time']
    )
    assigned_topic = Topic.query.filter_by(topic=url_info['topic']).first()
    if assigned_topic:
        # the topic existed, assign the news to this topic
        assigned_topic.newses.append(news_article)
    else:
        new_topic = Topic(topic=url_info['topic'], category_url=url_info['topic_url'])
        new_topic.newses.append(news_article)
        db.session.add(new_topic)
    db.session.commit()
    # news_cache.push(url)  # save this url in cache for next adjustment
    print("<"*8, "Hi, write success ($_$) ", ">"*8)


def recursive_scrap_news(start_url, max_iter=5, iter_time=0):
    """
    Recusive scraping news like a spider, never stop until max iteration
    :param start_url: given start point
    :param max_iter: max num of iteration
    :param iter_time: how many times recursively scrping
    :return:
    """
    deepth = iter_time
    print("\n********** Deepth is %d now **********" % deepth)
    if deepth >= max_iter:
        # Go to maximum iteration
        print("It's max iteration, then go back to last iteration....")
        return
    # import ipdb; ipdb.set_trace()
    news_url_list = extract_news_urls_from_page(start_url)
    # Write data in database
    for url in news_url_list:
        print("News' URL: ", url)
        try:
            save_info_by_url(url)
            recursive_scrap_news(url, max_iter=max_iter, iter_time=deepth+1)
        except SQLAlchemyError as e:
            print("Write Database error")
            traceback.print_exc(e)
            continue
        except Exception as e:
            print("Terrible !!! (>_<)")
            traceback.print_exc()
            continue
        except KeyboardInterrupt:
            print("Quit in force by YOU, save data before I leave ....")
            db.session.commit()
            break


def create_collector_thread(url, max_iter):
    thread = threading.Thread(target=recursive_scrap_news, args=(url, max_iter))# (target=worker, args=(limit, jobs, results))
    thread.daemon = True
    thread.start()


def main():
    if os.environ.get("HOME") == '/Users/chibin':  # mac env
        app = create_app(OSxConfig)
    else:
        app = create_app(TestConfig)

    with app.app_context():
        # urls_to_parse = Queue()
        categories_list = [
            "http://www.bbc.com/news/world",
            "http://www.bbc.com/news/world/asia",
            "http://www.bbc.com/news",
            "http://www.bbc.com/news/science_and_environment",
            "http://www.bbc.com/news/entertainment_and_arts",
            "http://www.bbc.com/news/asia/health",
            "http://www.bbc.com/news/world/asia/china"
        ]
        for cate in categories_list:
            print("\nStart url: ", cate, "\n\n")
            recursive_scrap_news(cate, max_iter=3)
        # create_collector_thread(url, max_iter=20)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Time consuming: %d" % (time.time() - start_time))
'''

def collect_news():
    """
   :param data: list of lists --> [title, link, summary]
   :param RSS_SOURCE: dict of {topic, rss_url}
   :function: collect articles and save them into database
   """
    for topic, rss in RSS_SOURCES.items():
        rss_data = parse_rss(rss)
        for data in rss_data:
            existed_news = News.query.filter_by(source_url=data[1]).first()
            print(data[1])
            if existed_news:
                print("Existed article, omit.....")
                break
            page_info = parse_news_page(data[1])
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


'''