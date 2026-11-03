from __future__ import unicode_literals

from io import StringIO

import pytest

import pynmea2


VALID = ('$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,'
         '100.00,M,-33.9,M,,0000*6D\n')
MISSING = VALID.split('*')[0] + '\n'
INVALID = VALID.split('*')[0] + '*00\n'
MALFORMED = 'not an NMEA sentence\n'


@pytest.mark.parametrize('errors', ['raise', 'yield', 'ignore'])
@pytest.mark.parametrize(
    'checksums', ['check', 'required', 'my_data_is_corrupt'])
@pytest.mark.parametrize('kind', ['valid', 'missing', 'invalid', 'malformed'])
def test_stream_checksum_policy(checksums, errors, kind):
    sentences = {'valid': VALID, 'missing': MISSING,
                 'invalid': INVALID, 'malformed': MALFORMED}
    expected_error = None
    if kind == 'malformed':
        expected_error = pynmea2.ParseError
    elif ((kind == 'missing' and checksums == 'required') or
          (kind == 'invalid' and checksums != 'my_data_is_corrupt')):
        expected_error = pynmea2.ChecksumError

    reader = pynmea2.NMEAStreamReader(errors=errors, checksums=checksums)
    # A valid second message checks that error modes retain stream ordering.
    batch = reader.next(sentences[kind] + VALID)
    if expected_error is not None and errors == 'raise':
        with pytest.raises(expected_error):
            list(batch)
        return

    messages = list(batch)
    if expected_error is not None and errors == 'yield':
        assert len(messages) == 2
        assert type(messages[0]) is expected_error
        messages = messages[1:]
    elif expected_error is not None:
        assert len(messages) == 1
    else:
        assert len(messages) == 2

    for message in messages:
        assert isinstance(message, pynmea2.GGA)
        assert message.data == ['184353.07', '1929.045', 'S', '02410.506',
                                'E', '1', '04', '2.6', '100.00', 'M',
                                '-33.9', 'M', '', '0000']


@pytest.mark.parametrize('errors', ['raise', 'yield', 'ignore'])
def test_default_stream_checksum_policy(errors):
    reader = pynmea2.NMEAStreamReader(errors=errors)
    if errors == 'raise':
        with pytest.raises(pynmea2.ChecksumError):
            list(reader.next(INVALID))
    else:
        messages = list(reader.next(INVALID + MISSING))
        if errors == 'yield':
            assert len(messages) == 2
            assert isinstance(messages[0], pynmea2.ChecksumError)
        else:
            assert len(messages) == 1
        assert isinstance(messages[-1], pynmea2.GGA)


def test_stream_checksum_policy_with_chunks_and_file():
    reader = pynmea2.NMEAStreamReader(checksums='my_data_is_corrupt')
    assert list(reader.next(INVALID[:12])) == []
    messages = list(reader.next(INVALID[12:] + VALID))
    assert len(messages) == 2
    assert all(isinstance(message, pynmea2.GGA) for message in messages)

    # Existing positional stream/errors arguments retain their meaning.
    reader = pynmea2.NMEAStreamReader(
        StringIO(INVALID), 'raise', checksums='my_data_is_corrupt')
    assert len(list(reader.next())) == 1
    assert list(reader.next()) == []


@pytest.mark.parametrize('checksums', ['bad', None, False])
def test_bad_stream_checksum_policy(checksums):
    with pytest.raises(ValueError):
        pynmea2.NMEAStreamReader(checksums=checksums)
