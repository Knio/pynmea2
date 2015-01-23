try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import pynmea2

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

    f = StringIO(data * 2)
    sr = pynmea2.NMEAStreamReader(f)
    assert len(sr.next()) == 1
    assert len(sr.next()) == 1
    assert len(sr.next()) == 0
