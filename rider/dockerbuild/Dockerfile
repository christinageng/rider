FROM tutum/ubuntu
COPY splunk.tgz /tmp/splunk.tgz
WORKDIR /tmp
RUN tar zxvf splunk.tgz
VOLUME /splunkdb
RUN echo "SPLUNK_DB = /splunkdb" >> splunk/etc/splunk-launch.conf.default
COPY run.sh /tmp/run.sh
ADD cluster /tmp/cluster
ADD set_root_pw.sh /tmp/set_root_pw.sh
RUN chmod +x /tmp/cluster/*
RUN chmod +x /tmp/run.sh
RUN ls -al /tmp
RUN ls -al /tmp/cluster
EXPOSE 8000
EXPOSE 8089
ENTRYPOINT ["/tmp/run.sh"]