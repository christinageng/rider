import os
from rider.commands.base import Command
from rider.config import KNIGHT_FILE, KNIGHT_FILE_SINGLE
from rider.utils import read_dict_fd
from rider.container import DockerClientFactory
from optparse import Option, BadOptionError
import sys



class CleanCommand(Command):
    name = "clean"
    usage = """%prog """
    summary = "clean the current cluster environment"

    def __init__(self):
        super(CleanCommand, self).__init__()
        self.docker_client = DockerClientFactory.get_docker_client()
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
            self.logger.error("ERROR: %s" % "Bad --env-name value, it should be one of the following: \n  cluster|single|all")
            return

        # clean cluster env
        if os.path.exists(KNIGHT_FILE) and (options.env_name.lower()=="cluster" or options.env_name.lower()=="all"):
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

        # clean single env
        if os.path.exists(KNIGHT_FILE_SINGLE) and (options.env_name.lower()=="single" or options.env_name.lower()=="all"):
            container_infos = read_dict_fd(os.path.abspath(KNIGHT_FILE_SINGLE))
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
                os.remove(os.path.abspath(KNIGHT_FILE_SINGLE))