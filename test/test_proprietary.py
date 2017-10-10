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
    # class with no extra comma
    class TNLDG(pynmea2.tnl.TNL):
        fields = ()

    # raise Exception(TNL.sentence_types)
    # raise Exception(pynmea2.ProprietarySentence.sentence_types)

    data = "$PTNLDG,44.0,33.0,287.0,100,0,4,1,0,,,*3E"
    msg = pynmea2.parse(data)
    assert isinstance(msg, TNLDG)
    assert msg.data == ['DG', '44.0', '33.0', '287.0', '100', '0', '4', '1', '0', '', '', '']
    assert str(msg) == data


    # type with extra comma

    data = '$PTNL,PJT,NAD83(Conus),CaliforniaZone 4 0404*51'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.tnl.TNLPJT
    assert msg.manufacturer == 'TNL'
    assert msg.sentence_type == 'PJT'
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


def test_grm():
    data = ' $PGRME,15.0,M,45.0,M,25.0,M*1C'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.grm.GRME
    assert msg.sentence_type == 'GRME'
    assert msg.hpe == 15.0
    assert msg.hpe_unit == 'M'
    assert msg.vpe == 45.0
    assert msg.vpe_unit == 'M'
    assert msg.osepe == 25.0
    assert msg.osepe_unit == 'M'

def test_tnl():
    data = '$PTNL,BPQ,224445.06,021207,3723.09383914,N,12200.32620132,W,EHT-5.923,M,5*60'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.tnl.TNLBPQ
    assert msg.datestamp == datetime.date(2007,12,2)
    assert msg.latitude == 37.384897319
    assert msg.longitude == -122.00543668866666


def test_ubx00():
    data = '$PUBX,00,074440.00,4703.74203,N,00736.82976,E,576.991,D3,2.0,2.0,0.091,0.00,-0.032,,0.76,1.05,0.65,14,0,0*70'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.ubx.UBX00
    assert msg.timestamp == datetime.time(7, 44, 40)
    assert msg.latitude == 47.06236716666667
    assert msg.lat_dir == 'N'


def test_ubx03():
    data = '$PUBX,03,20,3,e,281,72,36,062,5,e,034,10,23,000,8,U,328,11,44,064,9,-,323,-2,,000,13,-,341,01,,000,16,U,307,45,49,064,18,e,144,18,,000,21,U,150,74,35,037,25,e,134,06,,000,27,U,271,20,52,064,29,U,074,36,36,063,31,U,209,26,37,040,120,e,210,31,,000,126,-,157,33,,000,66,U,036,19,34,015,67,e,090,20,22,000,68,-,136,00,,000,73,e,273,60,47,064,74,U,330,24,44,064,80,U,193,36,36,023*33'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.ubx.UBX03
    assert msg.num_sv == 20


def test_ubx04():
    data = '$PUBX,04,073824.00,131014,113903.99,1814,16,495176,342.504,21*18'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.ubx.UBX04
    assert msg.date == datetime.date(2014, 10, 13)
    assert msg.time == datetime.time(7, 38, 24)
    assert msg.clk_bias == 495176


def test_create():
    sentence = pynmea2.srf.SRF100('SRF', [
        '100', '%d' % 1,
        '%d' % 9600,
        '%d' % 7,
        '%d' % 1,
        '%d' % 0])
    data = sentence.render(checksum=True, dollar=True, newline=False)
    assert data == '$PSRF100,1,9600,7,1,0*02'
