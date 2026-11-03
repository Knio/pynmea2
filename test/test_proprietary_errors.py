"""Malformed proprietary dispatch must respect parser and stream errors."""

import pytest

import pynmea2


MANUFACTURERS = ('ASH', 'FEC', 'SXN', 'TNL', 'UBX', 'VTX')
VALID = '$GPGLL,4916.45,N,12311.12,W,225444,A'


def with_checksum(line):
    return line + '*%02X' % pynmea2.NMEASentence.checksum(line[1:])


@pytest.mark.parametrize('manufacturer', MANUFACTURERS)
@pytest.mark.parametrize('checked', (False, True))
def test_truncated_proprietary_parse_error(manufacturer, checked):
    line = '$P' + manufacturer
    if checked:
        line = with_checksum(line)
    with pytest.raises(pynmea2.ParseError) as raised:
        pynmea2.parse(line)
    assert isinstance(raised.value, ValueError)
    assert raised.value.args[0][1] == line


@pytest.mark.parametrize('manufacturer', MANUFACTURERS)
@pytest.mark.parametrize('errors', ('raise', 'yield', 'ignore'))
def test_truncated_proprietary_stream_policy(manufacturer, errors):
    reader = pynmea2.NMEAStreamReader(errors=errors)
    stream = reader.next('$P' + manufacturer + '\n' + VALID + '\n')
    if errors == 'raise':
        with pytest.raises(pynmea2.ParseError):
            list(stream)
    elif errors == 'yield':
        messages = list(stream)
        assert len(messages) == 2
        assert isinstance(messages[0], pynmea2.ParseError)
        assert isinstance(messages[1], pynmea2.GLL)
    else:
        messages = list(stream)
        assert len(messages) == 1
        assert isinstance(messages[0], pynmea2.GLL)


@pytest.mark.parametrize('errors', ('yield', 'ignore'))
def test_chunked_truncation_preserves_following_message(errors):
    reader = pynmea2.NMEAStreamReader(errors=errors)
    assert list(reader.next('$PFE')) == []
    first = list(reader.next('C\r\n' + VALID[:8]))
    assert len(first) == (1 if errors == 'yield' else 0)
    if first:
        assert isinstance(first[0], pynmea2.ParseError)
    messages = list(reader.next(VALID[8:] + '\r\n'))
    assert len(messages) == 1
    assert isinstance(messages[0], pynmea2.GLL)


@pytest.mark.parametrize('manufacturer', MANUFACTURERS)
def test_unknown_proprietary_subtype_still_round_trips(manufacturer):
    line = '$P' + manufacturer + ',UNRECOGNIZED,raw,value'
    message = pynmea2.parse(line)
    assert message.manufacturer == manufacturer
    assert message.data == ['', 'UNRECOGNIZED', 'raw', 'value']
    assert message.render(checksum=False) == line


@pytest.mark.parametrize('line', ('$PLCJ', '$PZZZ', VALID))
def test_existing_short_fallback_and_talker_behavior(line):
    assert pynmea2.parse(line).render(checksum=False) == line


@pytest.mark.parametrize('manufacturer', MANUFACTURERS)
def test_checksum_rejection_precedes_proprietary_dispatch(manufacturer):
    line = '$P' + manufacturer
    with pytest.raises(pynmea2.ChecksumError):
        pynmea2.parse(line, checksums='required')
    incorrect = line + '*%02X' % (
        pynmea2.NMEASentence.checksum(line[1:]) ^ 0xff)
    with pytest.raises(pynmea2.ChecksumError):
        pynmea2.parse(incorrect)
