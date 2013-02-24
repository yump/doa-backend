class QAMRadio:
	"""Superclass for QAM radios."""

	def __init__(self, host=None, port=None):
		raise NotImplementedError

	def sample(self):
		raise NotImplementedError

