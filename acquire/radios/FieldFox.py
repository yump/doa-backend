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

import telnetlib
from ..QAMRadio import QAMRadio

class FieldFox(QAMRadio):

	"""A class to communicate with the Agilent FieldFox network analyzer."""

	def __init__(self, host, port=5025):
		self.conn = telnetlib.Telnet(host, port)
		self.scpi("*RST")                  # reset
		self.barrier()
		self.scpi("CALC:PAR1:DEF S21")     # measure S21
		self.scpi("INIT:CONT 0")           # single sweep mode
		self.scpi("CALC:SEL:FORM uphase")  # unwrapped phase
		self.scpi("SENS:SWE:POIN 3")       # get 3 points
		self.scpi("SENS:FREQ:STAR 2.45e9") # we 2.45 GHz now
		self.scpi("SENS:FREQ:STOP 2.45e9")
		self.scpi(":BWID 3e2")             # minimum IF bandwidth
		self.scpi("DISP:ENAB 0")           # Shaves ~100ms
		self.sync()

	def __del__(self):
		self.conn.close()

	def sample(self):
		"""
		Collect an I,Q pair as a tuple of strings.
		Using strings for storage and transfer allows the final user of
		the data to convert it to its native floating point format.
		"""
		self.scpi("INIT")
		self.barrier()
		self.scpi("CALC:DATA:SDAT?")     # get I/Q sample
		#self.scpi("CALC:DATA:FDAT?")    # get unwrapped phase sample
		answer =  self.conn.read_until(b'\n').decode('ascii')
		parsed = answer.strip().split(",")
		return tuple(parsed[0:2])        # First I,Q pair

	def sync(self):        
		"""
		Wait for completion of pending commands.
		"""
		self.scpi("*OPC?")
		self.conn.read_until(b'\n')

	def barrier(self):
		"""
		Force previous commands to finish before subsequent commands..
		"""
		self.scpi("*WAI")

	def scpi(self, command):
		"""
		Send a string to the SCPI instrument.
		Handles encoding and termination.
		"""
		self.conn.write(command.encode('ascii') + b'\n')

	def command(self, command):
		"""
		Send an SCPI command and return the result. For human interactive use.
		"""
		self.scpi(command)
		return conn.read_until(b'\n').decode('ascii')

