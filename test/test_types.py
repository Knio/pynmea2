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
    assert msg.sentence_type == 'RTE'
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
    assert msg.sentence_type == 'R00'
    assert msg.waypoint_list == ['A','B','C']

    msg.waypoint_list = ['ABC','DEF']
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

from pynmea2 import nmea


def test_proprietary():
    class ABCX(nmea.ProprietarySentence):
        fields = (
            ('First', 'a'),
            ('Second', 'b'),
        )

    data = '$PABCX,1,2*4B'
    msg = pynmea2.parse(data)
    assert isinstance(msg, ABCX)
    assert msg.manufacturer == 'ABC'
    assert msg.sentence_type =='X'
    assert msg.a == '1'
    assert msg.b == '2'
    assert str(msg)== data

def test_proprietary_with_comma():
    class TNLPJT(nmea.ProprietarySentence):
        fields = (
                  ('Coordinate System', 'coord_name'),
                  ('Project Name', 'project_name'),
                  )
        def render(self, checksum=True, dollar=True, newline=False):
            res = 'P' + self.manufacturer + ',' + self.sentence_type + ','
            res += ','.join(self.data)
            if checksum:
                res += '*%02X' % nmea.NMEASentence.checksum(res)
            if dollar:
                res= '$' + res
            if newline:
                res += (newline is True) and '\r\n' or newline
            return res
    
    
    data = '$PTNL,PJT,NAD83(Conus),CaliforniaZone 4 0404*51'
    msg = pynmea2.parse(data)
    assert isinstance(msg, TNLPJT)
    assert msg.manufacturer == 'TNL'
    assert msg.sentence_type == 'PJT'
    assert msg.coord_name == 'NAD83(Conus)'
    assert msg.project_name == 'CaliforniaZone 4 0404'
    assert str(msg)== data
