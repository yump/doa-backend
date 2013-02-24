#!/usr/bin/env python3

import socket
import logging
import time
from pprint import pformat
from acquire.QAMRadio import QAMRadio
from acquire.util.linefromsocket import linefromsocket

class acquisitionServer:

	"""A service to coordinate with a controller to grab samples from a radio.
	"""

	# protocol versions working as of now
	okProtVersion = {1}
	
	def __init__(self,host,port,radio):
		self.log = logging.getLogger()
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		# allow immediate restart if the server crashes
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((host,port))
		self.log.info("Trying to connect to network analyzer...")
		self.radio = radio
		self.log.info("Successfully connected to network analyzer.")
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
					self.log.info("Client disconnected")
					break
				else:
					ant = int(msg)
					self.sampleVer1(ant)
					conn.sendall( "{}\n".format(msg).encode() )
		except ValueError:
			conn.sendall("NOPE\n".encode())
			self.log.error("Malformed v1 message {}".format(pformat(msg)) )

	def sampleVer1(self, ant):
		"""Collect and log a sample from the radio
		"""
		result = self.radio.sample()
		self.log.debug("Got {} for antenna {}".format(result,ant))
		#TODO: stuff in database
		tstamp = time.time()

	def __del__(self):
		self.sock.close()
			

