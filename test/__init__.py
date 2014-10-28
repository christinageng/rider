import ssl

import container


boot2docker = "192.168.59.103:2376"

tls_config = container.tls.TLSConfig(verify='/Users/cesc/.boot2docker/certs/boot2docker-vm/ca.pem',
                                     client_cert=('/Users/cesc/.boot2docker/certs/boot2docker-vm/cert.pem',
                                                  '/Users/cesc/.boot2docker/certs/boot2docker-vm/key.pem'),
                                     ssl_version=ssl.PROTOCOL_TLSv1,
                                     assert_hostname=False)

client = container.Client(base_url='https://192.168.59.103:2376', tls=tls_config)
print client.images()
