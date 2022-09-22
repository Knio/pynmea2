import datetime

import pynmea2


def test_ashrltn():
    data = '$PASHR,LTN,3*3D'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.ash.ASHRLTN
    assert msg.manufacturer == 'ASH'
    assert msg.subtype == 'LTN'
    assert msg.latency == 3
    assert msg.render() == data


def test_ashratt():
    data = '$PASHR,130533.620,0.311,T,-80.467,-1.395,0.25,0.066,0.067,0.215,2,3*12'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.ash.ASHRATT
    assert msg.data == ['R', '130533.620', '0.311', 'T', '-80.467', '-1.395', '0.25', '0.066', '0.067', '0.215', '2', '3']
    assert msg.manufacturer == 'ASH'
    assert msg.timestamp == datetime.time(13, 5, 33, 620000, tzinfo=datetime.timezone.utc)
    assert msg.true_heading == 0.311
    assert msg.is_true_heading == 'T'
    assert msg.roll == -80.467
    assert msg.pitch == -1.395
    assert msg.heave == 0.25
    assert msg.roll_accuracy == 0.066
    assert msg.pitch_accuracy == 0.067
    assert msg.heading_accuracy == 0.215
    assert msg.aiding_status == 2
    assert msg.imu_status == 3
    assert msg.render() == data


def test_ashratt_with_2_vs_3_decimal_timestamp():
    msg_3 = pynmea2.parse('$PASHR,130533.620,0.311,T,-80.467,-1.395,,0.066,0.067,0.215,2,3*0B')
    msg_2 = pynmea2.parse('$PASHR,130533.62,0.311,T,-80.467,-1.395,,0.066,0.067,0.215,2,3*3B')

    assert msg_3.timestamp == msg_2.timestamp


def test_ash_undefined():
    '''
    Test that non-ATT messages still fall back to the generic ASH type
    '''
    data = '$PASHR,XYZ,123'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.ash.ASH
    assert msg.manufacturer == 'ASH'
    # assert msg.sentence_type == 'XYZ'
    assert msg.data == ['R', 'XYZ', '123']
    assert msg.render(checksum=False) == data
