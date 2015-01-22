import pytest
import pynmea2

data = "$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D"


def test_version():
    version = '1.3.4'
    assert pynmea2.version == version
    assert pynmea2.__version__ == version


def test_sentence():
    msg = pynmea2.parse(data)
    assert msg.talker == 'GP'
    assert msg.sentence_type == 'GGA'
    assert str(msg) == data


def test_checksum():
    d = data[:-2] + '00'
    with pytest.raises(pynmea2.ChecksumError):
        msg = pynmea2.parse(d)


def test_attribute():
    msg = pynmea2.parse(data)
    with pytest.raises(AttributeError):
        msg.foobar


def test_fail():
    with pytest.raises(pynmea2.ParseError):
        pynmea2.parse('FOOBAR')

    with pytest.raises(pynmea2.SentenceTypeError):
        pynmea2.parse('$GPABC,1,2,3')


def test_mixin():
    msg = pynmea2.parse(data)
    assert msg.latitude  == -19.484083333333334
    assert msg.longitude ==  24.175100000000000
    assert msg.latitude_minutes  == 29.045000000000073
    assert msg.longitude_minutes == 10.506000000000085
    assert msg.latitude_seconds  ==  2.6999999999970896
    assert msg.longitude_seconds == 30.360000000000582


def test_missing():
    msg = pynmea2.parse("$GPVTG,108.53,T,,M,0.04,N,0.07,K,A*31")
    assert msg.mag_track == None

def test_missing_2():
    # $GPGSV,3,1,09,12,28,063,33,14,63,000,32,22,68,150,26,25,40,109,23*7B
    # $GPGSV,3,2,09,31,42,227,19,32,17,313,20,01,09,316,,11,08,292,*73
    # $GPGSV,3,3,09,24,03,046,*47
    msg = pynmea2.parse('$GPGSV,3,3,09,24,03,046,*47')
    assert msg.snr_4 == ''

def test_missing_3():
    data = '$GPVTG,,T,,M,0.00,N*1B'
    msg = pynmea2.parse(data)
    assert None == msg.spd_over_grnd_kmph
    assert msg.render() == data

def test_missing_4():
    data = '$GPVTG,,T,,M,0.00,N*1B'
    msg = pynmea2.parse(data)
    assert None == msg.spd_over_grnd_kmph
    assert msg.render() == data


def test_dollar():
    data = 'GPGSV,3,3,09,24,03,046,*47\r\n'
    msg = pynmea2.parse(data)
    assert msg.render(dollar=False, newline=True) == data


def test_whitespace():
    data = '  GPGSV,3,3,09,24,03,046,*47  \r\n  '
    msg = pynmea2.parse(data)
    assert msg.render(dollar=False) == data.strip()


def test_nmea_util():
    assert pynmea2.nmea_utils.dm_to_sd('0') == 0.
    assert pynmea2.nmea_utils.dm_to_sd('12108.1') == 121.135

def test_missing_latlon():
    data = '$GPGGA,201716.684,,,,,0,00,,,M,0.0,M,,0000*5F'
    msg = pynmea2.parse(data)
    print(msg)
    assert msg.latitude == 0.

def test_query():
    data = 'CCGPQ,GGA'
    msg = pynmea2.parse(data)
    assert isinstance(msg, pynmea2.QuerySentence)
    assert msg.talker == 'CC'
    assert msg.listener == 'GP'
    assert msg.sentence_type == 'GGA'


#
# ^o^
#       |\    ship it!
#       | \   /
#      /|  \
#   __/_|___\_
# ~~\________/~~
#  ~~~~~~~~~~~~

