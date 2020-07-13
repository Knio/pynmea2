import pynmea2


def test_cerulean():
    data = '$USRTH,358.5,1.5,2.8,142.8,52.8,37.2,2.8,-0.6,1.9,178.1,271.9,16*49'
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.types.talker.RTH
    assert msg.sentence_type == 'RTH'
    assert msg.talker == 'US'
    assert msg.ab == 358.5
    assert msg.ac == 1.5
    assert msg.ae == 2.8
    assert msg.sr == 142.8
    assert msg.tb == 52.8
    assert msg.cb == 37.2
    assert msg.te == 2.8
    assert msg.er == -0.6
    assert msg.ep == 1.9
    assert msg.ey == 178.1
    assert msg.ch == 271.9
    assert msg.db == 16.0
