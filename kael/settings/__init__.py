import os

SSL_KEYFILE = os.path.split(os.path.realpath(__file__))[0] + os.sep + "server.key"
SSL_CERTFILE = os.path.split(os.path.realpath(__file__))[0] + os.sep + "server.crt"