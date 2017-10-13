import pynmea2


def test_sxn20():
    data = '$PSXN,20,0,0,0,0*3B'
    msg = pynmea2.parse(data)
    assert isinstance(msg, pynmea2.types.sxn.SXN20)
    assert msg.message_type == 20
    assert msg.horiz_qual == 0
    assert msg.hgt_qual == 0
    assert msg.head_qual == 0
    assert msg.rp_qual == 0
    assert msg.render() == data


def test_sxn23():
    data = '$PSXN,23,0.30,-0.97,298.57,0.13*1B'
    msg = pynmea2.parse(data)
    assert isinstance(msg, pynmea2.types.sxn.SXN23)
    assert msg.message_type == 23
    assert msg.roll == 0.30
    assert msg.pitch == -0.97
    assert msg.head == 298.57
    assert msg.heave == 0.13
    assert msg.render() == data
