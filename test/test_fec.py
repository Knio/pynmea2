import pytest

import pynmea2


def test_fecgpatt():
    data = "$PFEC,GPatt,294.7,-02.5,+00.4*45"
    msg = pynmea2.parse(data)
    assert type(msg) is pynmea2.fec.FECGPatt
    assert msg.manufacturer == 'FEC'
    assert msg.yaw == 294.7
    assert msg.pitch == -2.5
    assert msg.roll == 0.4
    assert msg.render() == data


def test_fecgphve():
    data = "$PFEC,GPhve,00.007,A*08"
    msg = pynmea2.parse(data)
    assert type(msg) is pynmea2.fec.FECGPhve
    assert msg.manufacturer == "FEC"
    assert msg.heave == 0.007
    assert msg.status == "A"
    assert msg.render() == data


@pytest.mark.parametrize("data,heave,status", [
    ("$PFEC,GPhve,-0.114,A*16", -0.114, "A"),
    ("$PFEC,GPhve,-0.114,V*01", -0.114, "V"),
    ("$PFEC,GPhve,-0.114,*57", -0.114, ""),
    ("$PFEC,GPhve,-0.114*7B", -0.114, ""),
    ("$PFEC,GPhve,,V*06", None, "V"),
    ("$PFEC,GPhve*50", None, ""),
    ("$PFEC,GPhve,not-a-number,V*11", "not-a-number", "V"),
    ("$PFEC,GPhve,00.000,X*16", 0.0, "X"),
])
def test_fecgphve_status(data, heave, status):
    msg = pynmea2.parse(data)
    original_fields = list(msg.data)

    assert type(msg) is pynmea2.fec.FECGPhve
    assert msg.status == status
    assert msg.heave == heave
    assert type(msg.heave) is type(heave)
    assert msg.data == original_fields
    assert msg.render() == data


def test_fecgphve_status_assignment():
    msg = pynmea2.parse("$PFEC,GPhve,-0.114,V*01")
    original_heave = msg.heave

    msg.status = "A"

    assert msg.data == ["", "GPhve", "-0.114", "A"]
    assert msg.heave == original_heave
    assert msg.render() == "$PFEC,GPhve,-0.114,A*16"
    assert pynmea2.parse(msg.render()).status == "A"


def test_fec_unknown_sentence_preserves_raw_fields():
    data = "$PFEC,GPimu,0.210,0.056,-0.023,0,-0.654,0.448,0.486,0,0*42"
    msg = pynmea2.parse(data)

    assert type(msg) is pynmea2.fec.FEC
    assert msg.data == ["", "GPimu", "0.210", "0.056", "-0.023", "0",
                        "-0.654", "0.448", "0.486", "0", "0"]
    with pytest.raises(AttributeError):
        msg.status
    assert msg.render() == data
