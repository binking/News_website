"""
    Define some constants to use
"""

DB_OPERATION_SUCCESS = 100
DB_OPERATION_SUCCESS_MSG = "Very Good! Wirte database success ($_$)"
DB_OPERATION_FAILED = -100
DB_OPERATION_FAILED_MSG = "Terrible!!! Failed to write database >_< "
RETRY_TIMES = 5
BBC_WEBSITE = "http://www.bbc.com"
RSS_SOURCES = {
    "Home": 'http://feeds.bbci.co.uk/news/rss.xml',
    "World": 'http://feeds.bbci.co.uk/news/world/rss.xml',
    "UK": 'http://feeds.bbci.co.uk/news/uk/rss.xml',
    "Business": 'http://feeds.bbci.co.uk/news/business/rss.xml',
    "UK Politics": 'http://feeds.bbci.co.uk/news/politics/rss.xml',
    "Health": 'http://feeds.bbci.co.uk/news/health/rss.xml',
    "Education & Family": 'http://feeds.bbci.co.uk/news/education/rss.xml',
    "Science & Environment": "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    "Technology": 'http://feeds.bbci.co.uk/news/technology/rss.xml',
    "Entertainment & Arts": 'http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml',
    "Sport": 'http://feeds.bbci.co.uk/sport/rss.xml',
    "Magazine": 'http://feeds.bbci.co.uk/news/magazine/rss.xml',
    "Africa": 'http://feeds.bbci.co.uk/news/world/africa/rss.xml',
    "Asia": 'http://feeds.bbci.co.uk/news/world/asia/rss.xml',
    "Europe": 'http://feeds.bbci.co.uk/news/world/europe/rss.xml',
    "Latin America & Caribbean": 'http://feeds.bbci.co.uk/news/world/latin_america/rss.xml',
    "Middle East": 'http://feeds.bbci.co.uk/news/world/middle_east/rss.xml',
    "China": 'http://feeds.bbci.co.uk/news/world/asia/china/rss.xml',
    "India": 'http://feeds.bbci.co.uk/news/world/asia/india/rss.xml',
    "US & Canada": 'http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml',
    "England": 'http://feeds.bbci.co.uk/news/england/rss.xml',
    "Northern Ireland": 'http://feeds.bbci.co.uk/news/northern_ireland/rss.xml',
    "Scotland": 'http://feeds.bbci.co.uk/news/scotland/rss.xml',
    "Wales": 'http://feeds.bbci.co.uk/news/wales/rss.xml',
}

STOP_WORDS = ['a', 'about', 'above', 'after', 'again', 'against', 'all',
              'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be',
              'because', 'been', 'before', 'being', 'below', 'between',
              'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't",
              'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't",
              'down', 'during', 'each', 'few', 'for', 'from', 'further',
              'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having',
              'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers',
              'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd",
              "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it',
              "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't",
              'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once',
              'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out',
              'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's",
              'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's",
              'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there',
              "there's", 'these', 'they', "they'd", "they'll", "they're", "they've",
              'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up',
              'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've",
              'were', "weren't", 'what', "what's", 'when', "when's", 'where',
              "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's",
              'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll",
              "you're", "you've", 'your', 'yours', 'yourself', 'yourselves'
]

ENGLISH_WORD_REXPR = [
        r'<[^>]+>', # HTML tags
        r'(?:@[\w_]+)', # @-mentions
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
        r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
        r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
        r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
        r'(?:[\w_]+)', # other words
        r'(?:\S)' # anything else
]