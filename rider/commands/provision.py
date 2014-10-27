from rider.commands.base import Command
import rider.utils
from optparse import Option
import time, os


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

    def run(self, args):
        # create cluster master

        options, arg_else = self.parse_args(args)
        dc = rider.utils.docker_client()
        randtimestamp = str(int((time.time())))
        master_name = 'master_' + randtimestamp
        lcmaster_name = "licensemaster_" + randtimestamp

        print "--------Creating Cluster-Master node start--------"

        rid = dc.create_container('coreqa/splunk', command="master", hostname=None, user=None,
                                  detach=False, stdin_open=False, tty=False, mem_limit=0,
                                  ports=None, environment=None, dns=None, volumes=None,
                                  volumes_from=None, network_disabled=False, name=master_name,
                                  entrypoint=None, cpu_shares=None, working_dir=None,
                                  memswap_limit=0)

        dc.start(rid["Id"], publish_all_ports=True)

        print "--------Creating Cluster-Master node finished--------"






        # create license master

        license_path=os.path.dirname(options.license_file)
        license_file_name=os.path.basename(options.license_file)


        print "--------Creating license-Master node start--------"

        rid=dc.create_container('coreqa/splunk', command="lm", hostname=None, user=None,
                                  detach=False, stdin_open=False, tty=False, mem_limit=0,
                                  ports=None, environment=['LICENSE_FILE=/license/'+license_file_name], dns=None, volumes=['/license'],
                                  volumes_from=None, network_disabled=False, name=lcmaster_name,
                                  entrypoint=None, cpu_shares=None, working_dir=None,
                                  memswap_limit=0)

        dc.start(rid["Id"],binds={license_path:
                                 {
                                 'bind': '/license',
                                 'ro': False
                                 }}, publish_all_ports=True)

        print "--------Creating license-Master node finished--------"





        # create cluster indexer


        for i in range(0,int(options.indexer_num)):
            print "--------Creating cluster-indexer  start--------"
            rid=dc.create_container('coreqa/splunk', command="indexer", hostname=None, user=None,
                                      detach=False, stdin_open=False, tty=False, mem_limit=0,
                                      ports=None, environment=None, dns=None, volumes=None,
                                      volumes_from=None, network_disabled=False, name=None,
                                      entrypoint=None, cpu_shares=None, working_dir=None,
                                      memswap_limit=0)

            dc.start(rid["Id"], links=[(lcmaster_name,'licensemaster'),(master_name,'master')],publish_all_ports=True)
            print "--------Creating cluster-indexer node finished--------"





           # create cluster indexer


        for i in range(0,int(options.sh_num)):

            print "--------Creating cluster-search heard start--------"
            rid=dc.create_container('coreqa/splunk', command="sh", hostname=None, user=None,
                                      detach=False, stdin_open=False, tty=False, mem_limit=0,
                                      ports=None, environment=None, dns=None, volumes=None,
                                      volumes_from=None, network_disabled=False, name=None,
                                      entrypoint=None, cpu_shares=None, working_dir=None,
                                      memswap_limit=0)

            dc.start(rid["Id"],links=[(lcmaster_name,'licensemaster'),(master_name,'master')], publish_all_ports=True)
            print "--------Creating cluster-search head finished--------"

        pass