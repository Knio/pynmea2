import pytest
import pynmea2
import pynmea2.nmea_utils


def test_GGA():
    data = "$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D"
    msg = pynmea2.parse(data)
    assert msg.latitude == -19.484083333333334
    assert msg.longitude == 24.1751
    assert msg.is_valid == True

def test_latlon():
    data = "$GPGGA,161405.680,37.352387,N,121.953086,W,1,10,0.01,-110.342552,M,0.000000,M,,0000,*4E"
    msg = pynmea2.parse(data)
    with pytest.raises(ValueError):
        x =  msg.latitude
