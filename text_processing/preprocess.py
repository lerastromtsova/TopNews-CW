"""
This is where preprocessing happens.
input: text
output: preprocessed text (string)
"""
from nltk.corpus import wordnet as wn
import os
import nltk
import string
from text_processing.translate import translate
import re
import sqlite3

# STOP_PATH = '../../text_processing/stop-words.txt'
STOP_PATH = os.getcwd()+'/text_processing/stop-words.txt'
PUNKTS = ["''",'``','...','’','‘','-','“','"','—','”','–','–––','––', " | "]
SYM_MAP = {'â': 'a', 'Ç': 'C', 'ç': 'c', 'Ğ': 'g', 'ğ': 'g', 'İ':'I', 'ı':'i', 'î':'i', 'Ö':'O', 'ö': 'oe',
           'Ş': 'S', 'ş': 's', 'Ü': 'U', 'ü': 'u', 'é': 'e', 'à': 'a', 'è': 'e' , 'û': 'u', 'ô': 'o', 'œ': 'o',
           'ñ': 'n', 'á': 'a', 'í': 'i', 'ú': 'u', '¿': '', 'č': 'c', 'ć': 'c', 'ů': 'u', 'ei': 'ey', 'oe': 'o'}

with open(STOP_PATH, "r") as f:
    STOP_WORDS = f.read().split('\n')


def preprocess(text, with_uppercase=True):

    for p in PUNKTS:
        text = ' '.join(text.split(p))
    for p in string.punctuation:
        text = ' '.join(text.split(p))

    tokens = [wn.morphy(t) if wn.morphy(t) is not None else t for t in nltk.word_tokenize(text)]

    if with_uppercase:
        tokens = [t for t in tokens if (t.lower() not in STOP_WORDS)
                  and t not in PUNKTS and t not in string.punctuation
                  and len(t) > 1]

    else:
        tokens = [t.lower() for t in tokens if
                  (t.lower() not in STOP_WORDS)
                  and t not in PUNKTS and t not in string.punctuation
                  and len(t) > 1]

    for key, value in SYM_MAP.values():
        tokens = [t.replace(key, value) for t in tokens]

    # to_add = []
    # to_remove = []
    # for i in range(len(tokens)-1):
    #     if tokens[i].isdigit():
    #         if tokens[i + 1].isdigit():
    #             to_add.append(tokens[i] + tokens[i + 1])
    #             to_remove.append(tokens[i])
    #             to_remove.append(tokens[i + 1])
    #
    # tokens.extend(to_add)
    # tokens = [t for t in tokens if t not in to_remove]

    return tokens


conn = sqlite3.connect("db/entities.db")
c = conn.cursor()
c.execute("SELECT * FROM entities")
all_rows = c.fetchall()
DEFINITELY_ENTITIES = [row[0] for row in all_rows]


def find_entities(sentence):

    uppercase_words = []
    named_entities = set()

    for word in sentence:
        if word in DEFINITELY_ENTITIES:
            named_entities.add(word)
        elif word[0].isupper():
            if word.lower() not in STOP_WORDS:
                uppercase_words.append('Why did ' + word.lower() + ' say?')

    str_to_translate = '\n'.join(uppercase_words)

    eng = translate(str_to_translate, arg='en')
    deu = translate(eng, arg='de')
    eng1 = translate(deu, arg='en')

    eng = eng.split('\n')
    eng1 = eng1.split('\n')

    for i in range(len(eng)):
        if eng[i]:
            word = eng[i].split()[-2]
            word1 = eng1[i].split()[-2]
            if len(word) > 1 and word1[0].isupper() and word.lower() == word1.lower():
                named_entities.add(word1)
                c.execute("INSERT OR REPLACE INTO entities (name) VALUES (?)", (word1, ))
                # print(word1)

    conn.commit()

    return named_entities


def check_first_entities(list_of_ents):
    uppercase_words = []
    named_entities = {}
    for word in list_of_ents:
        uppercase_words.append('Why did ' + word.lower() + ' say?')
    str_to_translate = '\n'.join(uppercase_words)

    eng = translate(str_to_translate, arg='en')
    deu = translate(eng, arg='de')
    eng1 = translate(deu, arg='en')

    eng = eng.split('\n')
    eng1 = eng1.split('\n')

    for i in range(len(eng)):
        if eng[i]:
            word = eng[i].split()[-2]
            word1 = eng1[i].split()[-2]
            if len(word) > 1 and word1[0].isupper() and word.lower() == word1.lower():
                named_entities[word1] = True
            elif word1[0].islower() and word.lower() == word1.lower():
                named_entities[word1] = False
    return named_entities


def split_into_paragraphs(text):
    return text.split('\n')

def split_into_sentences(paragraph):
    sentenceEnders = re.compile('[.!?]')
    sentenceList = sentenceEnders.split(paragraph)
    return sentenceList