"""
Give response to user answers (definitions users gave for words).

Author: Cathy Jiao
"""

from vocabtion.datamuse import Datamuse
from nltk.corpus import wordnet as wn
from vocabtion import progress as prog

# Object for calling datamuse api
datamuse_api = Datamuse()


def lookup(text, word):
    """
    Given a definition and a word check if the definition matches to the word and provide feedback.

    :param text: a string of text that is the definition
    :param word: (str)
    :return: (str) message indicating if definition was correct
    """

    # check if definition matches word
    matched = match_definition(text, word)

    # update the progress of word
    prog.update_progress(word, matched)

    # get true definition of word
    definition = get_definition(word)

    # create response
    if matched:
        response = 'CORRECT!'
    else:
        response = 'INCORRECT!'
    msg = '>> {}\n>> {}: {}'.format(response, word.upper(), definition)

    return msg


def match_definition(text, word):
    """
    Given a definition and a word, see if the definition matches to the word.

    :param text: a string of text that is the definition
    :param word: (str)
    :return: (bool) true if word matches the definition, false otherwise
    """

    # feed the definition into datamuse api, get response of all matches to definition
    results = datamuse_api.words(ml=text)

    # get all words that match definition
    candidate_words = [result['word'] for result in results]

    if word in candidate_words:
        return True
    else:
        return False


def get_definition(word):
    """
    Given a word, retrieve its definition.

    TODO: currently wordnet gets various definitions of the input word, but returns only the first definition.
    Need to summarize the different (and possibly overlapping) definitions and return the summaries.

    :param word: (str)
    :return: (str) definition of input word
    """

    # get synsets of word from wordnet
    syns = wn.synsets(word)

    if syns:
        # retrieve first definition
        definition = syns[0].definition()
    else:
        definition = 'Please google this word!'
    return definition
