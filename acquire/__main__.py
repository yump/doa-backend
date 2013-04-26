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

import logging
import acquire.config
from acquire.acquisitionServer import acquisitionServer
from acquire.radios.Dummy import Dummy
from acquire.radios.FieldFox import FieldFox
from acquire import samplesink

logging.basicConfig(filename=acquire.config.logfile,level=logging.DEBUG)

if acquire.config.dummy:
    radio = Dummy()
else:
    radio = FieldFox(
        host = acquire.config.fieldfoxhost,
        freq = acquire.config.freq, 
        span = 0,
        ifbw = acquire.config.ifbw, 
        npoints = acquire.config.npoints,
        meas_type = "S21",
        meas_format = "phase"
    )

sink = samplesink.JSONSender(
    dataformat = acquire.config.dataformat,
    freq = acquire.config.freq,
    url = acquire.config.sampleurl
)

server = acquisitionServer(
    acquire.config.listenhost,
    acquire.config.serverport,
    radio,
    sink
)
try:
    server.serve()
except (KeyboardInterrupt):
    server.close()
    print("Exiting.")
