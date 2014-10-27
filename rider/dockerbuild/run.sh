#!/bin/bash

/tmp/splunk/bin/splunk edit user admin -password notchangeme --accept-license --answer-yes --no-prompt -auth admin:changeme
/tmp/splunk/bin/splunk start --accept-license --answer-yes --no-prompt

if [[ "$1" == "lm" ]];then
	./cluster/lm.sh
elif [[ "$1" == "master" ]]; then
	./cluster/master.sh
elif [[ "$1" == "indexer" ]]; then
	./cluster/indexer.sh
elif [[ "$1" == "sh" ]]; then
	./cluster/sh.sh
elif [[ "$1" == "dps" ]]; then
	./cluster/dps.sh
elif [[ "$1" == "fwdr" ]]; then
	./cluster/fwdr.sh
fi

if [ ! -f /.root_pw_set ]; then
        /set_root_pw.sh
fi



/tmp/splunk/bin/splunk start && exec /usr/sbin/sshd -D && sh -c "while true;do sleep 10;done"
                                 