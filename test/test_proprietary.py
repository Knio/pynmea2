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

    # unimplemented sentence
    data = '$PSRF999,0,1200,8,1,1'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.srf.SRF


def test_grm():
    data = ' $PGRME,15.0,M,45.0,M,25.0,M*1C'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.grm.GRME

def test_tnl():
    data = '$PTNL,BPQ,224445.06,021207,3723.09383914,N,12200.32620132,W,EHT-5.923,M,5*60'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.tnl.TNLBPQ
    assert msg.datestamp == datetime.datetime(2007,12,2,0,0)
    assert msg.latitude == 37.384897319
    assert msg.longitude == -122.00543668866666


