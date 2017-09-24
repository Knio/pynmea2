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
