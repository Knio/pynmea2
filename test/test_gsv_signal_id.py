"""NMEA 4.10 GSV signal IDs follow a variable number of satellite groups."""
import pytest
import pynmea2


@pytest.mark.parametrize('sentence,signal_id,last_prn,last_value,next_prn', [
    ('$GPGSV,3,1,11,04,06,317,21,05,17,057,34,09,00,348,,12,01,118,,1*68', '1', 'sv_prn_num_4', '12', None),
    ('$GPGSV,3,3,11,26,49,301,08,29,58,056,37,31,50,235,22,1*55', '1', 'sv_prn_num_3', '31', 'sv_prn_num_4'),
    ('$GPGSV,3,3,09,25,,,40,1*6E', '1', 'sv_prn_num_1', '25', 'sv_prn_num_2'),
    ('$GAGSV,1,1,00,2*76', '2', None, None, 'sv_prn_num_1'),
])
def test_reported_sentences(sentence, signal_id, last_prn, last_value, next_prn):
    message = pynmea2.parse(sentence, check=True)
    if last_prn:
        assert getattr(message, last_prn) == last_value
    if next_prn:
        assert getattr(message, next_prn) == ''
    assert message.signal_id == signal_id
    assert str(message) == sentence


@pytest.mark.parametrize('groups', range(5))
@pytest.mark.parametrize('signal_id', [None, '', '1', '7'])
def test_legacy_and_extended_lengths(groups, signal_id):
    data = ['1', '1', str(groups)] + ['25', '45', '120', '40'] * groups
    if signal_id is not None:
        data.append(signal_id)
    message = pynmea2.GSV('GP', 'GSV', data)
    reparsed = pynmea2.parse(str(message), check=True)
    assert reparsed.data == data
    assert reparsed.signal_id == (signal_id or '')
    for i in range(1, 5):
        assert getattr(reparsed, 'sv_prn_num_%d' % i) == ('25' if i <= groups else '')


def test_modifying_existing_satellite_preserves_signal_id():
    message = pynmea2.parse('$GPGSV,3,3,09,25,,,40,1*6E')
    message.sv_prn_num_1 = '26'
    reparsed = pynmea2.parse(str(message), check=True)
    assert reparsed.sv_prn_num_1 == '26'
    assert reparsed.signal_id == '1'


def test_missing_satellite_cannot_overwrite_signal_id():
    message = pynmea2.parse('$GPGSV,3,3,09,25,,,40,1*6E')
    with pytest.raises(IndexError):
        message.sv_prn_num_2 = '26'
    assert str(message) == '$GPGSV,3,3,09,25,,,40,1*6E'
