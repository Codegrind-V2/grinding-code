import re

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize


def tokenize_word(text):
    """ Tokenize a text into words using NLTK

    Filter punctuations (non-alphanumeric characters) except period.
    Tokenize text into words.
    Filter periods.
    Filter stop words and empty words.
    Stem words.
    Filter non-noun words, if only_noun=true

    Args:
        text: Text to be tokenized into words.
        only_noun: A boolean, if true then filter non-noun words
    Returns:
        A list of word tokens.
    """

    text = text.lower()

    pattern = re.compile(r'[^a-zA-Z.]+')
    text = pattern.sub(' ', text)

    word_tokens = word_tokenize(text)

    pattern = re.compile(r'\.+')
    word_tokens = [pattern.sub('', word) for word in word_tokens]

    stop_words = set(stopwords.words('english'))
    word_tokens = [word for word in word_tokens if word and word not in stop_words]

    stemmer = SnowballStemmer('english')
    word_tokens = [stemmer.stem(word) for word in word_tokens]

    return word_tokens


def tokenize_sentence(text):
    """Tokenize a text into sentences using NLTK

    Args:
        text: Text to be tokenized into sentences.
    """

    sentence_tokens = sent_tokenize(text, language='english')

    return sentence_tokens
