#!/bin/bash


echo $MASTER_PORT_8089_TCP_ADDR
echo $LM_PORT_8089_TCP_ADDR

/tmp/splunk/bin/splunk edit cluster-config -mode searchhead -secret secret12  -master_uri https://$MASTER_PORT_8089_TCP_ADDR:8089 -replication_port 9011 -auth admin:notchangeme
/tmp/splunk/bin/splunk edit licenser-localslave -master_uri https://$LM_PORT_8089_TCP_ADDR:8089 -auth admin:notchangeme
/tmp/splunk/bin/splunk stop -f  