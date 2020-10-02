""" Entrypoint of vocabtester """
from .progress import load_vocab_sets_data
from .commands import Shell

if __name__ == '__main__':
    """ parse args and run cmd shell """

    load_vocab_sets_data()
    Shell().cmdloop()
