import pynmea2
import datetime

def test_proprietary_1():
    # A sample proprietary sentence from a LCJ Capteurs
    # anemometer.
    data = "$PLCJ,5F01,66FC,AA,9390,6373"
    msg = pynmea2.parse(data)
    assert msg.manufacturer == "LCJ"
    assert msg.data == ['','5F01','66FC','AA','9390','6373']
    assert msg.render(checksum=False) == data


def test_proprietary_2():
    # A sample proprietary sentence from a LCJ Capteurs anemometer.
    # Note: This sample is the main reason why we can't assume
    #       anything about the content of the proprietary sentences
    #       due to the lack of a comma after the manufacturer ID and
    #       extra comma at the end.
    data = "$PLCJE81B8,64A0,2800,2162,0E,"
    msg = pynmea2.parse(data)
    assert msg.manufacturer == 'LCJ'
    assert msg.data == ['E81B8', '64A0', '2800', '2162', '0E', '']
    assert repr(msg) == "<ProprietarySentence() data=['E81B8', '64A0', '2800', '2162', '0E', '']>"
    assert msg.render(checksum=False) == data


def test_proprietary_3():
    # A sample proprietary sentence from a Magellan device
    # (via <http://www.gpsinformation.org/dale/nmea.htm#proprietary>).
    data = "$PMGNST,02.12,3,T,534,05.0,+03327,00*40"
    msg = pynmea2.parse(data)
    assert msg.manufacturer == 'MGN'
    assert msg.data == ['ST','02.12','3','T','534','05.0','+03327','00']
    assert msg.render() == data


def test_extra_comma():
    # extra comma after name
    data = "$PTNL,AVR,212604.30,+52.1800,Yaw,,,-0.0807,Roll,12.579,3,1.4,16*21"
    msg = pynmea2.parse(data)
    assert msg.manufacturer == 'TNL'
    assert msg.data == ['', 'AVR','212604.30','+52.1800','Yaw','','','-0.0807','Roll','12.579','3','1.4','16']
    assert msg.render() == data


def test_proprietary_type():
    class ABC(pynmea2.ProprietarySentence):
        fields = (
            ('Empty', '_'),
            ('First', 'a'),
            ('Second', 'b'),
        )

    data = '$PABC,1,2*13'
    msg = pynmea2.parse(data)
    assert isinstance(msg, ABC)
    assert msg.manufacturer == 'ABC'
    assert msg.a == '1'
    assert msg.b == '2'
    assert repr(msg) == "<ABC(_='', a='1', b='2')>"
    assert str(msg) == data


def test_proprietary_with_comma():
    data = "$PTNLDG,44.0,33.0,287.0,100,0,4,1,0,,,*3E"
    msg = pynmea2.parse(data)
    assert isinstance(msg, pynmea2.tnl.TNLDG)
    assert msg.data == ['DG', '44.0', '33.0', '287.0', '100', '0', '4', '1', '0', '', '', '']
    assert str(msg) == data

    # type with extra comma

    data = '$PTNL,PJT,NAD83(Conus),CaliforniaZone 4 0404*51'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.tnl.TNLPJT
    assert msg.manufacturer == 'TNL'
    assert msg.type == 'PJT'
    assert msg.coord_name == 'NAD83(Conus)'
    assert msg.project_name == 'CaliforniaZone 4 0404'
    assert str(msg) == data


def test_srf():
    # implemented sentence
    data = '$PSRF100,0,1200,8,1,1'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.srf.SRF100
    assert msg.sentence_type == 'SRF100'
    assert msg.protocol == '0'
    assert msg.baud == '1200'
    assert msg.databits == '8'
    assert msg.stopbits == '1'
    assert msg.parity == '1'

    # unimplemented sentence
    data = '$PSRF999,0,1200,8,1,1'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.srf.SRF
    assert msg.render(checksum=False) == data


def test_grm():
    data = '$PGRME,15.0,M,45.0,M,25.0,M*1C'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.grm.GRME
    assert msg.sentence_type == 'GRME'
    assert msg.hpe == 15.0
    assert msg.hpe_unit == 'M'
    assert msg.vpe == 45.0
    assert msg.vpe_unit == 'M'
    assert msg.osepe == 25.0
    assert msg.osepe_unit == 'M'
    assert msg.render() == data


def test_tnl():
    data = '$PTNL,BPQ,224445.06,021207,3723.09383914,N,12200.32620132,W,EHT-5.923,M,5*60'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.tnl.TNLBPQ
    assert msg.datestamp == datetime.date(2007,12,2)
    assert msg.latitude == 37.384897319
    assert msg.longitude == -122.00543668866666
    assert msg.render() == data


def test_ubx00():
    data = '$PUBX,00,074440.00,4703.74203,N,00736.82976,E,576.991,D3,2.0,2.0,0.091,0.00,-0.032,,0.76,1.05,0.65,14,0,0*70'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.ubx.UBX00
    assert msg.identifier() == 'PUBX'
    assert msg.ubx_type == '00'
    assert msg.timestamp == datetime.time(7, 44, 40, tzinfo=datetime.timezone.utc)
    assert msg.latitude == 47.06236716666667
    assert msg.lat_dir == 'N'
    assert msg.render() == data


def test_ubx03():
    data = '$PUBX,03,20,3,e,281,72,36,062,5,e,034,10,23,000,8,U,328,11,44,064,9,-,323,-2,,000,13,-,341,01,,000,16,U,307,45,49,064,18,e,144,18,,000,21,U,150,74,35,037,25,e,134,06,,000,27,U,271,20,52,064,29,U,074,36,36,063,31,U,209,26,37,040,120,e,210,31,,000,126,-,157,33,,000,66,U,036,19,34,015,67,e,090,20,22,000,68,-,136,00,,000,73,e,273,60,47,064,74,U,330,24,44,064,80,U,193,36,36,023*33'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.ubx.UBX03
    assert msg.num_sv == 20
    assert msg.render() == data


def test_ubx04():
    data = '$PUBX,04,073824.00,131014,113903.99,1814,16,495176,342.504,21*18'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.ubx.UBX04
    assert msg.date == datetime.date(2014, 10, 13)
    assert msg.time == datetime.time(7, 38, 24, tzinfo=datetime.timezone.utc)
    assert msg.clk_bias == 495176
    assert msg.render() == data


def test_create():
    sentence = pynmea2.srf.SRF100('SRF', [
        '100', '%d' % 1,
        '%d' % 9600,
        '%d' % 7,
        '%d' % 1,
        '%d' % 0])
    data = sentence.render(checksum=True, dollar=True, newline=False)
    assert data == '$PSRF100,1,9600,7,1,0*02'


def test_unknown_sentence():
    data = 'PZZZABC,1,2,3'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.ProprietarySentence
    assert msg.manufacturer == 'ZZZ'
    assert msg.data == ['ABC', '1', '2', '3']
    assert msg.render(checksum=False, dollar=False) == data


def test_proprietary_VTX_0002():
    # A sample proprietary sentence from a Vectronix device (laser distance)
    data = "$PVTX,0002,181330,00005.22,M,262.518,T,-01.967,09.358,W*7E"
    msg = pynmea2.parse(data)
    assert msg.manufacturer == 'VTX'
    assert msg.dist == 5.22
    assert msg.direction == 262.518
    assert msg.va == -1.967
    assert msg.render() == data


def test_proprietary_VTX_0012():
    # A sample proprietary sentence from a Vectronix device (target position)
    data = "$PVTX,0012,177750,3348.5861,N,10048.5861,W,00045.2,M,038.8,M*22"
    msg = pynmea2.parse(data)
    assert msg.manufacturer == 'VTX'
    assert msg.latitude == 33.80976833333333
    assert msg.longitude == -100.80976833333334
    assert msg.altitude == 45.2
    assert msg.gain == 38.8
    assert msg.render() == data


def test_proprietary_GRMW():
    # A sample proprietary Garmin Waypoint sentence, generated by DIREWOLF
    data = "$PGRMW,AC7FD-1,,000A,AC7FD local DIGI U=12.5V|T=23.9C*1A"
    msg = pynmea2.parse(data)
    assert msg.manufacturer == 'GRM'
    assert msg.wname == 'AC7FD-1'
    assert msg.altitude == None
    assert msg.symbol == '000A'
    assert msg.comment == 'AC7FD local DIGI U=12.5V|T=23.9C'


def test_proprietary_MGNWPL():
    # A sample proprietary Magellan Waypoint sentence, generated by DIREWOLF
    data = "$PMGNWPL,4531.7900,N,12253.4800,W,,M,AC7FD-1,AC7FD local DIGI U=12.5V|T=23.9C,c*46"
    msg = pynmea2.parse(data)
    assert msg.manufacturer == 'MGN'
    assert msg.lat =='4531.7900'
    assert msg.lat_dir == 'N'
    assert msg.lon == '12253.4800'
    assert msg.lon_dir == 'W'
    assert msg.altitude == None
    assert msg.altitude_unit == 'M'
    assert msg.wname == 'AC7FD-1'
    assert msg.comment == 'AC7FD local DIGI U=12.5V|T=23.9C'
    assert msg.icon == 'c'
    assert msg.latitude == 45.529833333333336
    assert msg.longitude == -122.89133333333334


def test_KWDWPL():
    # A sample proprietary Kenwood Waypoint sentence, generated by DIREWOLF
    data = "$PKWDWPL,053125,V,4531.7900,N,12253.4800,W,,,200320,,AC7FD-1,/-*10"
    msg = pynmea2.parse(data)
    assert msg.manufacturer == "KWD"
    assert msg.timestamp == datetime.time(5, 31, 25, tzinfo=datetime.timezone.utc)
    assert msg.status == 'V'
    assert msg.is_valid == False
    assert msg.lat == '4531.7900'
    assert msg.lat_dir == 'N'
    assert msg.lon == '12253.4800'
    assert msg.lon_dir == 'W'
    assert msg.sog == None
    assert msg.cog == None
    assert msg.datestamp == datetime.date(2020, 3, 20)
    assert msg.datetime == datetime.datetime(2020, 3, 20, 5, 31, 25, tzinfo=datetime.timezone.utc)
    assert msg.altitude == None
    assert msg.wname == 'AC7FD-1'
    assert msg.ts == '/-'
    assert msg.latitude == 45.529833333333336
    assert msg.longitude == -122.89133333333334

def test_PKNDS():
    # A sample proprietary Kenwood sentence used for GPS data communications in NEXEDGE Digital
    data = "$PKNDS,114400,A,4954.1450,N,11923.6043,W,001.4,356.8,130223,19.20,W00,U00002,207,00,*2E"
    msg = pynmea2.parse(data)
    assert msg.manufacturer == "KND"
    assert msg.timestamp == datetime.time(11, 44, 00, tzinfo=datetime.timezone.utc)
    assert msg.status == 'A'
    assert msg.is_valid == True
    assert msg.lat == '4954.1450'
    assert msg.lat_dir == 'N'
    assert msg.lon == '11923.6043'
    assert msg.lon_dir == 'W'
    assert msg.datestamp == datetime.date(2023, 2, 13)
    assert msg.datetime == datetime.datetime(2023, 2, 13, 11, 44, 00, tzinfo=datetime.timezone.utc)
    assert msg.senderid == 'U00002'
    assert msg.senderstatus  == 207
    assert msg.latitude == 49.90241666666667
    assert msg.longitude == -119.393405

def test_PKNSH():
    # A sample proprietary Kenwood sentence used for GPS data communications in NEXEDGE Digital
    data = "$PKNSH,4954.1450,N,11923.6043,W,114400,A,U00002,*44"
    msg = pynmea2.parse(data)
    assert msg.manufacturer == "KNS"
    assert msg.timestamp == datetime.time(11, 44, 00, tzinfo=datetime.timezone.utc)
    assert msg.status == 'A'
    assert msg.is_valid == True
    assert msg.lat == '4954.1450'
    assert msg.lat_dir == 'N'
    assert msg.lon == '11923.6043'
    assert msg.lon_dir == 'W'
    assert msg.senderid == 'U00002'
    assert msg.latitude == 49.90241666666667
    assert msg.longitude == -119.393405

def test_PKLDS():
    # A sample proprietary Kenwood sentence used for GPS data communications in FleetSync II signaling
    data = "$PKLDS,122434,A,4954.1474,N,11923.6044,W,001.1,194.9,130223,19.20,W00,100,1001,80,00,*60"
    msg = pynmea2.parse(data)
    assert msg.manufacturer == "KLD"
    assert msg.timestamp == datetime.time(12, 24, 34, tzinfo=datetime.timezone.utc)
    assert msg.status == 'A'
    assert msg.is_valid == True
    assert msg.lat == '4954.1474'
    assert msg.lat_dir == 'N'
    assert msg.lon == '11923.6044'
    assert msg.lon_dir == 'W'
    assert msg.datestamp == datetime.date(2023, 2, 13)
    assert msg.datetime == datetime.datetime(2023, 2, 13, 12, 24, 34, tzinfo=datetime.timezone.utc)
    assert msg.senderid == '1001'
    assert msg.fleet == 100
    assert msg.latitude == 49.902456666666666
    assert msg.longitude == -119.39340666666666

def test_PKLSH():
    # A sample proprietary Kenwood sentence used for GPS data communications in FleetSync II signaling
    data = "$PKLSH,4954.1474,N,11923.6044,W,122434,A,100,1001,*3F"
    msg = pynmea2.parse(data)
    assert msg.manufacturer == "KLS"
    assert msg.timestamp == datetime.time(12, 24, 34, tzinfo=datetime.timezone.utc)
    assert msg.status == 'A'
    assert msg.is_valid == True
    assert msg.lat == '4954.1474'
    assert msg.lat_dir == 'N'
    assert msg.lon == '11923.6044'
    assert msg.lon_dir == 'W'
    assert msg.senderid == '1001'
    assert msg.fleet == 100
    assert msg.latitude == 49.902456666666666
    assert msg.longitude == -119.39340666666666
