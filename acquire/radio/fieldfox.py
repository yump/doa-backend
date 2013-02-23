import telnetlib
from acquire.radio.radio import radio

class FieldFox(radio):

	"""A class to communicate with the Agilent FieldFox network analyzer."""

	def __init__(self, host, port=5025):
		self.conn = telnetlib.Telnet(host, port)
		self.scpi("*RST")                  # reset
		self.barrier()
		self.scpi("CALC:PAR1:DEF S21")     # measure S21
		self.scpi("INIT:CONT 0")           # single sweep mode
		self.scpi("CALC:SEL:FORM uphase")  # unwrapped phase
		self.scpi("SENS:SWE:POIN 3")       # get 3 points
		self.scpi("SENS:FREQ:STAR 2.45e9") # we 2.45 GHz now
		self.scpi("SENS:FREQ:STOP 2.45e9")
		self.scpi(":BWID 3e2")             # minimum IF bandwidth
		self.scpi("DISP:ENAB 0")           # Shaves ~100ms
		self.sync()

	def __del__(self):
		self.conn.close()

	def sample(self):
		self.scpi("INIT")
		self.barrier()
		self.scpi("CALC:DATA:SDAT?")       # get formatted data
		answer =  self.conn.read_until(b'\n').decode('ascii')
		parsed = answer.strip().split(",")
		return parsed[0:2]

	def sync(self):        # wait for completion of pending commands
		self.scpi("*OPC?")
		self.conn.read_until(b'\n')

	def barrier(self):        # force previous commands to finish first
		self.scpi("*WAI")

	def scpi(self, command):
		self.conn.write(command.encode('ascii') + b'\n')

	def command(self, command):
		self.scpi(command)
		return conn.read_until(b'\n').decode('ascii')

