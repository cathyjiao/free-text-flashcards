"""
Command interpreter for vocabtion.

Author: Cathy Jiao
"""

import cmd
from vocabtion import progress as prog
from vocabtion.question import question_user


class Shell(cmd.Cmd):
    """
    Command interpreter class for vocabtion.

    See https://docs.python.org/3/library/cmd.html.
    """

    intro = '>> MAIN MENU\n>> Welcome! Type help or ? to list commands.'
    prompt = '>> '

    def do_test(self, arg):
        """
        Begin testing on a test set: 'test gre'.

        :param arg: (str) name of test set
        """

        # return if no test set name is provided
        if not arg:
            print('No test set selected. Please select or add a test set')
            return

        # load progress for selected test set
        prog.load(arg)
        _print_start_msg()

        # start test
        while question_user():
            continue

        # save progress and exit
        prog.save()
        prog.clear()
        _print_exit_msg()

    def do_delete(self, arg):
        """
        Deletes test sets: e.g. 'delete gre' or 'delete all' to delete all sets.

        :param arg: (optional) (str) 'all'
        """

        prompt_all = '>> Delete all vocab sets? [y/n]'
        prompt_file = '>> Delete: {}? [y/n]'.format(arg)
        msg_unchanged = '>> Nothing happened.'
        msg_err = '>> Please select [y/n]'
        msg_del_all = '>> All vocab sets deleted!'
        msg_del_file = '>> Deleted: {}'.format(arg)

        if arg == 'all':
            _prompt_yes_no(prompt_all, prog.delete_all_vocab_sets, None, msg_err, pos_msg=msg_del_all,
                           neg_msg=msg_unchanged)
        else:
            _prompt_yes_no(prompt_file, prog.delete_vocab_set, None, msg_err, pos_msg=msg_del_file, pos_args=arg,
                           neg_msg=msg_unchanged)

    def do_clear(self, arg):
        """
        Clears progress of test sets: e.g. 'clear gre' or 'clear all' to clear progress from all sets.

        :param arg: (optional) (str) 'all'
        """

        prompt_all = '>> Clear all progress? [y/n]'
        prompt_file = '>> Clear progress for: {}? [y/n]'.format(arg)
        msg_unchanged = '>> Progress unchanged.'
        msg_err = '>> Please select [y/n]'
        msg_del_all = '>> All progress cleared!'
        msg_del_file = '>> Cleared progress for: {}'.format(arg)

        if arg == 'all':
            _prompt_yes_no(prompt_all, prog.clear_all_progress, None, msg_err, pos_msg=msg_del_all,
                           neg_msg=msg_unchanged)
        else:
            _prompt_yes_no(prompt_file, prog.clear_progress, None, msg_err, pos_msg=msg_del_file, pos_args=arg,
                           neg_msg=msg_unchanged)

    def do_progress(self, arg):
        """
        Display progress for all vocab sets or display progress for a specific set: 'progress gre'.

        :param arg: (str) name of vocab set to test
        """

        if not arg:
            prog.print_overall_progress()
        else:
            prog.print_progress(arg, True)

    def do_add(self, arg):
        """
        Add a new vocab set: 'vocab path_to_vocab_set'.

        :param arg: (str) path of vocab file to add
        """

        # ask user to give name to vocab set and add set
        print('>> Please enter a name for this vocab set')
        resp = input('>> ')
        prog.add_vocab(resp, arg)
        print('>> Vocab set \'{}\' added!'.format(resp))

        # ask user if they want to begin practicing on newly added set
        msg = '>> Begin practicing on \'{}\'? [y/n]'.format(resp)
        msg_unchanged = '>> Back at main menu'
        msg_err = '>> Please select [y/n]'
        _prompt_yes_no(msg, self.do_test, None, msg_err, pos_args=resp, neg_msg=msg_unchanged)

    def do_exit(self, arg):
        """
        Closes the program.
        """

        print('>> Goodbye!')
        return True


def _print_start_msg():
    """
    Message to print before starting a test.
    """

    print('>> Testing vocab from: {}'.format(prog.vocab_name))
    print('>> Type \'exit\' to go back to main menu')
    print('>>')


def _print_exit_msg():
    """
    Message to print upon finishing a test.
    """
    print('>> Saved progress for: {}'.format(prog.vocab_name))
    print('>> Back to main menu.')


def _prompt_yes_no(prompt_msg, pos_function, neg_function, err_msg, pos_args=None, neg_args=None,
                   pos_msg=None,
                   neg_msg=None):
    """
    Yes or no prompt for user.

    :param prompt_msg: (str) a y/n prompt message
    :param pos_function: (func pointer) function to carry out if user replies with 'yes'
    :param neg_function: (func pointer) function to carry out if user replies with 'no'
    :param err_msg: (str) message to print if user enters anything but yes or no
    :param pos_args: (optional) (any) args for pos function
    :param neg_args: (optionak) (any) args for negative function
    :param pos_msg: (optional) (str) message to print upon completing pos function
    :param neg_msg: (optional) (str) message to print upon completing neg function
    """

    # prompt user and read response
    print(prompt_msg)
    response = input('>> ')

    positive_answers = ['y', 'yes']
    negative_answers = ['n', 'no']

    # process user answer
    if response in positive_answers:
        # run the pos function
        if pos_function:
            if pos_args:
                pos_function(pos_args)
            else:
                pos_function()

        # print pos message
        if pos_msg:
            print(pos_msg)

    elif response in negative_answers:
        # run the neg function
        if neg_function:
            if neg_args:
                neg_function(neg_args)
            else:
                neg_function()

        # print neg message
        if neg_msg:
            print(neg_msg)
    else:
        # user response is not a valid answer
        print(err_msg)
