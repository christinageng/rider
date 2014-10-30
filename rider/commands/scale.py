import sys
import time
from optparse import Option, BadOptionError

import os
from rider.container import SplunkContainerFactory
from rider.commands.base import Command
from rider.config import ROLE, KNIGHT_FILE
from rider.utils import write_json_fd, read_dict_fd, write_container_info_to_dict


class ScaleCommand(Command):
    name = "scale"
    usage = """%prog """
    summary = "scale out the indexer and search head according to the current envrionment"

    def __init__(self):
        super(ScaleCommand, self).__init__()

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
        if not os.path.exists(os.path.abspath(KNIGHT_FILE)):
            self.logger.error(
                "There maybe hasn't a environment here currently , please provision first then scale")
            return

        container_infos = read_dict_fd(os.path.abspath(KNIGHT_FILE))

        # if the KeyError happend , there maybe a problem in the previous environment
        master_name = container_infos[ROLE["MASTER"]][0]["name"]
        license_master = container_infos.get(ROLE["LICENSEMASTER"], None)
        license_master_name = license_master[0]["name"] if license_master else None

        links = [(master_name, 'master')] if not license_master_name else [(license_master_name, 'lm'),
                                                                           (master_name, 'master')]

        current_indexer_number = len(container_infos.get(ROLE["INDEXER"], []))
        if current_indexer_number >= int(options.indexer_num):
            self.logger.info("current indexer num [%s] is bigger/equal than the target" % current_indexer_number)
        else:
            scf = SplunkContainerFactory()
            self.logger.error("scale indexer from %s -> %s" % (current_indexer_number, options.indexer_num))
            for i in range(int(options.indexer_num) - current_indexer_number):
                container_name, container = scf.create_container(image=options.image_name, role=ROLE["INDEXER"],
                                                                 command="indexer",
                                                                 links=links)
                time.sleep(4)  # some work round
                write_container_info_to_dict(container_infos, container)

        current_sh_number = len(container_infos.get(ROLE["SEARCHHEAD"], []))
        if current_sh_number >= int(options.sh_num):
            self.logger.info("current search head num [%s] is bigger/equal than the target" % current_sh_number)
        else:
            scf = SplunkContainerFactory()
            self.logger.error("scale search head from %s -> %s" % (current_sh_number, options.sh_num))
            for i in range(int(options.sh_num) - current_sh_number):
                container_name, container = scf.create_container(image=options.image_name, role=ROLE["SEARCHHEAD"],
                                                                 command="sh",
                                                                 links=links)
                time.sleep(4)
                write_container_info_to_dict(container_infos, container)

        write_json_fd(container_infos, os.path.abspath(KNIGHT_FILE))

