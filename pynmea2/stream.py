from __future__ import unicode_literals
from . import nmea

class NMEAStreamReader(object):
    '''
    Reads NMEA sentences from a stream.
    '''
    def __init__(self, stream=None, stream_size=-1):
        '''
        Create NMEAStreamReader object.

        `stream`: file-like object to read from, can be omitted to
        pass data to `next` manually
        `stream_size`: determines # of bytes to read from stream for each
        `next` user configurable to help responsiveness of stream reader
        '''
        self.stream = stream
        self.buffer = ''
        self.stream_size = stream_size

    def next(self, data=None):
        '''
        consume `data` (if given, or calls `stream.read()` if `stream` was given
        in the constructor) and return a list of `NMEASentence` objects parsed
        from the stream (may be empty)
        '''
        if data is None:
            if self.stream:
                data = self.stream.read(self.stream_size)
            else:
                return []

        lines = (self.buffer + data).split('\n')
        self.buffer = lines.pop()

        return [nmea.NMEASentence.parse(line) for line in lines]
