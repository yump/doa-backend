#!/usr/bin/env python3

import fieldfox
import socket
import logging
import time
from pprint import pformat

class acquisitionServer:

	# protocol versions working as of now
	okProtVersion = {1}
	
	def __init__(self,host,port,fieldfoxip):
		self.log = logging.getLogger()
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		# allow immediate restart if the server crashes
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((host,port))
		self.log.info("Trying to connect to network analyzer...")
		self.netAnalyzer = fieldfox.FieldFox(fieldfoxip)
		self.log.info("Successfully connected to network analyzer.")
		# TODO: acquire database here

	## Begin serving -- DOES NOT RETURN
	def serve(self):
		self.log.info("Server starting")
		self.sock.listen(0)
		while True:
			conn,addr = self.sock.accept()
			# TODO: create new session in database
			self.handleClient(conn,addr)
			conn.close() #closed here and only here
		return

	## Generic client handler (dispatches by version)
	def handleClient(self, conn, addr):
		hello = conn.recv(1024).decode().split()
		try:
			assert hello[0] == "HELO"
			protVersion = int(hello[1])
			assert protVersion in self.okProtVersion
		except Exception as err:
			conn.sendall("NOPE\n".encode())
			self.log.exception("Bad connection attempt from {} with "
			                   "message {}".format(addr,pformat(hello)) )
		else:
			conn.sendall("OHAI\n".encode())
			if protVersion is 1:
				self.handleClientVer1(conn,addr)

	## Protocol Version 1 client handler
	def handleClientVer1(self, conn, addr):
		self.log.info("{} connected with "
		              "protocol version 1".format(addr))
		try:
			while True:
				msg = conn.recv(1024).decode().strip()
				if msg == "GBYE":
					conn.sendall("GBYE\n".encode())
					self.log.info("Client disconnected")
					break
				else:
					ant = int(msg)
					self.sampleVer1(ant)
					conn.sendall( "{}\n".format(msg).encode() )
		except ValueError:
			conn.sendall("NOPE\n".encode())
			self.log.error("Malformed v1 message {}".format(pformat(msg)) )

	## Collect and log a sample from the network analyzer
	def sampleVer1(self, ant):
		result = self.netAnalyzer.sample()
		self.log.debug("Got {} for antenna {}".format(result,ant))
		#TODO: stuff in database
		tstamp = time.time()

	def __del__(self):
		self.sock.close()
			

if __name__ == "__main__":
	import config
	logging.basicConfig(filename=config.logfile,level=logging.DEBUG)
	port = config.serverport
	host = config.listenhost
	ffhost = config.fieldfoxhost
	server = acquisitionServer(host,port,ffhost)
	server.serve()
