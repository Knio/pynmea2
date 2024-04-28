from decimal import Decimal
import datetime

import pynmea2

def test_tnlpjk():
    data = '$PTNL,PJK,202831.50,011112,+805083.350,N,+388997.346,E,10,09,1.5,GHT+25.478,M*77'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.tnl.TNLPJK
    assert msg.manufacturer == 'TNL'
    assert msg.type == 'PJK'
    assert msg.timestamp == datetime.time(20, 28, 31, 500000, tzinfo=datetime.timezone.utc)
    assert msg.datestamp == datetime.date(2012, 11, 1)
    assert msg.northing == 805083.350
    assert msg.north == 'N'
    assert msg.easting == 388997.346
    assert msg.east == 'E'
    assert msg.gps_quality == '10'
    assert msg.num_sats == 9
    assert msg.dop == 1.5
    assert msg.height == 'GHT+25.478'

def test_tnlpjk2():
    # not sure if this is correct checksum, because of too long (for NMEA standard) msg
    data = '$PTNL,PJK,010717.00,170896,+732646.511,N,+1731051.091,E,1,05,2.7,EHT+28.345,M*7A'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.tnl.TNLPJK
    assert msg.manufacturer == 'TNL'
    assert msg.type == 'PJK'
    assert msg.timestamp == datetime.time(1, 7, 17, 0, tzinfo=datetime.timezone.utc)
    assert msg.datestamp == datetime.date(1996, 8, 17)
    assert msg.northing == 732646.511
    assert msg.north == 'N'
    assert msg.easting == 1731051.091
    assert msg.east == 'E'
    assert msg.gps_quality == '1'
    assert msg.num_sats == 5
    assert msg.dop == 2.7
    assert msg.height == 'EHT+28.345'

def test_tnlpjt():
    data = '$PTNL,PJT,NAD83(Conus),California Zone 4 0404,*5D'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.tnl.TNLPJT
    assert msg.manufacturer == 'TNL'
    assert msg.type == 'PJT'
    assert msg.coord_name == 'NAD83(Conus)'
    assert msg.project_name == 'California Zone 4 0404'

def test_tnldg_beacon():
    data = '$PTNLDG,44.0,33.0,287.0,100,0,4,1,0,,,*3E'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.tnl.TNLDG
    assert msg.manufacturer == 'TNL'
    assert msg.strength == 44.0
    assert msg.snr == 33.0
    assert msg.frequency == 287.0
    assert msg.bitrate == 100
    assert msg.channel_no == 0
    assert msg.status == '4'
    assert msg.channel_used == '1'
    assert msg.performance == 0

def test_tnldg_lband():
    data = '$PTNLDG,124.0,10.5,1557855.0,1200,2,4,0,3,,,*3C'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.tnl.TNLDG
    assert msg.manufacturer == 'TNL'
    assert msg.strength == 124.0
    assert msg.snr == 10.5
    assert msg.frequency == 1557855.0
    assert msg.bitrate == 1200
    assert msg.channel_no == 2
    assert msg.status == '4'
    assert msg.channel_used == '0'
    assert msg.performance == 3

def test_tnlvgk():
    data = '$PTNL,VGK,160159.00,010997,-0000.161,00009.985,-0000.002,3,07,1.4,M*0B'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.tnl.TNLVGK
    assert msg.manufacturer == 'TNL'
    assert msg.type == 'VGK'
    assert msg.timestamp == datetime.time(16, 1, 59, 0, tzinfo=datetime.timezone.utc)
    assert msg.datestamp == datetime.date(1997, 9, 1)
    assert msg.east == -0.161
    assert msg.north == 9.985
    assert msg.up == -0.002
    assert msg.gps_quality == '3'
    assert msg.num_sats == 7
    assert msg.dop == 1.4

def test_tnlvhd():
    data = '$PTNL,VHD,030556.00,300998,187.718,-22.138,-76.929,-5.015,0.033,0.006,3,07,2.4,M*22'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.tnl.TNLVHD
    assert msg.manufacturer == 'TNL'
    assert msg.type == 'VHD'
    assert msg.timestamp == datetime.time(3, 5, 56, 0, tzinfo=datetime.timezone.utc)
    assert msg.datestamp == datetime.date(1998, 9, 30)
    assert msg.azimuth == 187.718
    assert msg.azdt == -22.138
    assert msg.vertical == -76.929
    assert msg.vertdt == -5.015
    assert msg.range == 0.033
    assert msg.rdt == 0.006
    assert msg.gps_quality == '3'
    assert msg.num_sats == 7
    assert msg.pdop == 2.4

def test_tnlevt():
    data = '$PTNL,EVT,131007.999785,2,460,2181,5,18*72'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.tnl.TNLEVT
    assert msg.manufacturer == 'TNL'
    assert msg.type == 'EVT'
    assert msg.timestamp == datetime.time(13, 10, 7, 999785, tzinfo=datetime.timezone.utc)
    assert msg.port_num == 2
    assert msg.event_num == 460
    assert msg.gps_week_num == 2181
    assert msg.gps_day_num == 5
    assert msg.leap_secs == 18
