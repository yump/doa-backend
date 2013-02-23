import logging
import acquire.config
from acquire.acquisitionServer import acquisitionServer
from acquire.radio.dummy import dummy

logging.basicConfig(filename=acquire.config.logfile,level=logging.DEBUG)
port = acquire.config.serverport
host = acquire.config.listenhost
ffhost = acquire.config.fieldfoxhost
radio = dummy()
server = acquisitionServer(host,port,radio)
server.serve()

