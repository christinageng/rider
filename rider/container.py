import sys
import ssl
import time

import docker
import os
from rider.log import logger
from rider import utils


class DockerClientFactory(object):
    DOCKER_CERT_PATH = "DOCKER_CERT_PATH"
    DOCKER_TLS_VERIFY = "DOCKER_TLS_VERIFY"
    DOCKER_HOST = "DOCKER_HOST"

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


class SplunkContainerFactory(object):
    def __init__(self):
        self.docker = DockerClientFactory.get_docker_client()

    def create_container(self, image, role, command, environment=None, volumes=None, links=None, binds=None):
        timestamp = int(time.time())
        container_name = "%s_%s" % (role, timestamp)
        result = self.docker.create_container(image=image, command=command, detach=True,
                                              environment=environment,
                                              volumes=volumes,
                                              name=container_name,
        )
        self.docker.start(result["Id"], links=links, binds=binds, publish_all_ports=True)
        detail = self.docker.inspect_container(result["Id"])
        container = SplunkContainer(result["Id"], role, detail)
        if not container.health_check():
            logger.error("start the container fail ,rollback the container")
            try:
                self.docker.stop(container.cid)
                self.docker.remove_container(container.cid)
            except:
                pass
            sys.exit(1)
        else:
            logger.info("create the container %s" % container_name)
            return container_name, container


class SplunkContainer(object):
    def __init__(self, cid, role, detail):
        self.cid = cid
        self.role = role
        self.name = detail["Name"][1:]
        self.internal_ip = detail["NetworkSettings"]["IPAddress"]
        self.port_mapping = {}
        for k, v in detail["NetworkSettings"]["Ports"].items():
            self.port_mapping[k.split("/")[0]] = v[0]["HostPort"]

    def health_check(self, timeout=10 * 60):
        if sys.platform.lower().startswith("darwin"):
            docker_host = os.environ[DockerClientFactory.DOCKER_HOST]
            host = docker_host[docker_host.rfind("/") + 1:docker_host.rfind(":")]
        elif sys.platform.lower().startswith("linux"):
            host = "127.0.0.1"

        result = utils.health_check(host, self.port_mapping["8089"], timeout, https=True)
        return result

    def __str__(self):
        return "%s,%s,%s" % (self.name, self.cid, self.port_mapping)

    __repr__ = __str__

    def to_dict(self):
        return {
            "cid": self.cid,
            "internal_ip": self.internal_ip,
            "name": self.name,
            "port_mapping": ",".join(["%s->%s" % (k, v) for k, v in self.port_mapping.items()])
        }


def check_image_existed(image_name):
    docker_client = DockerClientFactory.get_docker_client()
    symbol = image_name.rfind(":")
    if symbol == -1:
        repo_name = image_name
        image_name = "%s:latest" % image_name
    else:
        repo_name = image_name[:symbol]

    results = docker_client.images(name=repo_name)
    for result in results:
        if result["RepoTags"][0] == image_name:
            return True
    return False


if __name__ == "__main__":
    docker_container = DockerClientFactory.get_docker_client()
    result = check_image_existed(image_name="busybox:afdsf")
    print result