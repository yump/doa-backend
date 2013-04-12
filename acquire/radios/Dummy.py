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

from ..QAMRadio import QAMRadio
import time

class Dummy(QAMRadio):

    """A class to pretend to be an Agilent FieldFox network analyzer."""

    def __init__(self, host=None, port=None):
        pass

    def sample(self):
        time.sleep(0.100)
        return ("4","2")


