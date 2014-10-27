import copy
from optparse import OptionGroup, Option


def make_option_group(group, parser):
    """
    Return an OptionGroup object
    group  -- assumed to be dict with 'name' and 'options' keys
    parser -- an optparse Parser
    """
    option_group = OptionGroup(parser, group['name'])
    for option in group['options']:
        option_group.add_option(option.make())
    return option_group


class OptionMaker(object):
    """Class that stores the args/kwargs that would be used to make an Option,
    for making them later, and uses deepcopy's to reset state."""

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def make(self):
        args_copy = copy.deepcopy(self.args)
        kwargs_copy = copy.deepcopy(self.kwargs)
        return Option(*args_copy, **kwargs_copy)