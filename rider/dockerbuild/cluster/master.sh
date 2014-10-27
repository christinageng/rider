  #!/bin/bash

/tmp/splunk/bin/splunk edit cluster-config -mode master -secret secret12 -auth admin:notchangeme
/tmp/splunk/bin/splunk stop -f  