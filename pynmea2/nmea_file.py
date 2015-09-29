try:
    # pylint: disable=used-before-assignment
    basestring = basestring
except NameError: # py3
    basestring = str

from .nmea import NMEASentence


class NMEAFile(object):
    """
    Reads NMEA sentences from a file similar to a standard python file object.
    """

    def __init__(self, f, *args, **kwargs):
        super(NMEAFile, self).__init__()
        if isinstance(f, basestring) or args or kwargs:
            self._file = self.open(f, *args, **kwargs)
        else:
            self._file = f
        self._context = None

    def open(self, fp, mode='r'):
        """
        Open the NMEAFile.
        """
        self._file = open(fp, mode=mode)
        return self._file

    def close(self):
        """
        Close the NMEAFile.
        """
        self._file.close()

    def __iter__(self):
        """
        Iterate through the file yielding NMEASentences
        :return:
        """
        for line in self._file:
            yield self.parse(line)

    def __enter__(self):
        if hasattr(self._file, '__enter__'):
            self._context = self._file.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._context:
            ctx = self._context
            self._context = None
            ctx.__exit__(exc_type, exc_val, exc_tb)

    def next(self):
        """
        Iterate through the file object returning NMEASentence objects
        :return: NMEASentence
        """
        data = self._file.readline()
        return self.parse(data)

    def parse(self, s):
        return NMEASentence.parse(s)

    def readline(self):
        """
        Return the next NMEASentence in the file object
        :return: NMEASentence
        """
        data = self._file.readline()
        s = self.parse(data)
        return s

    def read(self):
        """
        Return a list of NMEASentence objects for each line in the file
        :return: list of NMEASentence objects
        """
        return [s for s in self]
