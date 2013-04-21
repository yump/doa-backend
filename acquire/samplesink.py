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

import time
import logging
import json
from urllib import request

"""The samplesink module provides a generic interface for backends to store
I/Q samples from an antenna array. New storage backends should subclass
samplesink.samplesink, and override _init() and _stow() as necessary.
"""

class Samplesink:
    """
    A superclass for backends to store samples.  Files, databases
    http APIs, line printers, N-redundant carrier pidgeons, etc.
    
    Samples are grouped into traversals of the entire antenna array.  It is 
    assumed that a repetition of an antenna number is the beginning of a new
    traversal.
    """

    def __init__(self):
        self.seen = set()
        self.trav_idx = 0
        self.polysample = {}
        log = logging.getLogger(__name__)
    
    def close(self):
        self.reset()

    def put(self,ant,sample):
        """
        Accept a sample for storage. Samples are accumulated until a repeat
        appears, at which time they are all conveyed to the backend together.
        """
        if ant in self.seen:       #detect traverse boundaries
            if self.trav_idx == 0: #learn allowed antenna IDs
                self.allowed_ant = frozenset(self.seen)
                self.num_antennas = len(self.allowed_ant)
            # Send the collated sample to the backend, with timestamp, and
            # prepare for another traverse.
            self._stow(time.time(), self.polysample)
            self.trav_idx += 1
            self.seen.clear()      #reset to begin new traverse
            self.polysample = {}
        self.seen.add(ant)
        if self.trav_idx != 0 and ant not in self.allowed_ant:
            raise ValueError("Bad antenna ID, not in initial pattern.")
        # Accumulate samples
        self.polysample[ant] = sample
        #let the backend do whatever

    def _stow(self, timestamp, sampledict):
        """Convey the data to the backend. Sampledict maps antenna IDs to data.
        """
        raise NotImplementedError

    def reset(self):
        self._stow(time.time(), self.polysample)
        self.seen.clear()      #reset to begin new traverse
        self.polysample = {}
        self.trav_idx = 0


class ReprPrinter(Samplesink):
    """
    Samplesink that prints the data on stdout.
    """
    def __init__(self,fn):
        super().__init__()
        self.fn = fn

    def _stow(self, timestamp, sampledict):
        with open(self.fn,"a") as outfile:
            print("{}\t{}".format(timestamp,sampledict), file=outfile)


class JSONSender(Samplesink):
    """
    Samplesink that sends the samples to a remote machine with JSON encoding
    """
    def __init__(self,url):
        super().__init__()
        self.url = url

    def _stow(self, timestamp, sampledict):
        jsondata = json.dumps([timestamp,sampledict]).encode('UTF-8')
        headers = {}
        headers['Content-Type'] = 'application/json'
        req = request.Request(self.url, jsondata, headers)
        request.urlopen(req)


