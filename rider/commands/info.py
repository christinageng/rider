import sys
from optparse import Option, BadOptionError

import os
from tabulate import tabulate
from rider.commands.base import Command
from rider.config import KNIGHT_FILE, ROLE,KNIGHT_FILE_SINGLE
from rider.utils import read_dict_fd


headers = ["Role", "Name", "Internal IPAddress", "Port Mapping", "Splunk Authentication", "SSH Authentication","Image Name"]

SEQUENCE = [ROLE["MASTER"], ROLE["LICENSEMASTER"], ROLE["INDEXER"], ROLE["SEARCHHEAD"]]
SEQUENCE_SINGLE = [ROLE["SINGLE"]]


class InfoCommand(Command):
    name = "info"
    usage = """%prog """
    summary = "show info of the current cluster environment"

    def __init__(self):
        super(InfoCommand, self).__init__()

        self.parser.add_option(Option(
            '--env-name',
            dest='env_name',
            action='store',
            default='all',
            help="the rider env: cluster|single|all ,default is all"))


    def run(self, args):

        try:
            options, arg_else = self.parse_args(args)
        except BadOptionError:
            self.logger.error("ERROR: %s" % str(sys.exc_info()[1]))
            return


        if options.env_name not in ('cluster','single','all'):
            self.logger.error("ERROR: %s" % "Bad --env-name value, it should be one of the following: \n cluster|single|all")
            return

        table_data = []

        # read info from cluster env
        if os.path.exists(KNIGHT_FILE) and (options.env_name.lower()=='cluster' or options.env_name.lower()=='all'):
            container_infos = read_dict_fd(os.path.abspath(KNIGHT_FILE))
            for seq_role in SEQUENCE:
                for container in container_infos.get(seq_role, []):
                    table = []
                    table.append(seq_role)
                    table.append(container["name"])
                    table.append(container["internal_ip"])
                    table.append(container["port_mapping"])
                    table.append("admin/notchangeme")
                    table.append("root/password")
                    table.append(container["image_name"])

                    table_data.append(table)



        # read info from single env
        if os.path.exists(KNIGHT_FILE_SINGLE) and (options.env_name.lower()=='single' or options.env_name.lower()=='all'):
            container_infos = read_dict_fd(os.path.abspath(KNIGHT_FILE_SINGLE))
            for seq_role in SEQUENCE_SINGLE:
                for container in container_infos.get(seq_role, []):
                    table = []
                    table.append(seq_role)
                    table.append(container["name"])
                    table.append(container["internal_ip"])
                    table.append(container["port_mapping"])
                    table.append("admin/notchangeme")
                    table.append("root/password")
                    table.append(container["image_name"])

                    table_data.append(table)





        self.logger.info("\n\n" + tabulate(table_data, headers=headers))