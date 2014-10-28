import sys
from optparse import Option, BadOptionError

import os
from rider.commands.base import Command
from rider.container import SplunkContainerFactory


ROLE = {
    "MASTER": "master",
    "LICENSEMASTER": "licensemaster",
    "INDEXER": "indexer",
    "SEARCHHEAD": "sh"
}


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
            default='3',
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
            default='10.66.128.203:49153/coreqa/splunk:clustering',
            help="the image name"
        ))

    def run(self, args):
        try:
            options, arg_else = self.parse_args(args)
        except BadOptionError:
            self.logger.error("ERROR: %s" % str(sys.exc_info()[1]))
            sys.exit(1)

        scf = SplunkContainerFactory()

        # create master node
        master_name, container = scf.create_container(image=options.image_name, role=ROLE["MASTER"],
                                                      command="master")

        # create license master node
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
        # create indexer
        for i in range(0, int(options.indexer_num)):
            container_name, container = scf.create_container(image=options.image_name, role=ROLE["INDEXER"],
                                                             command="indexer",
                                                             links=[(license_master_name, 'licensemaster'),
                                                                    (master_name, 'master')]
            )

        # create search head
        for i in range(0, int(options.sh_num)):
            container_name, container = scf.create_container(image=options.image_name, role=ROLE["SEARCHHEAD"],
                                                             command="sh",
                                                             links=[(license_master_name, 'licensemaster'),
                                                                    (master_name, 'master')]
            )