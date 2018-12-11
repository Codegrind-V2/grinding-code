from operator import itemgetter

from tf_idf import term_frequency as tf, inverse_document_frequency as idf
from tokenizer import tokenize_word, tokenize_sentence


class ArticleSummarizer:
    """Summarize an article

    Rank sentences in the article with tf-idf scoring algorithm.
    """

    def __init__(self, article, document_number, document_frequency):
        """ Inits ArticleSummarizer

        Tokenize the article into sentences and words.
        Count term frequency and document frequency of each word.
        Score each sentence with tf-idf.
        Weigh each sentence relative to its position.
        Rank the sentences by the score in decreasing order.

        Args:
            article: A string of article text.
            document_number: Number of documents in dataset.
            document_frequency: Frequency of a word in documents dataset, i.e.
                 if a document has word, document_frequency[word] increase by 1.
        """

        self.__sentences = tokenize_sentence(article)
        self.__document_number = document_number + 1
        self.__document_frequency = document_frequency

        self.__word_frequency = {}
        word_set = set()

        for sentence in self.__sentences:
            words = tokenize_word(sentence)
            for word in words:
                if word not in self.__word_frequency:
                    self.__word_frequency[word] = 1
                else:
                    self.__word_frequency[word] += 1

                word_set.add(word)

        for word in word_set:
            if word not in self.__document_frequency:
                self.__document_frequency[word] = 1
            else:
                self.__document_frequency[word] += 1

        self.__sentence_scores = []

        for sentence in self.__sentences:
            self.__sentence_scores.append(
                [self.__sentence_score(sentence), sentence])

        self.__weigh_sentences_by_position()

        self.__sentence_scores = sorted(
            self.__sentence_scores, key=itemgetter(0), reverse=True)

    def __sentence_score(self, sentence):
        # return a sentence's average tf-idf score

        words = tokenize_word(sentence)

        if not words:
            return 0

        total = 0
        for word in words:
            total += self.__word_score(word)

        return total / len(words)

    def __word_score(self, word):
        # return a word's tf-idf score

        return tf(word, self.__word_frequency) * idf(
            word, self.__document_number, self.__document_frequency)

    def __weigh_sentences_by_position(self):
        # weigh each sentence relative to its position.

        # weight values are taken from a paper by Yohei Seki
        # http://research.nii.ac.jp/ntcir/workshop/OnlineProceedings3/NTCIR3-TSC-SekiY.pdf

        for index, __sentence_score in enumerate(self.__sentence_scores):
            distribution = index / len(self.__sentence_scores)

            if 0 <= distribution and distribution < 0.1:
                weight = 0.17
            elif 0.1 <= distribution and distribution < 0.2:
                weight = 0.23
            elif 0.2 <= distribution and distribution < 0.3:
                weight = 0.14
            elif 0.3 <= distribution and distribution < 0.4:
                weight = 0.08
            elif 0.4 <= distribution and distribution < 0.5:
                weight = 0.05
            elif 0.5 <= distribution and distribution < 0.6:
                weight = 0.04
            elif 0.6 <= distribution and distribution < 0.7:
                weight = 0.06
            elif 0.7 <= distribution and distribution < 0.8:
                weight = 0.04
            elif 0.8 <= distribution and distribution < 0.9:
                weight = 0.04
            else:
                weight = 0.15

            __sentence_score[0] *= weight

    def get_top_sentences(self, sentence_number):
        """Return top sentences from the ranked sentences

        Args:
            sentence_number: Number of top sentences to be returned.

        Returns:
            A list of top sentences.
        """

        ranked_sentences = set([
            sentence[1]
            for sentence in self.__sentence_scores[0:sentence_number]
        ])
        top_n_sentences = [
            sentence for sentence in self.__sentences
            if sentence in ranked_sentences
        ]

        return top_n_sentences
