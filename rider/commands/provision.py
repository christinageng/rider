import sys
from optparse import Option, BadOptionError
import time

import os
from rider.commands.base import Command
from rider.container import SplunkContainerFactory, check_image_existed
from rider.config import ROLE, KNIGHT_FILE
from rider.utils import write_json_fd, write_container_info_to_dict


class ProvisionCommand(Command):
    name = "provision"
    usage = """%prog """
    summary = "provision the cluster environment according to the parameters"

    def __init__(self):
        super(ProvisionCommand, self).__init__()
        self.parser.add_option(Option(
            '--license-file',
            dest='license_file',
            action='store',
            default=None,
            help="the splunk license local path"))

        self.parser.add_option(Option(
            '--indexer-num',
            dest='indexer_num',
            action='store',
            default='2',
            help="the cluster indexer number"))

        self.parser.add_option(Option(
            '--sh-num',
            dest='sh_num',
            action='store',
            default='1',
            help="the cluster sh number"
        ))

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

        # check the environment existed
        if os.path.exists(os.path.abspath(KNIGHT_FILE)):
            self.logger.error(
                "There maybe an environment here currently , please remove the environment first \n"
                "or you can create the cluster in another folder")
            return

        # check the image existed
        if not check_image_existed(image_name=options.image_name):
            self.logger.error(
                "the image not existed , pls use docker pull %s or rider build to build the image" % options.image_name)
            return

        scf = SplunkContainerFactory()
        cluster_info = {}
        # create master node
        master_name, container = scf.create_container(image=options.image_name, role=ROLE["MASTER"],
                                                      command="master")
        write_container_info_to_dict(cluster_info, container)
        # create license master node only when specify the license file
        if options.license_file:
            license_path = os.path.dirname(options.license_file)
            license_file_name = os.path.basename(options.license_file)
            license_master_name, container = scf.create_container(image=options.image_name, role=ROLE["LICENSEMASTER"],
                                                                  command="lm",
                                                                  environment=[
                                                                      'LICENSE_FILE=/license/' + license_file_name],
                                                                  binds={license_path:
                                                                             {
                                                                                 'bind': '/license',
                                                                                 'ro': False}})
            time.sleep(8)  # some work round
            write_container_info_to_dict(cluster_info, container)

        # decide the links if the license_master is not existed
        links = [(master_name, 'master')] if not options.license_file else [(license_master_name, 'lm'),
                                                                            (master_name, 'master')]
        # create indexer
        for i in range(0, int(options.indexer_num)):
            container_name, container = scf.create_container(image=options.image_name, role=ROLE["INDEXER"],
                                                             command="indexer",
                                                             links=links
            )
            time.sleep(4)  # some work round
            write_container_info_to_dict(cluster_info, container)

        # create search head
        for i in range(0, int(options.sh_num)):
            container_name, container = scf.create_container(image=options.image_name, role=ROLE["SEARCHHEAD"],
                                                             command="sh",
                                                             links=links)
            time.sleep(4)  # some work round
            write_container_info_to_dict(cluster_info, container)

        write_json_fd(cluster_info, os.path.abspath(KNIGHT_FILE))
