import pynmea2


def test_follower_1():
    data = "$PLCJ,5F01,66FC,AA,9390,6373"
    msg = pynmea2.parse(data)
    assert msg.manufacturer == 'LCJ'


def test_follower_2():
    # missing comma in front, extra comma at end
    data = "$PLCJE81B8,64A0,2800,2162,0E,"
    msg = pynmea2.parse(data)
    assert msg.manufacturer == 'LCJ'
    assert msg.data == ['E81B8', '64A0', '2800', '2162', '0E', '']
    assert repr(msg) == "<ProprietarySentence() data=['E81B8', '64A0', '2800', '2162', '0E', '']>"


def test_follower_3():
    data = "$PMGNST,02.12,3,T,534,05.0,+03327,00*40"
    msg = pynmea2.parse(data)
    assert msg.manufacturer == 'MGN'


def test_extra_comma():
    # extra comma after name
    data = "$PTNL,AVR,212604.30,+52.1800,Yaw,,,-0.0807,Roll,12.579,3,1.4,16*21"
    msg = pynmea2.parse(data)
    assert msg.manufacturer == 'TNL'
    assert msg.data == ['AVR','212604.30','+52.1800','Yaw','','','-0.0807','Roll','12.579','3','1.4','16']


def test_proprietary():
    class ABC(pynmea2.ProprietarySentence):
        fields = (
            ('First', 'a'),
            ('Second', 'b'),
        )

    data = '$PABC,1,2*13'
    msg = pynmea2.parse(data)
    assert isinstance(msg, ABC)
    assert msg.manufacturer == 'ABC'
    assert msg.a == '1'
    assert msg.b == '2'
    assert repr(msg) == "<ABC(a='1', b='2')>"
