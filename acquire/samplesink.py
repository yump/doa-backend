class samplesink:
	"""A superclass for backends to store samples.  Files, databases
	http APIs, line printers, N-redundant carrier pidgeons, etc.
	
	Samples are grouped into traversals of the entire antenna array.  It is 
	assumed that a repetition of an antenna number is the beginning of a new
	traversal.
	"""

	self.seen = set()
	self.trav_idx = 0

	def __init__(self):
		raise NotImplementedError

	def put(self,ant,sample)
		"""Accept a sample for storage."""
		if ant in self.seen:
			self.trav_idx += 1
			self.seen.clear()
		self.seen.add(ant)
		self._stow(self.trav_idx, ant, sample)

	def _stow(self, sample_id, ant_id, sample):
		"""Convey the data to the backend.  sample_id identifies a traversal,
		and ant_id identifies an antenna and is unique within a traversal.
		"""
		raise NotImplementedError

class pyfile(samplesink):
	"""Writes the samples to a named file in python repr() format."""
	def __init__(self,filename,mode='w'):
		super().__init
		self.file = open(filename,mode)
	
	def put(self,sample)
