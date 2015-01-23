import pytest
import pynmea2

import datetime

from decimal import Decimal

def test_GGA():
    data = "$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D"
    msg = pynmea2.parse(data)
    assert msg.talker == 'GP'
    assert msg.sentence_type == 'GGA'
    assert isinstance(msg, pynmea2.GGA)

    # Timestamp
    assert msg.timestamp        == datetime.time(18, 43, 53, 70000)
    # Latitude
    assert msg.lat              == '1929.045'
    # Latitude Direction
    assert msg.lat_dir          == 'S'
    # Longitude
    assert msg.lon              == '02410.506'
    # Longitude Direction
    assert msg.lon_dir          == 'E'
    # GPS Quality Indicator
    assert msg.gps_qual         == '1'
    # Number of Satellites in use
    assert msg.num_sats         == '04'
    # Horizontal Dilution of Precision
    assert msg.horizontal_dil   == '2.6'
    # Antenna Alt above sea level (mean)
    assert msg.altitude         == 100.0
    # Units of altitude (meters)
    assert msg.altitude_units   == 'M'
    # Geoidal Separation
    assert msg.geo_sep          == '-33.9'
    # Units of Geoidal Separation (meters)
    assert msg.geo_sep_units    == 'M'
    # Age of Differential GPS Data (secs)
    assert msg.age_gps_data     == ''
    # Differential Reference Station ID
    assert msg.ref_station_id   == '0000'

    msg.altitude = 200.0
    assert str(msg) == "$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,200.0,M,-33.9,M,,0000*5E"

def test_RTE():
    data = "$GPRTE,2,1,c,0,PBRCPK,PBRTO,PTELGR,PPLAND,PYAMBU,PPFAIR,PWARRN,PMORTL,PLISMR*73"
    msg = pynmea2.parse(data)
    assert msg.talker == 'GP'
    assert msg.sentence_type == 'RTE'
    assert "2" == msg.num_in_seq
    assert "1" == msg.sen_num
    assert "c" == msg.start_type
    assert "0" == msg.active_route_id
    assert msg.waypoint_list == [
        "PBRCPK", "PBRTO", "PTELGR", "PPLAND", "PYAMBU",
        "PPFAIR", "PWARRN", "PMORTL", "PLISMR"]

    msg.waypoint_list = ['ABC', 'DEF']
    assert str(msg) == "$GPRTE,2,1,c,0,ABC,DEF*03"

def test_R00():
    data = "$GPR00,A,B,C*29"
    msg = pynmea2.parse(data)
    assert msg.talker == 'GP'
    assert msg.sentence_type == 'R00'
    assert msg.waypoint_list == ['A', 'B', 'C']

    msg.waypoint_list = ['ABC', 'DEF']
    assert str(msg) == "$GPR00,ABC,DEF*42"

def test_MWV():
    data = "$IIMWV,271.0,R,000.2,N,A*3B"
    msg = pynmea2.parse(data)

    assert msg.talker == 'II'
    assert msg.sentence_type == 'MWV'

    # Wind angle in degrees
    assert msg.wind_angle == Decimal('271.0')

    # Reference type
    assert msg.reference == 'R'

    # Wind speed
    assert msg.wind_speed == Decimal('0.2')

    # Wind speed units
    assert msg.wind_speed_units == 'N'

    # Device status
    assert msg.status == 'A'
    assert msg.render() == data


def test_GST():
    data = "$GPGST,172814.0,0.006,0.023,0.020,273.6,0.023,0.020,0.031*6A"
    msg = pynmea2.parse(data)
    assert isinstance(msg, pynmea2.GST)
    assert msg.timestamp == datetime.time(hour=17, minute=28, second=14)
    assert msg.rms == 0.006
    assert msg.std_dev_major == 0.023
    assert msg.std_dev_minor == 0.020
    assert msg.orientation == 273.6
    assert msg.std_dev_latitude == 0.023
    assert msg.std_dev_longitude == 0.020
    assert msg.std_dev_altitude == 0.031
    assert msg.render() == data


def test_RMC():
    data = '''$GPRMC,225446,A,4916.45,N,12311.12,W,000.5,054.7,191194,020.3,E*68'''
    msg = pynmea2.parse(data)
    assert isinstance(msg, pynmea2.RMC)
    assert msg.timestamp == datetime.time(hour=22, minute=54, second=46)
    assert msg.datestamp == datetime.date(1994, 11, 19)
    assert msg.latitude == 49.274166666666666
    assert msg.longitude == -123.18533333333333
    assert msg.datetime == datetime.datetime(1994, 11, 19, 22, 54, 46)
    assert msg.render() == data


def test_TXT():
    data = '$GNTXT,01,01,02,ROM BASE 2.01 (75331) Oct 29 2013 13:28:17*44'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.talker.TXT
    assert msg.text == 'ROM BASE 2.01 (75331) Oct 29 2013 13:28:17'


def test_ZDA():
    data = '''$GPZDA,010203.05,06,07,2008,-08,30'''
    msg = pynmea2.parse(data)
    assert isinstance(msg, pynmea2.ZDA)
    assert msg.timestamp == datetime.time(hour=1, minute=2, second=3, microsecond=50000)
    assert msg.day == 6
    assert msg.month == 7
    assert msg.year == 2008
    assert msg.local_zone == -8
    assert msg.local_zone_minutes == 30
    assert msg.datestamp == datetime.date(2008, 7, 6)
    assert msg.datetime == datetime.datetime(2008, 7, 6, 1, 2, 3, 50000, msg.tzinfo)

def test_VPW():
    data = "$XXVPW,1.2,N,3.4,M"
    msg = pynmea2.parse(data)
    assert isinstance(msg, pynmea2.VPW)
    assert msg.talker == 'XX'
    assert msg.speed_kn == 1.2
    assert msg.unit_knots == 'N'
    assert msg.speed_ms == 3.4
    assert msg.unit_ms == 'M'
