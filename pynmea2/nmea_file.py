from __future__ import unicode_literals
from pynmea2.nmea import NMEASentence


class NMEAFile(file):
    """
    Reads NMEA sentences from a file similar to a standard python file object.
    """

    def next(self):
        """
        Iterate through the file object returning NMEASentence objects
        :return: NMEASentence
        """
        data = super(NMEAFile, self).next()
        return NMEASentence.parse(data)

    def readline(self):
        """
        Return the next NMEASentence in the file object
        :return: NMEASentence
        """
        data = super(NMEAFile, self).readline()
        s = NMEASentence.parse(data)
        return s

    def read(self):
        """
        Return a list of NMEASentence objects for each line in the file
        :return: list of NMEASentence objects
        """
        return [s for s in self]
