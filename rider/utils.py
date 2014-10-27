import sys
import traceback

import os


try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

TRUE_BOOLEAN = ("YES", "Y")
FALSE_BOOLEAN = ("NO", "N")


def get_prog():
    return 'rider'


def get_terminal_size():
    """Returns a tuple (x, y) representing the width(x) and the height(x)
    in characters of the terminal window."""

    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            import struct

            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
                                                 '1234'))
        except:
            return None
        if cr == (0, 0):
            return None
        if cr == (0, 0):
            return None
        return cr

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (os.environ.get('LINES', 25), os.environ.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])


def get_userinput(msg, retry=3):
    for i in xrange(retry):
        resp = raw_input(msg)
        if resp.upper() in TRUE_BOOLEAN + FALSE_BOOLEAN:
            break
    else:
        sys.stderr.write("The pagrant could been created due to the user's wrong input\n")
        sys.exit(1)
    return resp


def is_true(value):
    return value.upper() in TRUE_BOOLEAN


def format_exc(exc_info=None):
    if exc_info is None:
        exc_info = sys.exc_info()
    out = StringIO()
    traceback.print_exception(*exc_info, **dict(file=out))
    return out.getvalue()


def docker_client():
    import ssl
    import docker


    boot2docker = "192.168.59.103:2376"

    tls_config = docker.tls.TLSConfig(verify='/Users/weiwang/.boot2docker/certs/boot2docker-vm/ca.pem',
                                      client_cert=('/Users/weiwang/.boot2docker/certs/boot2docker-vm/cert.pem',
                                                   '/Users/weiwang/.boot2docker/certs/boot2docker-vm/key.pem'),
                                      ssl_version=ssl.PROTOCOL_TLSv1,
                                      assert_hostname=False)

    client = docker.Client(base_url='https://192.168.59.103:2376', tls=tls_config)
    return client