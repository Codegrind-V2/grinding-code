from json import dump, load
from pandas import read_csv

from tokenizer import tokenize_word


class CorpusReader:
    """Corpus reader

    Try to open JSON file containing document number and document frequency.
    If fails, open corpus dataset and count the document frequency of each word.
    """

    def __init__(self):
        """Inits CorpusReader

        Try to open JSON file containing document number and frequency.

        If it fails, open corpus dataset.
        Count the document frequency of each word.
        """

        self.document_frequency = {}

        try:
            with open('news.json', 'r') as jsonfile:
                cache = load(jsonfile)

                self.document_number = cache[0]
                self.document_frequency = cache[1]
        except IOError:
            with open('data/news.json', 'w') as jsonfile:
                self.__articles = []

                self.__open_corpus()
                self.__count_document_frequency()

                self.document_number = len(self.__articles)

                dump((self.document_number, self.document_frequency), jsonfile)

    def __open_corpus(self):
        # open corpus dataset and store it in self.__articles

        with open('reducio/data/news.csv') as csvfile:
            reader = read_csv(csvfile)
            for entry in reader['body']:
                self.__articles.append(str(entry))

    def __count_document_frequency(self):
        # count the document frequency of each word

        for article in self.__articles:
            words = set(tokenize_word(article))
            for word in words:
                if word not in self.document_frequency:
                    self.document_frequency[word] = 1
                else:
                    self.document_frequency[word] += 1
