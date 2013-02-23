from acquire.radio.radio import radio
import time

class dummy(radio):

	"""A class to pretend to be an Agilent FieldFox network analyzer."""

	def __init__(self, host=None, port=None):
		pass

	def sample(self):
		time.sleep(0.100)
		return ["4","2"]


