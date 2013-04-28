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

import telnetlib
import scipy as sp
import logging
from ..QAMRadio import QAMRadio

class FieldFox(QAMRadio):
    """A class to communicate with the Agilent FieldFox network analyzer."""
    def __init__(
        self, 
        host,
        port=5025,
        freq=2.45e9, 
        span=0,
        ifbw=3e2,
        npoints=3,
        meas_type="S21",
        meas_format="phase"
    ):
        """
        Create a FieldFox radio.

        Parameters
        ----------
        freq : float
            Center frequency of operation

        span : float
            Bandwidth span over which to sweep.  freq=2.45e9, span=100e6 would
            sweep from 2.4 to 2.5 GHz, for example.

        ifbw : float
            Intermediate frequency bandwidth

        npoints : int
            Number of points to sample

        meas_type : string
            One of "S11", "S21", "S12", "S22".

        meas_format : string
            One of "phase", "uphase", "VSWR", "gdelay", "raw", etc. See Agilent
            FieldFox Programming Guide.
        """
        # Validate npoints argument within capabilities of FieldFox
        if npoints > 1001 or npoints < 3:
            raise ValueError("npoints must be between 3 and 1001")
        self.log = logging.getLogger(__name__)

        # Connect
        self.log.info("Connecting to FieldFox on {}:{}...".format(host,port))
        self.conn = telnetlib.Telnet(host, port)
        
        topfreq = freq + span/2
        botfreq = freq - span/2
        self.meas_format = meas_format

        # Configure FieldFox with measurement parameters
        self.log.info("Setting up FieldFox...")
        self.scpi("CALC:PAR1:DEF {}".format(meas_type))
        self.scpi("INIT:CONT 0")                        # single sweep mode
        if meas_format != "raw":
            self.scpi("CALC:SEL:FORM {}".format(meas_format))
        self.scpi("SENS:SWE:POIN {}".format(npoints)) 
        self.scpi("SENS:FREQ:STAR {}".format(botfreq))
        self.scpi("SENS:FREQ:STOP {}".format(topfreq))
        self.scpi(":BWID {}".format(ifbw))              # minimum IF bandwidth
        self.scpi("DISP:ENAB 0")                        # Shaves ~100ms
        self.sync()
        self.log.info("FieldFox ready.")

    def __del__(self):
        self.conn.close()

    def sample(self):
        """
        Collect a sample.

        Returns
        -------
        Either one of these, depending on measurement:

        ([real],[imag]) : float
            Vectors of real and imaginary parts. If a real measurement is
            taken, [imag] is a vector of zeros.    
        """
        # Trigger a sweep.
        self.scpi("INIT")
        self.barrier()

        if self.meas_format == "raw":
            # Get raw complex samples.
            self.scpi("CALC:DATA:SDAT?")
            answer =  self.conn.read_until(b'\n').decode('ascii')
            parsed = answer.strip().split(",")
            # even indicies are real part, odd are imaginary part
            real = [ float(parsed[i]) for i in range(0,len(parsed),2) ]
            imag = [ float(parsed[i]) for i in range(1,len(parsed),2) ]
            return (real,imag)
        else:
            # Get formatted samples.
            self.scpi("CALC:DATA:FDAT?")
            answer =  self.conn.read_until(b'\n').decode('ascii')
            parsed = answer.strip().split(",")
            return ( [float(x) for x in parsed], [0.0]*len(parsed) )

    def sync(self):        
        """
        Wait for completion of pending commands.
        """
        self.scpi("*OPC?")
        self.conn.read_until(b'\n')

    def barrier(self):
        """
        Force previous commands to finish before subsequent commands.
        """
        self.scpi("*WAI")

    def scpi(self, command):
        """
        Send a string to the SCPI instrument.
        Handles encoding and termination.
        """
        self.conn.write(command.encode('ascii') + b'\n')

    def command(self, command):
        """
        Send an SCPI command and return the result. For human interactive use.
        """
        self.scpi(command)
        return conn.read_until(b'\n').decode('ascii')

    def close(self):
        self.conn.close()
