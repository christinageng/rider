#!/usr/bin/python
# coding:utf8

'''
@author: shaoyuliang
@contact: mshao@splunk.com
@since: 7/16/14

'''

import sys
from optparse import BadOptionError

import os


def create_main_parser():
    pass


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