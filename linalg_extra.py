import scipy as sp

def eigsort(eigresult):
	"""Sort the output of scipy.linalg.eig() in terms of 
	eignevalue magnitude"""

	ix = sp.argsort(abs(eigresult[0]))
	return ( eigresult[0][ix], eigresult[1][:,ix] )
