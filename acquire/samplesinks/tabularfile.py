from acquire.samplesink import samplesink

class tabularfile(samplesink):
	"""Writes the samples to a named file in tab-separated format."""
	def __init__(self,filename,mode='w'):
		self.file = open(filename,mode) 

	def _stow(self, session_id, sample_id, ant_id, timestamp, sample):
		file.write("{}\t{}\t{}\t{}\t{}\n".format(
			session_id,
			sample_id,
			ant_id,
			timestamp,
			sample
			))
		file.flush()
		self.log.debug("Got {} for antenna {}".format(sample,ant_id))

	def _endtraverse(self):
		file.write("\n") #more human friendly

	def close(self):
		self.file.close()

