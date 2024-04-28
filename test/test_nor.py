import datetime

import pynmea2


def test_norbt0():
    data = '$PNORBT0,1,040721,131335.3341,23.961,-48.122,-32.76800,10.00000,0.00,0x00000000*48'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.nor.NORBT0
    assert msg.manufacturer == 'NOR'
    assert msg.sentence_type == 'NORBT0'
    assert msg.beam == 1
    assert msg.datestamp == datetime.date(2021, 7, 4)
    assert msg.timestamp == datetime.time(13, 13, 35, 334100, tzinfo=datetime.timezone.utc)
    assert msg.dt1 == 23.961
    assert msg.dt2 == -48.122
    assert msg.bv == -32.76800
    assert msg.fom == 10.00000
    assert msg.dist == 0.00
    assert msg.stat == '0x00000000'
    assert msg.render() == data


def test_norbt4():
    data = '$PNORBT4,1.234,-1.234,1.234,23.4,12.34567,12.3*3D'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.nor.NORBT4
    assert msg.manufacturer == 'NOR'
    assert msg.sentence_type == 'NORBT4'
    assert msg.dt1 == 1.234
    assert msg.dt2 == -1.234
    assert msg.sound_speed == 1.234
    assert msg.dir == 23.4
    assert msg.fom == 12.34567
    assert msg.dist == 12.3
    assert msg.render() == data


def test_norbt7():
    data = '$PNORBT7,1452244916.7508,1.234,-1.234,0.1234,0.1234,0.1234,12.34,23.45,23.45,23.45,23.45*39'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.nor.NORBT7
    assert msg.manufacturer == 'NOR'
    assert msg.sentence_type == 'NORBT7'
    assert msg.timestamp == datetime.datetime(2016, 1, 8, 9, 21, 56, 750800)
    assert msg.dt1 == 1.234
    assert msg.dt2 == -1.234
    assert msg.vx == 0.1234
    assert msg.vy == 0.1234
    assert msg.vz == 0.1234
    assert msg.fom == 12.34
    assert msg.d1 == 23.45
    assert msg.d2 == 23.45
    assert msg.d3 == 23.45
    assert msg.d4 == 23.45
    assert msg.render() == data


def test_norbt9():
    data = '$PNORBT9,1452244916.7508,1.234,-1.234,0.1234,0.1234,0.1234,12.34,23.45,23.45,23.45,23.45,23.4,1567.8,1.2,12.3,0x000FFFFF*1E'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.nor.NORBT9
    assert msg.manufacturer == 'NOR'
    assert msg.sentence_type == 'NORBT9'
    assert msg.timestamp == datetime.datetime(2016, 1, 8, 9, 21, 56, 750800)
    assert msg.dt1 == 1.234
    assert msg.dt2 == -1.234
    assert msg.vx == 0.1234
    assert msg.vy == 0.1234
    assert msg.vz == 0.1234
    assert msg.fom == 12.34
    assert msg.d1 == 23.45
    assert msg.d2 == 23.45
    assert msg.d3 == 23.45
    assert msg.d4 == 23.45
    assert msg.battery_voltage == 23.4
    assert msg.sound_speed == 1567.8
    assert msg.pressure == 1.2
    assert msg.temp == 12.3
    assert msg.stat == '0x000FFFFF'
    assert msg.render() == data


def test_norwt4():
    data = '$PNORWT4,1.2345,-1.2345,1.234,23.4,12.34,12.3*1C'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.nor.NORWT4
    assert msg.manufacturer == 'NOR'
    assert msg.sentence_type == 'NORWT4'
    assert msg.dt1 == 1.2345
    assert msg.dt2 == -1.2345
    assert msg.sound_speed == 1.234
    assert msg.dir == 23.4
    assert msg.fom == 12.34
    assert msg.dist == 12.3
    assert msg.render() == data


def test_norwt7():
    data = '$PNORWT7,1452244916.7508,1.234,-1.234,0.1234,0.1234,0.1234,12.34,23.45,23.45,23.45,23.45*2C'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.nor.NORWT7
    assert msg.manufacturer == 'NOR'
    assert msg.sentence_type == 'NORWT7'
    assert msg.timestamp == datetime.datetime(2016, 1, 8, 9, 21, 56, 750800)
    assert msg.dt1 == 1.234
    assert msg.dt2 == -1.234
    assert msg.vx == 0.1234
    assert msg.vy == 0.1234
    assert msg.vz == 0.1234
    assert msg.fom == 12.34
    assert msg.d1 == 23.45
    assert msg.d2 == 23.45
    assert msg.d3 == 23.45
    assert msg.d4 == 23.45
    assert msg.render() == data


def test_norwt9():
    data = '$PNORWT9,1452244916.7508,1.234,-1.234,0.1234,0.1234,0.1234,12.34,23.45,23.45,23.45,23.45,23.4,1567.8,1.2,12.3,0x000FFFFF*0B'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.nor.NORWT9
    assert msg.manufacturer == 'NOR'
    assert msg.sentence_type == 'NORWT9'
    assert msg.timestamp == datetime.datetime(2016, 1, 8, 9, 21, 56, 750800)
    assert msg.dt1 == 1.234
    assert msg.dt2 == -1.234
    assert msg.vx == 0.1234
    assert msg.vy == 0.1234
    assert msg.vz == 0.1234
    assert msg.fom == 12.34
    assert msg.d1 == 23.45
    assert msg.d2 == 23.45
    assert msg.d3 == 23.45
    assert msg.d4 == 23.45
    assert msg.battery_voltage == 23.4
    assert msg.sound_speed == 1567.8
    assert msg.pressure == 1.2
    assert msg.temp == 12.3
    assert msg.stat == '0x000FFFFF'
    assert msg.render() == data


def test_nori1():
    data = '$PNORI1,4,123456,3,30,1.00,5.00,BEAM*5B'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.nor.NORI1
    assert msg.manufacturer == 'NOR'
    assert msg.sentence_type == 'NORI1'
    assert msg.it == 4
    assert msg.sn == 123456
    assert msg.nb == 3
    assert msg.nc == 30
    assert msg.bd == 1.00
    assert msg.cs == 5.00
    assert msg.cy == 'BEAM'
    assert msg.render() == data


def test_nors1():
    data = '$PNORS1,161109,132455,0,34000034,23.9,1500.0,123.4,0.02,45.6,0.02,23.4,0.02,123.456,0.02,24.56*51'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.nor.NORS1
    assert msg.manufacturer == 'NOR'
    assert msg.sentence_type == 'NORS1'
    assert msg.datestamp == datetime.date(2009, 11, 16)
    assert msg.timestamp == datetime.time(13, 24, 55, tzinfo=datetime.timezone.utc)
    assert msg.ec == 0
    assert msg.sc == '34000034'
    assert msg.battery_voltage == 23.9
    assert msg.sound_speed == 1500.0
    assert msg.heading == 123.4
    assert msg.heading_std == 0.02
    assert msg.pitch == 45.6
    assert msg.pitch_std == 0.02
    assert msg.roll == 23.4
    assert msg.roll_std == 0.02
    assert msg.pressure == 123.456
    assert msg.pressure_std == 0.02
    assert msg.temp == 24.56
    assert msg.render() == data


def test_nors4():
    data = '$PNORS4,23.6,1530.2,0.0,0.0,0.0,0.000,23.30*66'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.nor.NORS4
    assert msg.manufacturer == 'NOR'
    assert msg.sentence_type == 'NORS4'
    assert msg.battery_voltage == 23.6
    assert msg.sound_speed == 1530.2
    assert msg.heading == 0.0
    assert msg.pitch == 0.0
    assert msg.roll == 0.0
    assert msg.pressure == 0.0
    assert msg.temp == 23.30
    assert msg.render() == data


def test_norc1():
    data = '$PNORC1,161109,132455,3,11.0,0.332,0.332,0.332,0.332,78.9,78.9,78.9,78.9,78,78,78,78*56'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.nor.NORC1
    assert msg.manufacturer == 'NOR'
    assert msg.sentence_type == 'NORC1'
    assert msg.datetime == datetime.datetime(2009, 11, 16, 13, 24, 55, tzinfo=datetime.timezone.utc)
    assert msg.cn == 3
    assert msg.cp == 11.0
    assert msg.vx == 0.332
    assert msg.vy == 0.332
    assert msg.vz == 0.332
    assert msg.vz2 == 0.332
    assert msg.amp1 == 78.9
    assert msg.amp2 == 78.9
    assert msg.amp3 == 78.9
    assert msg.amp4 == 78.9
    assert msg.r1 == 78
    assert msg.r2 == 78
    assert msg.r3 == 78
    assert msg.r4 == 78
    assert msg.render() == data


def test_norc4():
    data = '$PNORC4,1.5,1.395,227.1,32,32*7A'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.nor.NORC4
    assert msg.manufacturer == 'NOR'
    assert msg.sentence_type == 'NORC4'
    assert msg.cp == 1.5
    assert msg.sp == 1.395
    assert msg.dir == 227.1
    assert msg.r == 32
    assert msg.amp == 32
    assert msg.render() == data


def test_norh4():
    data = '$PNORH4,161109,143459,0,204C0002*38'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.nor.NORH4
    assert msg.manufacturer == 'NOR'
    assert msg.sentence_type == 'NORH4'
    assert msg.datestamp == datetime.date(2009, 11, 16)
    assert msg.timestamp == datetime.time(14, 34, 59, tzinfo=datetime.timezone.utc)
    assert msg.ec == 0
    assert msg.sc == '204C0002'
    assert msg.render() == data


def test_nor_undefined():
    '''
    Test that non-NOR messages still fall back to the generic NOR type
    '''
    data = '$PNORTT3,XYZ,123'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.nor.NOR
    assert msg.manufacturer == 'NOR'
    assert msg.sentence_type == 'NORTT3'
    assert msg.data == ['XYZ', '123']
    assert msg.render(checksum=False) == data
