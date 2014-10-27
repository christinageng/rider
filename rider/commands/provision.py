import sys
import time
from optparse import Option, BadOptionError

import os
from rider.commands.base import Command
from rider.docker import docker_client


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
            default=None,
            help="the cluster indexer number"))

        self.parser.add_option(Option(
            '--sh-num',
            dest='sh_num',
            action='store',
            default=None,
            help="the cluster sh number"
        ))

        self.parser.add_option(Option(
            '--image-name',
            dest='image-name',
            action='10.66.128.203:49154/coreqa/splunk:clustering',
            default=None,
            help="the cluster sh number"
        ))

    def run(self, args):
        try:
            options, arg_else = self.parse_args(args)
        except BadOptionError:
            self.logger.error("ERROR: %s" % str(sys.exc_info()[1]))
            sys.exit(1)

        dc = docker_client()
        rand_timestamp = str(int((time.time())))
        master_name = 'master_' + rand_timestamp
        lc_master_name = "licensemaster_" + rand_timestamp

        self.logger.info("Creating Cluster-Master node start")

        rid = dc.create_container('coreqa/splunk', command="master", hostname=None, user=None,
                                  detach=False, stdin_open=False, tty=False, mem_limit=0,
                                  ports=None, environment=None, dns=None, volumes=None,
                                  volumes_from=None, network_disabled=False, name=master_name,
                                  entrypoint=None, cpu_shares=None, working_dir=None,
                                  memswap_limit=0)

        dc.start(rid["Id"], publish_all_ports=True)
        self.logger.info("Creating Cluster-Master node finished")

        # create license master
        license_path = os.path.dirname(options.license_file)
        license_file_name = os.path.basename(options.license_file)

        self.logger.info("Creating license-Master node start")

        rid = dc.create_container('coreqa/splunk', command="lm", hostname=None, user=None,
                                  detach=False, stdin_open=False, tty=False, mem_limit=0,
                                  ports=None, environment=['LICENSE_FILE=/license/' + license_file_name], dns=None,
                                  volumes=['/license'],
                                  volumes_from=None, network_disabled=False, name=lc_master_name,
                                  entrypoint=None, cpu_shares=None, working_dir=None,
                                  memswap_limit=0)

        dc.start(rid["Id"], binds={license_path:
                                       {
                                           'bind': '/license',
                                           'ro': False
                                       }}, publish_all_ports=True)
        self.logger.info("Creating license-Master node finish")

        # create cluster indexer

        for i in range(0, int(options.indexer_num)):
            self.logger.info("Creating cluster-indexer start")
            rid = dc.create_container('coreqa/splunk', command="indexer", hostname=None, user=None,
                                      detach=False, stdin_open=False, tty=False, mem_limit=0,
                                      ports=None, environment=None, dns=None, volumes=None,
                                      volumes_from=None, network_disabled=False, name=None,
                                      entrypoint=None, cpu_shares=None, working_dir=None,
                                      memswap_limit=0)

            dc.start(rid["Id"], links=[(lc_master_name, 'licensemaster'), (master_name, 'master')],
                     publish_all_ports=True)
            self.logger.info("Creating cluster-indexer finish")

        # create search head
        for i in range(0, int(options.sh_num)):
            self.logger.info("Creating cluster-search heard start")
            rid = dc.create_container('coreqa/splunk', command="sh", hostname=None, user=None,
                                      detach=False, stdin_open=False, tty=False, mem_limit=0,
                                      ports=None, environment=None, dns=None, volumes=None,
                                      volumes_from=None, network_disabled=False, name=None,
                                      entrypoint=None, cpu_shares=None, working_dir=None,
                                      memswap_limit=0)

            dc.start(rid["Id"], links=[(lc_master_name, 'licensemaster'), (master_name, 'master')],
                     publish_all_ports=True)
            self.logger.info("Creating cluster-search heard finish")