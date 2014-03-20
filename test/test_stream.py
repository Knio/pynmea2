from __future__ import unicode_literals
import pynmea2
from tempfile import TemporaryFile

def test_stream():
    data = "$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D\n"

    sr = pynmea2.NMEAStreamReader()
    assert len(sr.next('')) == 0
    assert len(sr.next(data)) == 1
    assert len(sr.next(data)) == 1

    sr = pynmea2.NMEAStreamReader()
    assert len(sr.next(data)) == 1
    assert len(sr.next(data[:10])) == 0
    assert len(sr.next(data[10:])) == 1

    sr = pynmea2.NMEAStreamReader()
    assert sr.next() == []

    t = TemporaryFile()
    ''' Handle Exception for Python 2.7 and 3.3 Compatibility '''
    try:
       bdata = bytes(data,'UTF-8')
    except TypeError:
       bdata = data
    t.write(bdata)
    t.seek(0)
    sr = pynmea2.NMEAStreamReader(t)
    assert len(sr.next()) == 1
    assert len(sr.next()) == 0

    sr = pynmea2.NMEAStreamReader(data)
    assert sr.stream == None