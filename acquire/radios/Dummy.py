from ..QAMRadio import QAMRadio
import time

class Dummy(QAMRadio):

	"""A class to pretend to be an Agilent FieldFox network analyzer."""

	def __init__(self, host=None, port=None):
		pass

	def sample(self):
		time.sleep(0.100)
		return ["4","2"]


