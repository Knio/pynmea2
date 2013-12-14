import pytest
import pynmea2

import datetime

from decimal import Decimal

def test_GGA():
    data = "$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D"
    msg = pynmea2.parse(data)
    assert msg.talker == 'GP'
    assert msg.type == 'GGA'

    # Timestamp
    assert msg.timestamp        == datetime.time(18, 43, 53)
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

def test_rte():
    data = "$GPRTE,2,1,c,0,PBRCPK,PBRTO,PTELGR,PPLAND,PYAMBU,PPFAIR,PWARRN,PMORTL,PLISMR*73"
    msg = pynmea2.parse(data)
    assert msg.talker == 'GP'
    assert msg.type == 'RTE'
    assert "2" == msg.num_in_seq
    assert "1" == msg.sen_num
    assert "c" == msg.start_type
    assert "0" == msg.active_route_id
    assert msg.waypoint_list == [
        "PBRCPK", "PBRTO", "PTELGR", "PPLAND", "PYAMBU",
        "PPFAIR", "PWARRN", "PMORTL", "PLISMR"]

    msg.waypoint_list = ['ABC','DEF']
    assert str(msg) == "$GPRTE,2,1,c,0,ABC,DEF*03"

def test_r00():
    data = "$GPR00,A,B,C*29"
    msg = pynmea2.parse(data)
    assert msg.talker == 'GP'
    assert msg.type == 'R00'
    assert msg.waypoint_list == ['A','B','C']

    msg.waypoint_list = ['ABC','DEF']
    assert str(msg) == "$GPR00,ABC,DEF*42"

def test_MWV():
    data = "$IIMWV,271.0,R,000.2,N,A*3B"
    msg = pynmea2.parse(data)

    assert msg.talker == 'II'
    assert msg.type == 'MWV'

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

def test_proprietary_implemented():
    # Ensure a proprietary sentence that is explicitly implemented isn't
    # returned as a generic proprietary sentence.
    data = "$PGRME,15.0,M,45.0,M,25.0,M*1C"
    msg = pynmea2.parse(data)

    assert repr(msg) == "<RME(hpe='15.0', hpe_unit='M', vpe='45.0', vpe_unit='M', osepe='25.0', osepe_unit='M')>"


def test_proprietary_1():
    # A sample proprietary sentence from a LCJ Capteurs
    # anemometer.
    data = "$PLCJ,5F01,66FC,AA,9390,6373"
    msg = pynmea2.parse(data)

    assert msg.manufacturer == "LCJ"
    assert msg.type == "P"
    assert not msg.talker

    assert msg.data == (",5F01,66FC,AA,9390,6373", )

    assert str(msg) == data


def test_proprietary_2():
    # A sample proprietary sentence from a LCJ Capteurs anemometer.
    # Note: This sample is the main reason why we can't assume
    #       anything about the content of the proprietary sentences
    #       due to the lack of a comma after the manufacturer ID and
    #       extra comma at the end.
    data = "$PLCJE81B8,64A0,2800,2162,0E,"
    msg = pynmea2.parse(data)

    assert msg.manufacturer == "LCJ"
    assert msg.type == "P"
    assert not msg.talker

    assert msg.data == ("E81B8,64A0,2800,2162,0E,",)

    assert str(msg) == data


def test_proprietary_3():
    # A sample proprietary sentence from a Magellan device
    # (via <http://www.gpsinformation.org/dale/nmea.htm#proprietary>).
    data = "$PMGNST,02.12,3,T,534,05.0,+03327,00*40"
    msg = pynmea2.parse(data)

    assert msg.manufacturer == "MGN"
    assert msg.type == "P"
    assert not msg.talker

    assert msg.data == ("ST,02.12,3,T,534,05.0,+03327,00*40", )

    assert str(msg) == data
