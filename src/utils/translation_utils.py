import numpy as np
import re
from nltk.util import ngrams
from sklearn.metrics.pairwise import cosine_similarity


def clean_text(text_):
    """
    Cleans the text, so it can be used to find similar words.
    
    :param text_: The text we would like to clean.
    :return: Cleaned text.
    """
    text_ = text_.lower()
    text_ = text_.replace('.', ' ')
    text_ = text_.replace(',', ' ')
    text_ = text_.replace('"', ' ')
    text_ = text_.replace('(', ' ')
    text_ = text_.replace(')', ' ')
    text_ = text_.replace('„', ' ')
    text_ = text_.replace('“', ' ')
    text_ = text_.replace('°', ' ')
    text_ = text_.replace('/', ' ')
    text_ = text_.replace('\\', ' ')
    text_ = text_.replace('[', ' ')
    text_ = text_.replace(']', ' ')
    text_ = text_.replace('{', ' ')
    text_ = text_.replace('}', ' ')
    text_ = text_.replace(';', ' ')
    text_ = text_.replace(':', ' ')
    text_ = text_.replace('\'\'', ' ')
    text_ = re.sub('\s+', ' ', text_)
    return text_


def get_grams(text, from_=1, to_=3):
    """
    Takes text as an input and returns N-grams, which are consecutive strings
    of N words.

    :param text: Text to convert to n-grams.
    :param from_: The size of the smallest n-gram.
    :param to_: The size of the biggest n-gram.
    :return: Generator that returns n-grams.
    """
    grams = []
    text_split = text.split()
    max_grams = len(text_split) + 1
    for i_ in range(from_, min(to_ + 1, max_grams)):
        grams.append(list(map(lambda x: list(x), ngrams(text_split, i_))))
    return grams


def grams_to_embeddings(ngrams_list, model_):
    """
    Transforms N-grams to word embeddings that are needed for
    calculating similarity between N-grams.

    :param ngrams_list: N-grams which we want to transform.
    :param model_: FastText model used for calculating word embeddings.
    :return: FastText word embeddings vectors.
    """
    result = []
    for ngrams_ in ngrams_list:
        n_result = []
        for ngram in ngrams_:
            print(f'N: {ngram}')
            n_result.append(model_.get_sentence_vector(' '.join(ngram)))

        if n_result:
            result.append(n_result)
    return result


def average_similarity(query_ngrams_embeddings, context_ngrams_embeddings):
    """
    Calculates average similarity between the most similar
    query n-grams and context n-grams.

    :param query_ngrams_embeddings: n-grams for the text we want to find in context
    :param context_ngrams_embeddings: n-grams for the context
    :return: average of n-grams similarities with the highest similarities
    """
    if len(query_ngrams_embeddings) == 0 or len(context_ngrams_embeddings) == 0:
        print('Warning: parameter query_embeddings or context_embeddings is an empty list.')
        return -1, -1

    similarities = []
    for query_embedding in query_ngrams_embeddings:
        tmp = []
        for context_embedding in context_ngrams_embeddings:
            s = cosine_similarity(query_embedding, context_embedding)[0][0]
            tmp.append(s)
            print(s)

        similarities.append(tmp)

    indexes = []
    max_similarities = []
    for similarity_matrix in similarities:
        argmax = np.argmax(similarity_matrix)
        indexes.append(argmax)
        max_similarities.append(similarity_matrix[argmax])

    return indexes, similarities


def weighted_similarity(average_similarities):
    """
    Calculates weighted similarities based on the formula
    from the article. The longest n-gram has the biggest
    weight.

    :param average_similarities: average similarities between the most similar n-grams
    :return: weighted similarity of different lengths of n-grams
    """
    g = len(average_similarities)
    denominator = g * (g + 1) / 2
    return sum((i_ + 1) * avg_similarity / denominator for i_, avg_similarity in enumerate(average_similarities))


def find_similar_text(query, context, fasttext_model, start_n=1, end_n=3):
    """
    Finds the most similar word in text based on the FastText
    word embedding model and cosine similarity between n-grams.

    :param query: the text we are searching for
    :param context: the text in which we are searching
    :param fasttext_model: pre-trained FastText model for calculating word embeddings
    :param start_n: the size of the smallest n-gram
    :param end_n: the size of the larges n-gram
    :return: index of the first word in the context and the weighted similarity score
    """

    # Very important to clean text beforehand
    query = clean_text(query)
    context = clean_text(context)

    average_similarities_by_ngram = []
    start_indexes_by_ngram = []
    for query_grams, context_grams in zip(get_grams(query, start_n, end_n), get_grams(context, start_n, end_n)):

        best_similarities_by_gram = []
        start_indexes_by_gram = []
        for query_gram in query_grams:
            similarities = []
            for context_gram in context_grams:
                query_gram_text = ' '.join(query_gram)
                context_gram_text = ' '.join(context_gram)
                query_embedding = fasttext_model.get_sentence_vector(query_gram_text)
                context_embedding = fasttext_model.get_sentence_vector(context_gram_text)
                similar = cosine_similarity([query_embedding], [context_embedding])[0][0]
                similarities.append(similar)

            best_index = np.argmax(similarities)
            best_similarity = similarities[best_index]

            best_similarities_by_gram.append(best_similarity)
            start_indexes_by_gram.append(best_index)

        start_indexes_by_ngram.append(start_indexes_by_gram[0])
        average_similarities_by_ngram.append(sum(best_similarities_by_gram) / len(best_similarities_by_gram))

    return start_indexes_by_ngram, average_similarities_by_ngram

