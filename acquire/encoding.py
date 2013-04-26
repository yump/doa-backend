
# WARNING: This file dictates the JSON encoding used by
# acquire.acquisitionServer and by music-server, and is itself shared.  Any
# changes made to this file should be made in both places to preserve
# interoperability.  The original author ensured the consistency of both files
# by using hardlinks.

class SampleObject:
    """
    Transmission format is the JSON serialization of this object's __dict__.
    """
    def __init__(
        self,
        uuid,
        dataformat,
        sequence,
        timestamp,
        real,
        imag=None
    ):
        self.uuid = uuid
        self.dataformat = dataformat
        self.sequence = sequence
        self.timestamp = timestamp
        # real and imag are dicts mapping antenna IDs to sample vectors
        self.real = real
        self.imag = imag

    @classmethod
    def from_dict(cls,initdict):
        # convert json's string integers back to integers
        imag = { int(ant):data for ant,data in initdict["imag"].items() }
        real = { int(ant):data for ant,data in initdict["real"].items() }
        return cls(
            uuid = initdict["uuid"],
            dataformat = initdict["dataformat"],
            sequence = int(initdict["sequence"]),
            timestamp = initdict["timestamp"],
            real = real,
            imag = imag
        )


