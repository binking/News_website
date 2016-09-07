import re
from collections import Counter
from test_website.models.news import News
from test_website.extensions import db
from test_website.constants import STOP_WORDS, ENGLISH_WORD_REXPR
# from Stemmer import PorterStemmer
from nltk.stem.snowball import PortugueseStemmer
import matplotlib.pyplot as plt
from wordcloud import WordCloud


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
    tokens = tokens_re.findall(text)
    stems = [token.lower() for token in tokens if token.isalpha()]
    stems = [stem for stem in stems if len(stem) > 1 and not is_stop_word(stem)]
    return stems


# Why steeming remove e at the ending of token
def stemming(word):
    # stemmer = PorterStemmer()
    stemmer = PortugueseStemmer()
    stem = stemmer.stem(word)
    return stemmer.stem(stem)



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
            abstract = News.query.filter(News.id == news_id).first().abstract
            tokens = tokenize(abstract)
        bag_of_words.update([stemming(token) for token in tokens])
        # bag_of_words.update(tokens)
    # bag_of_words.update(vacabulary)
    return bag_of_words.most_common(most_freq)


if __name__=="__main__":
    try:
        wordcloud = WordCloud(width=1500,
                              height=1200,
                              max_words=200
                              ).generate_from_frequencies(word_count(200))
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()

    except KeyboardInterrupt:
        print("Stop")
