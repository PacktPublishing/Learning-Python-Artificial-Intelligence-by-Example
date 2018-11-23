"""
Functions to clean text
"""

import string
from gensim import corpora, utils, models, similarities

import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.corpus import wordnet
nltk.download('wordnet')


# Punctuation and stop words to be removed later
punctuation = set(string.punctuation)
stoplist = set(stopwords.words('english'))

# For LDA training later
dictionary = corpora.Dictionary()
lemma = WordNetLemmatizer()


def remove_punctuation(text):
    """
    Remove punctuation from text by checking each character against a set of punctation characters
    :text: string
    :return: string
    """
    return ''.join(char for char in text if char not in punctuation)


def remove_numbers(text):
    """
    Remove numbers from text as they aren't of value to our model
    :text: string
    :return: string
    """
    return ''.join(char for char in text if not char.isdigit())


def remove_stop_words(text):
    """
    Remove common words as they won't add any value to our model
    :text: string
    :return: string
    """
    return ' '.join([word for word in text.split() if word not in stoplist])


def remove_single_characters(text):
    """
    Remove any remaining single-character words
    :text: string
    :return: string
    """
    return ' '.join([word for word in text.split() if len(word) > 1])


def lemmatize(text):
    """
    Use NLTK lemma functionality to get the route word
    :text: string
    :return: string
    """
    return ' '.join([lemma.lemmatize(word) for word in text.split()])


def get_cleaned_text(text):
    """
    Return the page with stopwords, digits, punctuation and single character words removed
    :text: string
    :return: string
    """
    # Remove \n characters (Wikipedia has a lot of them in the page content!)
    text = text.replace('\n', '')
    # Remove numbers
    text = remove_numbers(text)
    # Remove stop words
    text = remove_stop_words(text)
    # Remove punctuation
    text = remove_punctuation(text)
    # Remove single character words
    text = remove_single_characters(text)
    # Lemmatize the document
    text = lemmatize(text)
    return text
