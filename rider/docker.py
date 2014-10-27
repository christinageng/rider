import sys
import ssl

import docker
import os
from rider.log import logger


class DockerClientFactory(object):
    DOCKER_CERT_PATH = "DOCKER_CERT_PATH"
    DOCKER_TLS_VERIFY = "DOCKER_TLS_VERIFY"
    DOCKER_HOST = "DOCKER_TLS_VERIFY"

    @classmethod
    def get_docker_client(cls):
        if sys.platform.lower().startswith("darwin"):
            try:
                docker_cert_path = os.environ[cls.DOCKER_CERT_PATH]
                docker_host = os.environ[cls.DOCKER_HOST]
            except Exception:
                logger.error("Please set the environment variables for the boot2docker\n")
                sys.exit(1)

            verify = os.path.join(docker_cert_path, "ca.pem")
            client_cert = (os.path.join(docker_cert_path, "cert.pem"), os.path.join(docker_cert_path, "key.pem"))
            tls_config = docker.tls.TLSConfig(verify=verify, client_cert=client_cert, ssl_version=ssl.PROTOCOL_TLSv1,
                                              assert_hostname=False)

            if docker_host.lower().startswith("tcp:"):
                base_url = "https" + docker_host[3:]
            else:
                logger.error("the DOCKER_HOST is not starts with tcp")
                sys.exit(1)

            return docker.Client(base_url=base_url, tls=tls_config)

        elif sys.platform.lower().startswith("linux"):
            base_url = "unix://var/run/docker.sock"
            return docker.Client(base_url=base_url)
        else:
            logger.error("current os platform is not supported\n")
            sys.exit(1)


def docker_client():
    tls_config = docker.tls.TLSConfig(verify='/Users/cesc/.boot2docker/certs/boot2docker-vm/ca.pem',
                                      client_cert=('/Users/cesc/.boot2docker/certs/boot2docker-vm/cert.pem',
                                                   '/Users/cesc/.boot2docker/certs/boot2docker-vm/key.pem'),
                                      ssl_version=ssl.PROTOCOL_TLSv1,
                                      assert_hostname=False)
    client = docker.Client(base_url='https://192.168.59.103:2376', tls=tls_config)
    return client