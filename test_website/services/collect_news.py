from urllib.request import urlopen
from io import StringIO
from lxml import etree
import feedparser
from ..constants import *

def parseRSS(url):
    rss = feedparser.parse(url)
    data = []
    for entry in rss['entries']:
        data.append([entry['title'], entry['link'], entry['summary']])
    return data

def parseBBCPage(url):
    RETRY_TIMES = 5
    try_time = 0
    path_to_text = '//*[@id="page"]/div[2]/div[2]/div/div[1]/div[1]/div[3]'
    while try_time < RETRY_TIMES:
        try:
            try_time += 1
            page = urlopen(url, timeout=30)
            text = str(page.read())
            tree = etree.parse(StringIO(text), etree.HTMLParser())
            tree.xpath('//*[@id="page"]/div[2]/div[2]/div/div[1]/div[1]/div[3]')

        except Exception as e:
            print(e)
            print("Try more %d times" % RETRY_TIMES - try_time)
