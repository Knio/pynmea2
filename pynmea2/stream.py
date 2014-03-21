from __future__ import unicode_literals
from . import nmea

class NMEAStreamReader(object):
    '''
    Reads NMEA sentences from a stream.
    '''
    def __init__(self, stream=None):
        '''
        Create NMEAStreamReader object.

        `stream`: file-like object to read from, can be omitted to
        pass data to `next` manually
        '''
        self.stream = stream
        self.buffer = ''

    def next(self, data=None):
        '''
        consume `data` (if given, or calls `stream.read()` if `stream` was given
        in the constructor) and return a list of `NMEASentence` objects parsed
        from the stream (may be empty)
        '''
        if data is None:
            if self.stream:
                data = self.stream.readline()
            else:
                return []

        lines = (self.buffer + data).split('\n')
        self.buffer = lines.pop()

        return [nmea.NMEASentence.parse(line) for line in lines]
