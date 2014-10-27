from optparse import Option

from rider.commands.base import Command


class BuildCommand(Command):
    name = "build"
    usage = """%prog """
    summary = "build the image using the new splunk.tar.gz"

    def __init__(self):
        super(BuildCommand, self).__init__()
        self.parser.add_option(Option(
            '--splunk-tar',
            dest='splunk_pkg',
            action='store',
            default=None,
            help="the splunk.tar.gz local path"
        ))

        self.parser.add_option(Option(
            '--image-name',
            dest='image_name',
            action='store',
            default="coreqa/splunk:clustering",
            help="the new name of the image"
        ))


    def run(self, args):
        options, arg_else = self.parse_args(args)