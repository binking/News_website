import re
from collections import Counter
from test_website.models.news import News
from test_website.extensions import db
from test_website.constants import STOP_WORDS, ENGLISH_WORD_REXPR
# from Stemmer import PorterStemmer
# from nltk.stem.snowball import PortugueseStemmer


def load_stop_words():
    stop_words = []
    with open("test_website/static/json/stop_words.txt", "r") as fr:
        for line in fr.readlines():
            stop_words.append(line.strip())
    return stop_words


def tokenize(text):
    tokens_re = re.compile(r'(' + '|'.join(ENGLISH_WORD_REXPR) + ')', re.VERBOSE | re.IGNORECASE)
    # text_without_dot = re.sub("\.", "\n", text)
    # tokens = text.lower().split()
    # import ipdb;ipdb.set_trace()
    # stems = [stemming(token) for token in tokens if token.isalpha()]
    tokens = tokens_re.findall(text.lower())
    stems = [token for token in tokens if token.isalpha() and len(token) > 1]
    stems = [stem for stem in stems if not is_stop_word(stem)]
    return stems


# Why steeming remove e at the ending of token
def stemming(word):
    # stemmer = PorterStemmer()
    stemmer = PortugueseStemmer()
    # stem = stemmer.stem(word, 0, len(word)-1)
    return stemmer.stem(word)


def is_stop_word(word,):
    if word in STOP_WORDS:
        return True
    return False


def word_count(most_freq=30):
    # vacabulary = []
    bag_of_words = Counter()
    news_id_text_dict = dict((ins.id, ins.content) for ins in db.session.query(News.id, News.content).all())
    for news_id in news_id_text_dict:
        if news_id_text_dict[news_id]:
            tokens = tokenize(news_id_text_dict[news_id])
        else:
            abstract = News.query.filter(News.id==news_id).first().abstract
            tokens = tokenize(abstract)
        bag_of_words.update(tokens)

    return bag_of_words.most_common(most_freq)


if __name__=="__main__":
    try:
        print(word_count(50))
    except KeyboardInterrupt:
        print("Stop")
