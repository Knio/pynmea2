try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import pynmea2

def test_file():
    filepath = "nmea_file"

    nmeafile = pynmea2.NMEAFile(filepath)

    nmea_strings = nmeafile.read()
    assert len(nmea_strings) == 10
    assert all([isinstance(s, pynmea2.NMEASentence) for s in nmea_strings])
    del nmeafile

    with pynmea2.NMEAFile(filepath) as _f:
        nmea_strings = [_f.readline() for i in xrange(10)]
    assert len(nmea_strings) == 10
    assert all([isinstance(s, pynmea2.NMEASentence) for s in nmea_strings])

    with pynmea2.NMEAFile(filepath) as _f:
        nmea_strings = [s for s in _f]
    assert len(nmea_strings) == 10
    assert all([isinstance(s, pynmea2.NMEASentence) for s in nmea_strings])


test_file()