import pynmea2
from pynmea2.types.proprietary.anz import ANZRSI


def test_ANZRSI_maps_named_fields_and_keeps_sentence_identifier():
    sentence = '$PANZRSI,65,0.0,6.7,S,0'

    msg = pynmea2.parse(sentence)

    assert isinstance(msg, ANZRSI)
    assert msg.sentence_id == 'RSI'
    assert msg.source_id == '65'
    assert msg.rudder_order == '0.0'
    assert msg.rudder_actual == '6.7'
    assert msg.status == 'S'
    assert msg.steering_position == '0'
    assert msg.render(checksum=False) == sentence


def test_ANZ_dispatches_using_first_nonempty_sentence_identifier():
    sentence = '$PANZ,,RSI,65,0.0,6.7,S,0'

    msg = pynmea2.parse(sentence)

    assert isinstance(msg, ANZRSI)
    assert msg.manufacturer == 'ANZ'
    assert msg.data == ['RSI', '65', '0.0', '6.7', 'S', '0']
    assert msg.sentence_id == 'RSI'
    assert msg.source_id == '65'
    assert msg.rudder_order == '0.0'
    assert msg.rudder_actual == '6.7'
    assert msg.status == 'S'
    assert msg.steering_position == '0'
    assert msg.render(checksum=False) == sentence


def test_ANZ_without_sentence_identifier_keeps_raw_data():
    sentence = '$PANZ,,'

    msg = pynmea2.parse(sentence)

    assert type(msg) == pynmea2.anz.ANZ
    assert msg.data == ['', '', '']
    assert msg.render(checksum=False) == sentence
