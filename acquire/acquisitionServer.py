#   Copyright 2012,2013 Russell Haley
#   (Please add yourself if you make changes)
#
#   This file is part of doa-backend.
#
#   doa-backend is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   doa-backend is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with doa-backend.  If not, see <http://www.gnu.org/licenses/>.

import socket
import logging
import time
from pprint import pformat
from acquire.QAMRadio import QAMRadio
from acquire.util.linefromsocket import linefromsocket

class acquisitionServer:
    """
    A service to coordinate with a controller to grab samples from a radio.
    """
    # protocol versions working as of now
    okProtVersion = {1}
    
    def __init__(self,host,port,radio,samplesink):
        self.log = logging.getLogger(__name__)
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # allow immediate restart if the server crashes
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host,port))
        self.radio = radio
        self.samplesink = samplesink
        # TODO: acquire database here

    def serve(self):
        """Begin serving -- DOES NOT RETURN
        """
        self.log.info("Server starting")
        self.sock.listen(0)
        while True:
            conn,addr = self.sock.accept()
            # TODO: create new session in database
            self.handleClient(conn,addr)
            conn.close() #closed here and only here
        return

    def handleClient(self, conn, addr):
        """Generic client handler (dispatches by version)
        """
        hello = linefromsocket(conn).decode().split()
        try:
            if hello[0] != "HELO":
                raise ValueError("HELO was not 'HELO'")
            protVersion = int(hello[1])
            if protVersion not in self.okProtVersion:
                raise ValueError("Bad protocol version")
        except Exception as err:
            conn.sendall("NOPE\n".encode())
            self.log.exception("Bad connection attempt from {} with "
                               "message {}".format(addr,pformat(hello)) )
        else:
            conn.sendall("OHAI\n".encode())
            if protVersion is 1:
                self.handleClientVer1(conn,addr)

    def handleClientVer1(self, conn, addr):
        """Protocol Version 1 client handler
        """
        self.log.info("{} connected with "
                      "protocol version 1".format(addr))
        try:
            while True:
                msg = linefromsocket(conn).decode().strip()
                if msg == "GBYE":
                    conn.sendall("GBYE\n".encode())
                    self.samplesink.reset()
                    self.log.info("Client disconnected")
                    break
                else:
                    ant = int(msg)
                    self.log.info("Asked to sample {}".format(ant))
                    self.sampleVer1(ant)
                    conn.sendall( "{}\n".format(msg).encode() )
        except ValueError:
            conn.sendall("NOPE\n".encode())
            self.log.error("Malformed v1 message {}".format(pformat(msg)) )
            raise

    def sampleVer1(self, ant):
        """Collect and log a sample from the radio
        """
        result = self.radio.sample()
        self.log.debug("Got {}".format(result))
        # Convey to Samplesink.
        self.samplesink.put(ant,result)

    def close(self):
        self.sock.close()
        self.radio.close()
            

