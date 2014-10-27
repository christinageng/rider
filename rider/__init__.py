import sys
from optparse import OptionParser, BadOptionError

import os
from rider import commands


def create_main_parser():
    parser = OptionParser()


def parse_opts(args):
    return cmd_name, cmd_args


def main():
    """
        main function
    """

    args = sys.argv[1:]
    try:
        cmd_name, cmd_args = parse_opts(args)
    except BadOptionError, e:
        sys.stderr.write(str(e))
        sys.stderr.write(os.linesep)
        sys.exit(1)

    command = commands[cmd_name]()
    command.execute(cmd_args)


# ########################
# #### just for test  ####
# ########################

if __name__ == "__main__":
    main()