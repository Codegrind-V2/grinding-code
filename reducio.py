from article_summarizer import ArticleSummarizer
from corpus_reader import CorpusReader


def reducio(article, sentence_number):
    corpus_reader = CorpusReader()

    article = article.replace('\n', ' ').replace('\r', '')

    summary = ArticleSummarizer(article, corpus_reader.document_number,
                                corpus_reader.document_frequency)
    
    top_sentences = summary.get_top_sentences(sentence_number)

    summarized_article = ''
    for sentence in top_sentences:
        summarized_article += ('<p>' + sentence + '</p>')

    return summarized_article
