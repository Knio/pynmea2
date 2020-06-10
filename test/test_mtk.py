import pynmea2


def test_mtk001():
    data = '$PMTK001,604,3*32'
    msg = pynmea2.parse(data)
    assert isinstance(msg, pynmea2.types.mtk.MTK001)
    assert msg.sentence_type == '001'
    assert msg.cmd == 604
    assert msg.flag == 3


def test_mtk220():
    sentence = pynmea2.ProprietarySentence('MTK', ('220', '200', ))
    assert str(sentence) == '$PMTK220,200*2C'
