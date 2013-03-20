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

