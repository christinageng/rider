import sys
import tempfile
import shutil
from optparse import Option, BadOptionError

import os
from rider.commands.base import Command
from rider.container import DockerClientFactory


class BuildCommand(Command):
    name = "build"
    usage = """%prog """
    summary = "build the image using the new splunk.tar.gz"

    def __init__(self):
        super(BuildCommand, self).__init__()
        self.parser.add_option(Option(
            '--splunk-pkg',
            dest='splunk_pkg',
            action='store',
            default=None,
            help="the splunk.tgz local path"
        ))

        self.parser.add_option(Option(
            '--image-name',
            dest='image_name',
            action='store',
            default="coreqa/splunk:clustering",
            help="the new name of the image"
        ))

        self.docker_client = DockerClientFactory.get_docker_client()

    def run(self, args):
        try:
            options, arg_else = self.parse_args(args)
        except BadOptionError:
            self.logger.error("ERROR: %s" % str(sys.exc_info()[1]))
            sys.exit(1)

        try:
            temp_build_path = tempfile.mkdtemp()
            temp_dockerbuild_path = os.path.join(temp_build_path, "dockerbuild")
            docker_build_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dockerbuild"))

            # prepare the build environment
            shutil.copytree(os.path.join(docker_build_path), os.path.join(temp_build_path, "dockerbuild"))
            shutil.copyfile(options.splunk_pkg, os.path.join(temp_build_path, "dockerbuild", "splunk.tgz"))

            # build the image
            yield_result = self.docker_client.build(path=temp_dockerbuild_path, tag="mark/splunk",
                                                    stream=True, rm=True)
            for result in yield_result:
                if not len(result) == 0:
                    self.logger.info(result[:-1])
            print 11
        finally:
            pass
