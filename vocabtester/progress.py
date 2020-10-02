"""
Handle user progress for vocab sets.

Author: Cathy Jiao
"""

import json
import pprint
from os.path import dirname, abspath, join
from os import remove

# TODO: many globals, probably not best coding practice, consider wrapping in a class
# globals
PARENT_DIR = dirname(abspath(__file__))
PROGRESS_DIR = join(PARENT_DIR, 'data')
VOCAB_SETS_JSON_FILENAME = 'vocab_sets.json'
VOCAB_SETS_PATH = join(PROGRESS_DIR, VOCAB_SETS_JSON_FILENAME)

vocab_name_to_progress_file = {}
progress_file_to_vocab_name = {}
word_to_progress = {}
vocab_name = ''
vocab_new = []
vocab_learning = []
vocab_reviewing = []
vocab_mastered = []

# prints out things nicely
pp = pprint.PrettyPrinter(indent=4)


def clear():
    """
    Clear all global variables
    """
    global vocab_name
    global word_to_progress
    global vocab_new
    global vocab_learning
    global vocab_reviewing
    global vocab_mastered

    vocab_name = ''
    word_to_progress = {}
    vocab_new = []
    vocab_learning = []
    vocab_reviewing = []
    vocab_mastered = []


def load_vocab_sets_data():
    """
    Load vocab sets info
    """

    global vocab_name_to_progress_file
    global progress_file_to_vocab_name
    with open(VOCAB_SETS_PATH, 'r') as file:
        vocab_name_to_progress_file = json.load(file)
        progress_file_to_vocab_name = {value: key for key, value in vocab_name_to_progress_file.items()}


def add_vocab(name, path):
    """
    Add a vocab set.

    :param name: (str) name of vocab set
    :param path: (str) path of file containing vocab words
    """

    global vocab_name_to_progress_file
    global vocab_name

    if name in vocab_name_to_progress_file:
        print('>> A set with name \'{}\' already exists. Please choose a different name'.format(name))
        return

    _vocab = read_words(path)
    if not _vocab:
        return

    # create a progress json file for new vocab set
    _word_to_progress = {word: [0, 0] for word in _vocab}
    progress_file_path = join(PROGRESS_DIR, '{}.json'.format(name))
    save_progress(progress_file_path, _word_to_progress)

    # save vocab set data
    vocab_name_to_progress_file[name] = progress_file_path
    save_vocab_sets_data(vocab_name_to_progress_file)


def read_words(path):
    """
    Read words from a text file

    :param path: (str) path of file to read
    :return: list of words or None if file does not exist
    """

    try:
        with open(path, 'r') as file:
            lines = file.readlines()
        _vocab = [l.strip().lower() for l in lines]
        return _vocab
    except FileNotFoundError:
        print('File does not exist: {}'.format(path))
        return None


def save():
    """
    Save all current progress.
    """

    progress_path = vocab_name_to_progress_file[vocab_name]
    save_progress(progress_path, word_to_progress)
    save_vocab_sets_data(vocab_name_to_progress_file)


def save_progress(path, _word_to_progress):
    """
    Save progress of current loaded vocab set.

    :param path: (str) path to save progress to
    :param _word_to_progress: (json)
    """

    with open(path, 'w+') as file:
        json.dump(_word_to_progress, file, indent=4)


def save_vocab_sets_data(_vocab_name_to_progress_file):
    """
    Save vocab set info.

    :param _vocab_name_to_progress_file: (str) file to save to
    """

    with open(VOCAB_SETS_PATH, 'w+') as file:
        json.dump(_vocab_name_to_progress_file, file, indent=4)


def load(name):
    """
    Load a vocab set.

    :param name: (str) name of vocab set to load
    """

    # vocab set does not exist
    if name not in vocab_name_to_progress_file:
        print('{} is not a vocab set'.format(name))
        return

    global vocab_name
    vocab_name = name

    # path of vocab file
    path = vocab_name_to_progress_file[name]

    # load progress file
    global word_to_progress
    word_to_progress = load_progress_json(path)

    if not word_to_progress:
        print('>> Progress file not found! Please re-add the vocab set')

    # load the vocab words relative to their categories
    global vocab_learning
    global vocab_reviewing
    global vocab_mastered
    global vocab_new
    vocab_learning, vocab_reviewing, vocab_mastered, vocab_new = load_vocab_categories(word_to_progress)


def load_progress_json(path):
    """
    Load a json file containing the progress of a vocab set.

    :param path: (str) path of the progress file
    :return: progress json or None if file is not found
    """

    # full path of file
    try:
        with open(path, 'r') as file:
            progress_json = json.load(file)
        return progress_json
    except FileNotFoundError:
        return None


def load_vocab_categories(vocab_json):
    """
    Load vocab words into categories.

    :param vocab_json: (json) all vocab words and related info
    :return: (list) four lists of vocab words
    """

    new = [word for word, info in vocab_json.items() if info[0] == 0]
    learning = [word for word, info in vocab_json.items() if info[0] == 1]
    reviewing = [word for word, info in vocab_json.items() if info[0] == 2]
    mastered = [word for word, info in vocab_json.items() if info[0] == 3]

    return learning, reviewing, mastered, new


def print_overall_progress():
    """
    Print progress of vocab sets.
    """

    names = list(vocab_name_to_progress_file.keys())
    if not names:
        print('>> No vocab sets detected!')
        return

    for name in names:
        print_progress(name)


def print_progress(name, verbose=False):
    """
    Print progress of a vocab set.

    :param name: (str) name of vocab set
    :param verbose: (bool) true or false for verbose printing
    :return:
    """

    # Load progress json
    path = vocab_name_to_progress_file[name]
    vocab_progress_json = load_progress_json(path)

    print('Progress for: {}'.format(name))

    # Print progress for each category
    learning, reviewing, mastered, new = load_vocab_categories(vocab_progress_json)
    category_to_vocab = {'new': new, 'learning': learning, 'reviewing': reviewing, 'mastered': mastered}
    for category, category_vocab in category_to_vocab.items():
        print('{}: {}/{} words'.format(category, len(category_vocab), len(vocab_progress_json)))
        if verbose:
            pp.pprint(category_vocab)
            print()
    print()


def delete_all_vocab_sets():
    """
    Delete all vocab sets
    """

    # clear globals
    global vocab_name_to_progress_file
    global progress_file_to_vocab_name
    global word_to_progress
    clear()
    save_vocab_sets_data({})

    # delete all progress files
    for name in vocab_name_to_progress_file:
        remove(vocab_name_to_progress_file[name])

    vocab_name_to_progress_file = {}
    progress_file_to_vocab_name = {}


def delete_vocab_set(name):
    """
    Deletes vocab set.
    :param name: (str) name of vocab set
    """

    path = vocab_name_to_progress_file[name]
    del vocab_name_to_progress_file[name]
    del progress_file_to_vocab_name[path]
    save_vocab_sets_data(vocab_name_to_progress_file)
    remove(path)


def clear_all_progress():
    """
    Clear all progress.
    """

    for name in vocab_name_to_progress_file:
        clear_progress(name)


def clear_progress(name):
    """
    Clear progress for a specific vocab set.

    :param name: (str) name of vocab set
    """

    path = vocab_name_to_progress_file[name]
    _word_to_progress = load_progress_json(path)
    _word_to_progress = {key: [0, 0] for key in _word_to_progress.keys()}
    save_progress(path, _word_to_progress)


def update_progress(word, flag, threshold=3):
    """
    Update progress of a word.

    :param word: (str) word to update
    :param flag: (bool) if user got word definition correct
    :param threshold: (int) number of consecutive times user must get word definition correct to go to next level
    """

    # get current word progress
    word_info = word_to_progress[word]
    # type of word - new, learning, reviewing or mastered
    category = word_info[0]
    # number of consecutive times user got word definition correct at current level
    consecutive = word_info[1]

    if category == 0:
        # word was a new word
        if flag:
            # automatically considered as "mastered" if user correctly defined new word
            category = 3
        else:
            category = 1
        consecutive = 0
    else:
        # word was not a new word
        if flag:
            # user got word definition correct
            consecutive += 1

            # increase category if they got word correct some consecutive amount of times
            if consecutive >= threshold and category <= 3:
                consecutive = 0
                category = category + 1
        else:
            # user defined word incorrectly, move down a category
            if category > 1:
                category = category - 1
                consecutive = 0

    # reload the word categories
    word_to_progress[word] = [category, consecutive]
    load_vocab_categories(word_to_progress)
