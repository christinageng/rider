#!/bin/bash

$LICENSE_FILE

/tmp/splunk/bin/splunk edit user admin -password notchangeme --accept-license --answer-yes --no-prompt -auth admin:changeme
/tmp/splunk/bin/splunk add licenses $LICENSE_FILE -auth admin:notchangeme
/tmp/splunk/bin/splunk restart
/tmp/splunk/bin/splunk edit licenser-groups Enterprise -is_active 1 -auth admin:notchangeme 
/tmp/splunk/bin/splunk stop -f

echo "finish subtask configuration"
