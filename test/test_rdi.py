import pynmea2

def test_rdid():
    data = '$PRDID,-1.31,7.81,47.31*68'
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.rdi.RDID
    assert msg.manufacturer == 'RDI'
    assert msg.subtype == 'D'
    assert msg.pitch == -1.31
    assert msg.roll == 7.81
    assert msg.heading == 47.31
    assert msg.render() == data
