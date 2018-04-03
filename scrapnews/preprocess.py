"""
This is where preprocessing happens.
input: text
output: preprocessed text (string)
"""
from gensim.utils import simple_preprocess
from nltk.corpus import wordnet as wn
import os
import nltk
import string

STOP_PATH = os.path.join(os.path.dirname(__file__), 'spiders', 'stop-words.txt')

PUNKTS = ["''",'``','...','’','‘','-']

with open(STOP_PATH,"r") as f:
    STOP_WORDS = f.read().split('\n')


def preprocess(text):

    tokens = [t.lower() for t in nltk.word_tokenize(text) if
              (t.lower() not in STOP_WORDS or t =='May') and t not in PUNKTS and t not in string.punctuation]
    tokens = [wn.morphy(t) if wn.morphy(t) is not None else t for t in tokens]
    return " ".join(tokens)
    #
    # tokens = simple_preprocess(text)
    #
    # tokens = [t for t in tokens if t not in STOP_WORDS]
    #
    # tokens = [wn.morphy(t) if wn.morphy(t) is not None else t for t in tokens]
    #
    # return " ".join(tokens)