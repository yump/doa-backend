import telnetlib

class FieldFox:

	"""A class to communicate with the Agilent FieldFox network analyzer."""

	def __init__(self, host, port):
		self.conn = telnetlib.Telnet(host, port)
		self.scpi("*RST")                  # reset
		self.wait()
		self.scpi("CALC:PAR1:DEF S21")     # measure S21
		self.scpi("INIT:CONT 0")           # single sweep mode
		self.scpi("CALC:SEL:FORM uphase")  # unwrapped phase
		self.scpi("SENS:SWE:POIN 3")       # get 3 points
		self.scpi("SENS:FREQ:STAR 2.45e9") # we 2.45 GHz now
		self.scpi("SENS:FREQ:STOP 2.45e9")
		self.scpi(":BWID 3e2")             # minimum IF bandwidth
		self.wait()

	def __del__(self):
		self.conn.close()

	def sample(self):
		self.scpi("INIT")
		self.wait()
		self.scpi("CALC:DATA:FDAT?")       # get formatted data
		answer =  self.conn.read_until(b'\n').decode('ascii')
		return (answer.rstrip("\n").split(","))[0]

	def wait(self):                   # wait for completion
		self.scpi("*WAI")
		#self.conn.read_until(b'\n')

	def scpi(self, command):
		self.conn.write(command.encode('ascii') + b'\n')

	def command(self, command):
		self.conn.write(command.encode('ascii') + b'\n')
		return conn.read_until(b'\n').decode('ascii')

