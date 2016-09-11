import requests, time
from lxml import html
from test_website.constants import RETRY_TIMES
from test_website.utils import retry


def scraping_news(url):
    r = requests.get('http://0.0.0.0:5000' + url)
    if r.status_code == 200:
        print(len(r.text))


@retry(RETRY_TIMES)
def get_news_urls(url):
    r = requests.get(url)
    if r.status_code == 200:
        root = html.fromstring(r.text)
        a_tags = root.xpath('.//h2/a[@href]')
        for a in a_tags:
            print(a.get('href'))
            scraping_news(a.get('href'))
        return 0
    return -1


if __name__ == "__main__":
    url = 'http://0.0.0.0:5000/news/{}'
    page_count = 0
    while True:
        res = get_news_urls(url.format(page_count))
        if res < 0:
            break
        page_count += 1
        time.sleep(1)



