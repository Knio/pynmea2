import pytest
import pynmea2

data = "$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D"


def test_version():
    version = '0.6.0'
    assert pynmea2.version == version
    assert pynmea2.__version__ == version


def test_sentence():
    msg = pynmea2.parse(data)
    assert msg.talker == 'GP'
    assert msg.sentence_type == 'GGA'
    assert str(msg) == data

def test_checksum():
    d = data[:-2] + '00'
    with pytest.raises(ValueError):
        msg = pynmea2.parse(d)

def test_mixin():
    msg = pynmea2.parse(data)
    assert msg.latitude == -19.484083333333334
    assert msg.longitude == 24.1751


def test_missing():
    msg = pynmea2.parse("$GPVTG,108.53,T,,M,0.04,N,0.07,K,A*31")
    assert msg.mag_track == None

#
# ^o^
#       |\    ship it!
#       | \   /
#      /|  \
#   __/_|___\_
# ~~\________/~~
#  ~~~~~~~~~~~~

