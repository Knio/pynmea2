import pynmea2


def test_fecgpatt():
    data = "$PFEC,GPatt,294.7,-02.5,+00.4*45"
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.fec.FECGPatt
    assert msg.manufacturer == 'FEC'
    assert msg.yaw == 294.7
    assert msg.pitch == -2.5
    assert msg.roll == 0.4
    assert msg.render() == data


def test_fecgphve():
    data = "$PFEC,GPhve,00.007,A*08"
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.fec.FECGPhve
    assert msg.manufacturer == "FEC"
    assert msg.heave == 0.007
    assert msg.render() == data
