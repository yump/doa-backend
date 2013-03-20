import time
import logging

"""The samplesink module provides a generic interface for backends to store
I/Q samples from an antenna array. New storage backends should subclass
samplesink.samplesink, and override _init() and _stow() as necessary.
"""

class samplesink:
	"""A superclass for backends to store samples.  Files, databases
	http APIs, line printers, N-redundant carrier pidgeons, etc.
	
	Samples are grouped into traversals of the entire antenna array.  It is 
	assumed that a repetition of an antenna number is the beginning of a new
	traversal.
	"""

	allowed_ant = set()
	seen = set()
	trav_idx = 0
	session_id = 0
	num_antennas = 0
	log = logging.getLogger(__name__)

	def __init__(self):
		raise NotImplementedError
	
	def close(self):
		raise NotImplementedError

	def put(self,ant,sample)
		"""Accept a sample for storage."""
		if ant in self.seen:       #detect traverse boundaries
			if self.trav_idx == 0: #learn allowed antenna IDs
				self.allowed_ant = frozenset(self.seen)
				self.num_antennas = len(self.allowed_ant)
			self._endtraverse()    #hook for backends
			self.trav_idx += 1
			self.seen.clear()      #reset to begin new traverse
		self.seen.add(ant)
		if self.trav_idx != 0 and ant not in self.allowed_ant:
			raise ValueError("Bad antenna ID, not in initial pattern.")
		#let the backend do whatever
		self._stow(self,session_id, self.trav_idx, ant, time.time(), sample)

	def _stow(self, session_id, sample_id, ant_id, timestamp, sample):
		"""Convey the data to the backend.  session_id identifies a set of
		consecutive samples from the same antenna array, sample_id identifies a
		traversal, and ant_id identifies an antenna and is unique within a
		traversal.  
		"""
		raise NotImplementedError

	def _endtraverse(self):
		pass

