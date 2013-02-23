import logging
import acquire.config
from acquire.acquisitionServer import acquisitionServer

logging.basicConfig(filename=acquire.config.logfile,level=logging.DEBUG)
port = acquire.config.serverport
host = acquire.config.listenhost
ffhost = acquire.config.fieldfoxhost
server = acquisitionServer(host,port,ffhost)
server.serve()

