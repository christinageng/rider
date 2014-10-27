from rider.commands.base import Command
import rider.utils
from optparse import Option
import time


class ProvisionCommand(Command):
    name = "provision"
    usage = """%prog """
    summary = "provision the cluster environment according to the parameters"

    def __init__(self):
        super(ProvisionCommand, self).__init__()
        self.parser.add_option(Option(
            '--splunk-tar',
            dest='splunk_pkg',
            action='store',
            default=None,
            help="the splunk.tar.gz local path"
        ))

    def run(self, args):
        # create cluster master

        randtimestamp = str(int((time.time())))
        mastername = 'master_' + randtimestamp
        lcmastername = "licensemaster_" + randtimestamp

        print "--------Creating Cluster-Master node start--------"
        dc = rider.utils.docker_client()
        rid = dc.create_container('coreqa/splunk', command="master", hostname=None, user=None,
                                  detach=False, stdin_open=False, tty=False, mem_limit=0,
                                  ports=None, environment=None, dns=None, volumes=None,
                                  volumes_from=None, network_disabled=False, name=mastername,
                                  entrypoint=None, cpu_shares=None, working_dir=None,
                                  memswap_limit=0)

        dc.start(rid["Id"], publish_all_ports=True)

        print "--------Creating Cluster-Master node finished--------"



        # create license master






        pass