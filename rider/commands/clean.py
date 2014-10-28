import os
from rider.commands.base import Command
from rider.config import KNIGHT_FILE
from rider.utils import read_dict_fd
from rider.container import DockerClientFactory


class CleanCommand(Command):
    name = "clean"
    usage = """%prog """
    summary = "clean the current cluster environment"

    def __init__(self):
        super(CleanCommand, self).__init__()
        self.docker_client = DockerClientFactory.get_docker_client()

    def run(self, args):
        if os.path.exists(KNIGHT_FILE):
            container_infos = read_dict_fd(os.path.abspath(KNIGHT_FILE))
            can_delete = True
            for key in container_infos.keys():
                for container in container_infos[key]:
                    try:
                        self.docker_client.stop(container["cid"], timeout=5 * 60)
                        self.docker_client.remove_container(container["cid"], v=True, force=True)
                        self.logger.error("successfully to remove the container [%s]" % container["name"])
                    except:
                        self.logger.error("fail to remove the container [%s]" % container["name"])
                        can_delete = False

            if can_delete:
                os.remove(os.path.abspath(KNIGHT_FILE))
