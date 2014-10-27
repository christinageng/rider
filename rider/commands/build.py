import sys
import tempfile
import shutil
from optparse import Option, BadOptionError

import os
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
        try:
            options, arg_else = self.parse_args(args)
        except BadOptionError:
            sys.exit(1)

        temp_build_path = tempfile.mkdtemp()
        dockerbuild_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dockerbuild"))

        print dockerbuild_path
        print temp_build_path

        shutil.copytree(os.path.join(dockerbuild_path, "cluster"), os.path.join(temp_build_path, "cluster"))
