import os
from tabulate import tabulate
from rider.commands.base import Command
from rider.config import KNIGHT_FILE, ROLE
from rider.utils import read_dict_fd

headers = ["Role", "Name", "Internal IPAddress", "Port Mapping", "Splunk Authentication", "SSH Authentication","Image Name"]

SEQUENCE = [ROLE["MASTER"], ROLE["LICENSEMASTER"], ROLE["INDEXER"], ROLE["SEARCHHEAD"]]


class InfoCommand(Command):
    name = "info"
    usage = """%prog """
    summary = "show info of the current cluster environment"

    def __init__(self):
        super(InfoCommand, self).__init__()

    def run(self, args):
        if os.path.exists(KNIGHT_FILE):
            table_data = []
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
        else:
            table_data = []

        self.logger.info("\n\n" + tabulate(table_data, headers=headers))