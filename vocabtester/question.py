"""
Generate questions to ask user.

Author: Cathy Jiao
"""

from vocabtion import progress as prog
from vocabtion.lookup import lookup
import random


def question_user():
    """
    Asks user to define a word.

    Return a bool: false if user wishes to quit being asked questions, true otherwise
    """

    # choose a word to test user
    word = choose_word()

    # get category of chosen word
    category_code = prog.word_to_progress[word][0]
    category = decode_word_category(category_code)

    # ask user to define word and read user response
    print('>> {} ({})'.format(word.upper(), category))
    text = input('>> definition: ')

    if text == 'e':
        # user wants to exit
        return False
    else:
        # give user feedback on their answer
        feedback = lookup(text, word)
        print(feedback)
        print('>>')
        return True


def decode_word_category(code):
    """
    Given an integer, map it to its corresponding category
    :param code: (int) 0-3
    :return: (str) category
    """

    mapping = {0: 'new', 1: 'learning', 2: 'reviewing', 3: 'mastered'}
    return mapping[code]


def choose_word(weights=[0.2, 0.35, 0.35, 0.1]):
    """
    Choose a word to test the user.

    Word chosen will be from one of these four categories:
    - new: a word user has not encountered before
    - learning: a word the user has defined (correctly or incorrectly) to a least once
    - reviewing: a word a user has defined correctly 3 consecutive times
    - mastered: a word a user has defined correctly 6 consecutive times

    :param weights: (list) a list of 4 integers representing the proportion of words to be chosen from each category.
    The sum of all integers in the list must be equal to 1.
    """

    # all words partitioned into their categories
    vocab_lists = [prog.vocab_new, prog.vocab_learning, prog.vocab_reviewing, prog.vocab_mastered]

    # re-weigh the weights (ignore vocab lists that are empty)
    weights = [w if len(vocab_lists[i]) > 0 else 0 for i, w in enumerate(weights)]
    weights = [float(i) / sum(weights) for i in weights]

    # choose a word category
    choice = random.choices(range(4), weights)[0]

    # choose a word from the chosen category
    if choice == 0:
        word = random.choice(prog.vocab_new)
    elif choice == 1:
        word = random.choice(prog.vocab_learning)
    elif choice == 2:
        word = random.choice(prog.vocab_reviewing)
    else:
        word = random.choice(prog.vocab_mastered)

    return word
