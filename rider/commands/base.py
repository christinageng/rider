import sys
import optparse

from rider import cmdoptions
from rider.cmdparser import ConfigOptionParser, UpdatingDefaultsHelpFormatter
from rider.utils import get_prog
from rider.log import logger


class Command(object):
    name = None
    usage = None
    hidden = None
    summary = ""

    def __init__(self):
        parser_kw = {
            'usage': self.usage,
            'prog': '%s %s' % (get_prog(), self.name),
            'formatter': UpdatingDefaultsHelpFormatter(),
            'add_help_option': False,
            'name': self.name,
            'description': self.__doc__,
        }

        self.parser = ConfigOptionParser(**parser_kw)

        # Commands should add options to this option group
        optgroup_name = '%s Options' % self.name.capitalize()
        self.cmd_opts = optparse.OptionGroup(self.parser, optgroup_name)

        # Add the general options
        gen_opts = cmdoptions.make_option_group(cmdoptions.general_group, self.parser)
        self.parser.add_option_group(gen_opts)

        # set logger
        self.logger = logger

    def setup_logging(self):
        pass

    def parse_args(self, args):
        # factored out for testability
        return self.parser.parse_args(args)

    def run(self, args):
        """
            The sub command class should overide this method
        """
        NotImplemented

    def execute(self, args=None):
        """
            The main interface for exectute the command
        """

        try:
            self.run(args)
        except Exception, e:
            print e
            sys.exit(1)
        except KeyboardInterrupt:
            sys.exit(1)