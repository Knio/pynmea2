import pynmea2


def test_follower_1():
    data = "$PLCJ,5F01,66FC,AA,9390,6373"
    msg = pynmea2.parse(data)
    assert msg.manufacturer == 'LCJ'
    assert msg.render(checksum=False) == data


def test_follower_2():
    # missing comma in front, extra comma at end
    data = "$PLCJE81B8,64A0,2800,2162,0E,"
    msg = pynmea2.parse(data)
    assert msg.manufacturer == 'LCJ'
    assert msg.data == ['E81B8', '64A0', '2800', '2162', '0E', '']
    assert repr(msg) == "<ProprietarySentence() data=['E81B8', '64A0', '2800', '2162', '0E', '']>"
    assert msg.render(checksum=False) == data


def test_follower_3():
    data = "$PMGNST,02.12,3,T,534,05.0,+03327,00*40"
    msg = pynmea2.parse(data)
    assert msg.manufacturer == 'MGN'
    assert msg.render() == data

def test_extra_comma():
    # extra comma after name
    data = "$PTNL,AVR,212604.30,+52.1800,Yaw,,,-0.0807,Roll,12.579,3,1.4,16*21"
    msg = pynmea2.parse(data)
    assert msg.manufacturer == 'TNL'
    assert msg.data == ['', 'AVR','212604.30','+52.1800','Yaw','','','-0.0807','Roll','12.579','3','1.4','16']
    assert msg.render() == data

def test_proprietary():
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
    class TNL(pynmea2.ProprietarySentence):
        sentence_types = {}
        def __new__(_cls, manufacturer, data):
            '''
            Return the correct sentence type based on the first field
            '''
            sentence_type = data[0] or data[1]
            cls = _cls.sentence_types[sentence_type]
            return super(TNL, cls).__new__(cls)

        def __init__(self, manufacturer, data):
            self.sentence_type = data[0] or data[1]
            super(TNL, self).__init__(manufacturer, data)

    # class with no extra comma
    class DG(TNL):
        fields = ()

    # raise Exception(TNL.sentence_types)
    # raise Exception(pynmea2.ProprietarySentence.sentence_types)

    data = "$PTNLDG,44.0,33.0,287.0,100,0,4,1,0,,,*3E"
    msg = pynmea2.parse(data)
    assert isinstance(msg, DG)
    assert msg.data == ['DG', '44.0', '33.0', '287.0', '100', '0', '4', '1', '0', '', '', '']
    assert str(msg) == data


    # type with extra comma
    class PJT(TNL):
        fields = (
            ('Empty', '_'),
            ('Sentence Type', 'type'),
            ('Coordinate System', 'coord_name'),
            ('Project Name', 'project_name'),
        )

    data = '$PTNL,PJT,NAD83(Conus),CaliforniaZone 4 0404*51'
    msg = pynmea2.parse(data)
    assert isinstance(msg, PJT)
    assert msg.manufacturer == 'TNL'
    assert msg.sentence_type == 'PJT'
    assert msg.coord_name == 'NAD83(Conus)'
    assert msg.project_name == 'CaliforniaZone 4 0404'
    assert str(msg) == data
