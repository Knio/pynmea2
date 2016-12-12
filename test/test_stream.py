import pytest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import pynmea2

DATA = "$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D\n"


def test_stream():
    sr = pynmea2.NMEAStreamReader()
    assert len(list(sr.next(''))) == 0
    assert len(list(sr.next(DATA))) == 1
    assert len(list(sr.next(DATA))) == 1

    sr = pynmea2.NMEAStreamReader()
    assert len(list(sr.next(DATA))) == 1
    assert len(list(sr.next(DATA[:10]))) == 0
    assert len(list(sr.next(DATA[10:]))) == 1

    sr = pynmea2.NMEAStreamReader()
    assert list(sr.next()) == []

    f = StringIO(DATA * 2)
    sr = pynmea2.NMEAStreamReader(f)
    assert len(list(sr.next())) == 1
    assert len(list(sr.next())) == 1
    assert len(list(sr.next())) == 0


def test_raise_errors():
    sr = pynmea2.NMEAStreamReader(errors='raise')
    assert list(sr.next('foobar')) == []
    with pytest.raises(pynmea2.ParseError):
        assert list(sr.next('foo\n'))


def test_yield_errors():
    sr = pynmea2.NMEAStreamReader(errors='yield')
    assert list(sr.next('foobar')) == []
    data = list(sr.next('foo\n' + DATA))
    assert len(data) == 2
    assert isinstance(data[0], pynmea2.ParseError)
    assert isinstance(data[1], pynmea2.GGA)


def test_ignore_errors():
    sr = pynmea2.NMEAStreamReader(errors='ignore')
    assert list(sr.next('foobar')) == []
    data = list(sr.next('foo\n' + DATA))
    assert len(data) == 1
    assert isinstance(data[0], pynmea2.GGA)


def test_bad_error_value():
    with pytest.raises(ValueError):
        sr = pynmea2.NMEAStreamReader(errors='bad')
