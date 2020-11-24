
"""Usage: twitchfacelib <command> [<args>...]

Commands:
  record  Record live twitch streams with faces.
"""

from docopt import docopt
def main(argv=None):
    args = docopt(__doc__, argv=argv, options_first=True)

    argv = [args['<command>']] + args['<args>']

    if args['<command>'] == 'record':
        from .record import main as record_main
        record_main()

    if args['<command>'] == 'test':
        from .test import main as test_main
        test_main()


if __name__ == '__main__':
    main()
