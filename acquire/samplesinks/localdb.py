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
from contextlib import closing
import squlite3

class localdb(samplesink):

	def __init__(self,dbfilename, config_name):
		self.dbcon = self._getdb(dbfilename)
		with closing(dbcon.cursor()) as cur:
			#TODO: get config_id
		
	def close(self):
		self.dbcon.rollback()
		self.dbcon.close()

	def _getdb(self, dbfilename, ):
		"""Idempotently initialilze the database and get a connection
		"""
		dbcon = sqlite3.connect(dbfilename)
		cur = dbcon.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS config("
				"config_name TEXT,"
				"config_id INTEGER"
				")"
				)
		cur.execute("CREATE TABLE IF NOT EXISTS antenna("
				"config_id INTEGER,"
				"antenna_id INTEGER,"
				"x DOUBLE," 
				"y DOUBLE," 
				"z DOUBLE," 
				"polarization TEXT" 
				")"
				)
		cur.execute("CREATE TABLE IF NOT EXISTS sample("
				"config_id INTEGER,"
				"session_id INTEGER,"
				"sample_id INTEGER,"
				"antenna_id INTEGER,"
				"time DOUBLE,"
				"I TEXT,"
				"Q TEXT"
				")"
				)
		dbcon.commit()
		cur.close()
		return dbcon

	

