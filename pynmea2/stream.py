from __future__ import unicode_literals
from . import nmea

__all__ = ['NMEAStreamReader']

ERRORS = ('raise', 'yield', 'ignore')

class NMEAStreamReader(object):
    '''
    Reads NMEA sentences from a stream.
    '''
    def __init__(self, stream=None, errors='raise'):
        '''
        Create NMEAStreamReader object.

        `stream`:   file-like object to read from, can be omitted to
                    pass data to `next` manually.
                    must support `.readline()` which returns a string

        `errors`: behaviour when a parse error is encountered. can be one of:
            `'raise'` (default) raise an exception immediately
            `'yield'`           yield the ParseError as an element in the
                                stream, and continue reading at the next line
            `'ignore'`          completely ignore and suppress the error, and
                                continue reading at the next line
        '''

        if errors not in ERRORS:
            raise ValueError('errors must be one of {!r} (was: {!r})'
                    .format(ERRORS, errors))

        self.errors = errors
        self.stream = stream
        self.buffer = ''

    def next(self, data=None):
        '''
        consume `data` (if given, or calls `stream.read()` if `stream` was given
        in the constructor) and yield a list of `NMEASentence` objects parsed
        from the stream (may be empty)
        '''
        if data is None:
            if self.stream:
                data = self.stream.readline()
            else:
                return

        lines = (self.buffer + data).split('\n')
        self.buffer = lines.pop()

        for line in lines:
            try:
                msg = nmea.NMEASentence.parse(line)
                yield msg
            except nmea.ParseError as e:
                if self.errors == 'raise':
                    raise e
                if self.errors == 'yield':
                    yield e
                if self.errors == 'ignore':
                    pass

    __next__ = next

    def __iter__(self):
        '''
        Support the iterator protocol.

        This allows NMEAStreamReader object to be used in a for loop.

          for batch in NMEAStreamReader(stream):
              for msg in batch:
                  print msg
        '''
        return self
