from math import log


def term_frequency(word, word_frequency):
    """Calculate tf value of a word

    Args:
        word: the word to be scored.
        word_frequency: frequency of a word in the article.
    Returns:
        A float representing the word's tf value.
    """

    return 0 if word_frequency[word] == 0 else 1 + log(word_frequency[word])


def inverse_document_frequency(word, document_number, document_frequency):
    """Calculate idf value of a word

    Args:
        word: the word to be scored.
        document_number: number of documents in dataset.
        document_frequency: Frequency of a word in documents dataset, i.e.
            if a document has word, document_frequency[word] increase by 1.
    Returns:
        A float repesenting the word's idf value.
    """

    return log(document_number / document_frequency[word])
