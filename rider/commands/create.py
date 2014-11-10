import sys
from optparse import Option, BadOptionError
import time

import os
from rider.commands.base import Command
from rider.container import SplunkContainerFactory, check_image_existed
from rider.config import ROLE,KNIGHT_FILE_SINGLE
from rider.utils import write_json_fd, read_dict_fd, write_container_info_to_dict



class CreateCommand(Command):
    name = "provision-single"
    usage = """%prog """
    summary = "provision the single splunk instance according to the parameters"

    def __init__(self):
        super(CreateCommand, self).__init__()

        self.parser.add_option(Option(
            '--single-num',
            dest='single_num',
            action='store',
            default='1',
            help="the single instance number"))


        self.parser.add_option(Option(
            '--image-name',
            dest='image_name',
            action='store',
            default='10.66.128.203:49153/coreqa/splunk:latest',
            help="the image name"
        ))

    def run(self, args):
        try:
            options, arg_else = self.parse_args(args)
        except BadOptionError:
            self.logger.error("ERROR: %s" % str(sys.exc_info()[1]))
            return


        # check the image existed
        if not check_image_existed(image_name=options.image_name):
            self.logger.error(
                "the image not existed , pls use docker pull %s or rider build to build the image" % options.image_name)
            return



           # check the environment existed
        if os.path.exists(os.path.abspath(KNIGHT_FILE_SINGLE)):
            container_infos = read_dict_fd(os.path.abspath(KNIGHT_FILE_SINGLE))
        else:
            container_infos ={}

        scf = SplunkContainerFactory()
        # create indexer
        for i in range(0, int(options.single_num)):
            container_name, container = scf.create_container(image=options.image_name, role=ROLE["SINGLE"],
                                                             command="SINGLE",
            )
            time.sleep(4)  # some work round
            write_container_info_to_dict(container_infos, container)


        write_json_fd(container_infos, os.path.abspath(KNIGHT_FILE_SINGLE))
