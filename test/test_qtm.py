import pynmea2

def test_pqtmverno():
    """Test PQTMVERNO with successful version response."""
    data = "$PQTMVERNO,LC29HAANR01A04S,2022/11/04,16:39:48*34"
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.qtm.QTMVERNO
    assert msg.sentence_type == "VERNO"
    assert msg.version == "LC29HAANR01A04S"
    assert msg.build_date == "2022/11/04"
    assert msg.build_time == "16:39:48"

def test_pqtmsavepar():
    """Test PQTMSAVEPAR with OK status."""
    data = "$PQTMSAVEPAR,OK*72"
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.qtm.QTMSAVEPAR
    assert msg.status == "OK"

def test_pqtmrestorepar():
    """Test PQTMRESTOREPAR with OK status."""
    data = "$PQTMRESTOREPAR,OK*3B"
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.qtm.QTMRESTOREPAR
    assert msg.status == "OK"

def test_qtmepe():
    """Test QTMEPE with example data."""
    data = "$PQTMEPE,2,3.393,3.476,12.713,4.857,13.609*5D"
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.qtm.QTMEPE
    assert msg.sentence_type == "EPE"
    assert msg.msg_ver == "2"
    assert msg.epe_north == "3.393"
    assert msg.epe_east == "3.476"
    assert msg.epe_down == "12.713"
    assert msg.epe_2d == "4.857"
    assert msg.epe_3d == "13.609"

def test_pqtmcfggeofence():
    """Test PQTMCFGGEOFENCE with a successful response."""
    data = "$PQTMCFGGEOFENCE,OK,1,1,0,2,30.123,-90.123,5.0,-91.456,31.789,-92.012,32.000,-93.000*41"
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.qtm.QTMCFGGEOFENCE
    assert msg.sentence_type == "CFGGEOFENCE"
    assert msg.status == "OK"
    assert msg.index == "1"
    assert msg.enabled == "1"
    assert msg.reserved == "0"
    assert msg.shape == "2"
    assert msg.lat0 == "30.123"
    assert msg.lon0 == "-90.123"
    assert msg.lat1_or_radius == "5.0"
    assert msg.lon1 == "-91.456"
    assert msg.lat2 == "31.789"
    assert msg.lon2 == "-92.012"
    assert msg.lat3 == "32.000"
    assert msg.lon3 == "-93.000"

def test_pqtmgeofencestatus():
    """Test PQTMGEOFENCESTATUS with example data."""
    data = "$PQTMGEOFENCESTATUS,1,093444.000,2,0,0,1*28"
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.qtm.QTMGEOFENCESTATUS
    assert msg.sentence_type == "GEOFENCESTATUS"
    assert msg.msg_ver == "1"
    assert msg.time == "093444.000"
    assert msg.state0 == "Outside geofence"
    assert msg.state1 == "Unknown"
    assert msg.state2 == "Unknown"
    assert msg.state3 == "Inside geofence"

def test_pqtmcfgsvin():
    """Test PQTMCFGSVIN with a successful response."""
    data = "$PQTMCFGSVIN,OK,2,300,1.5,6378137.0,0.0,0.0*7A"
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.qtm.QTMCFGSVIN
    assert msg.sentence_type == "CFGSVIN"
    assert msg.status == "OK"
    assert msg.mode == "2"
    assert msg.min_dur == "300"
    assert msg.acc_limit == "1.5"
    assert msg.ecef_x == "6378137.0"
    assert msg.ecef_y == "0.0"
    assert msg.ecef_z == "0.0"

def test_pqtmsvinstatus():
    """Test PQTMSVINSTATUS with example data."""
    data = "$PQTMSVINSTATUS,1,2241,1,0,0,538,43200,-2472436.0802,4828833.0026,3343698.4839,9.5*39"
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.qtm.QTMSVINSTATUS
    assert msg.sentence_type == "SVINSTATUS"
    assert msg.msg_ver == "1"
    assert msg.tow == "2241"
    assert msg.valid == "In-progress"
    assert msg.res0 == "0"
    assert msg.res1 == "0"
    assert msg.obs == "538"
    assert msg.cfg_dur == "43200"
    assert msg.mean_x == "-2472436.0802"
    assert msg.mean_y == "4828833.0026"
    assert msg.mean_z == "3343698.4839"
    assert msg.mean_acc == "9.5"

def test_pqtmgpsstart():
    """Test PQTMGNSSSTART with OK response."""
    data = "$PQTMGNSSSTART,OK*79"
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.qtm.QTMGNSSSTART
    assert msg.sentence_type == "GNSSSTART"
    assert msg.status == "OK"

def test_pqtmgnssstop():
    """Test PQTMGNSSSTOP with OK response."""
    data = "$PQTMGNSSSTOP,OK*21"
    msg = pynmea2.parse(data)
    assert type(msg) == pynmea2.qtm.QTMGNSSSTOP
    assert msg.sentence_type == "GNSSSTOP"
    assert msg.status == "OK"

def test_pqtmpvt():
    """Test PQTMPVT with example data."""
    data = "$PQTMPVT,1,31075000,20221225,083737.000,0,3,9,18,31.12738291,117.26372910,34.212,5.267,3.212,2.928,0.238,4.346,34.12,2.16,4.38*51"
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.qtm.QTMPVT
    assert msg.sentence_type == "PVT"
    assert msg.msg_ver == "1"
    assert msg.tow == "31075000"
    assert msg.date == "20221225"
    assert msg.time == "083737.000"
    assert msg.res == "0"
    assert msg.fix_mode == "3"
    assert msg.num_sat_used == "9"
    assert msg.leap_seconds == "18"
    assert msg.lat == "31.12738291"
    assert msg.lon == "117.26372910"
    assert msg.alt == "34.212"
    assert msg.sep == "5.267"
    assert msg.vel_n == "3.212"
    assert msg.vel_e == "2.928"
    assert msg.vel_d == "0.238"
    assert msg.spd == "4.346"
    assert msg.heading == "34.12"
    assert msg.hdop == "2.16"
    assert msg.pdop == "4.38"

def test_pqtmcfgnmeadp():
    """Test PQTMCFGNMEADP with a successful set response."""
    data = "$PQTMCFGNMEADP,OK,3,6,1,2,3,2*66"
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.qtm.QTMCFGNMEADP
    assert msg.sentence_type == "CFGNMEADP"
    assert msg.status == "OK"
    assert msg.utc_dp == "3"
    assert msg.pos_dp == "6"
    assert msg.alt_dp == "1"
    assert msg.dop_dp == "2"
    assert msg.spd_dp == "3"
    assert msg.cog_dp == "2"

def test_pqtmcfgrcvrmode():
    """Test PQTMCFGRCVRMODE with a successful set response."""
    data = "$PQTMCFGRCVRMODE,OK,2*7A"
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.qtm.QTMCFGRCVRMODE
    assert msg.sentence_type == "CFGRCVRMODE"
    assert msg.status == "OK"
    assert msg.mode == "2"

    # Check if the mode description matches
    description = msg.get_mode_description()
    assert description == "Base Station"

def test_pqtmpl():
    """Test PQTMPL with example data."""
    data = "$PQTMPL,1,55045200,5.00,1,1,2879,2718,4766,5344,4323,10902,,,1*2D"
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.qtm.QTMPL
    assert msg.sentence_type == "PL"
    assert msg.msg_ver == "1"
    assert msg.tow == "55045200"
    assert msg.pul == "5.00"
    assert msg.res1 == "1"
    assert msg.res2 == "1"
    assert msg.pl_posn == "2879"
    assert msg.pl_pose == "2718"
    assert msg.pl_posd == "4766"
    assert msg.pl_veln == "5344"
    assert msg.pl_vele == "4323"
    assert msg.pl_veld == "10902"
    assert msg.res3 == ""  # Null field
    assert msg.res4 == ""  # Null field
    assert msg.pl_time == "1"

def test_pqtmcfgsbas():
    """Test PQTMCFGSBAS with example data."""
    data = "$PQTMCFGSBAS,OK,2A*2E"
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.qtm.QTMCFGSBAS
    assert msg.sentence_type == "CFGSBAS"
    assert msg.status == "OK"
    assert msg.value == "2A"  # Hexadecimal value for SBAS configuration

    # Validate SBAS configuration description
    description = msg.get_sbas_description()
    assert "WAAS" not in description
    assert "EGNOS" not in description
    assert "MSAS" not in description
    assert "GAGAN" in description  # MSAS not enabled with this value

def test_pqtmcfgcnst():
    """Test PQTMCFGCNST with example data."""
    data = "$PQTMCFGCNST,OK,1,1,0,1,0,0*79"
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.qtm.QTMCFGCNST
    assert msg.sentence_type == "CFGCNST"
    assert msg.status == "OK"
    assert msg.gps == "1"
    assert msg.glonass == "1"
    assert msg.galileo == "0"
    assert msg.bds == "1"
    assert msg.qzss == "0"
    assert msg.reserved == "0"

    # Validate constellation status descriptions
    statuses = msg.get_constellation_status()
    assert statuses["GPS"] == "Enabled"
    assert statuses["GLONASS"] == "Enabled"
    assert statuses["Galileo"] == "Disabled"
    assert statuses["BDS"] == "Enabled"
    assert statuses["QZSS"] == "Disabled"

def test_pqtmdop():
    """Test PQTMDOP with example data."""
    data = "$PQTMDOP,1,570643000,1.01,0.88,0.49,0.73,0.50,0.36,0.35*7C"
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.qtm.QTMDOP
    assert msg.sentence_type == "DOP"
    assert msg.msg_ver == "1"
    assert msg.tow == "570643000"
    assert msg.gdop == "1.01"
    assert msg.pdop == "0.88"
    assert msg.tdop == "0.49"
    assert msg.vdop == "0.73"
    assert msg.hdop == "0.50"
    assert msg.ndop == "0.36"
    assert msg.edop == "0.35"

    # Validate DOP status descriptions
    assert msg.get_dop_status(msg.gdop) == "Valid"
    assert msg.get_dop_status("99.99") == "Invalid"

def test_pqtmcfgfixrate():
    """Test PQTMCFGFIXRATE with a successful set response."""
    data = "$PQTMCFGFIXRATE,OK*27"
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.qtm.QTMCFGFIXRATE
    assert msg.sentence_type == "CFGFIXRATE"
    assert msg.status == "OK"

def test_pqtmvel():
    """Test PQTMVEL with example data."""
    data = "$PQTMVEL,1,154512.100,1.251,2.452,1.245,2.752,3.021,180.512,0.124,0.254,0.250*67"
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.qtm.QTMVEL
    assert msg.version == "1"
    assert msg.sentence_type == "VEL"
    assert msg.time == "154512.100"
    assert msg.vel_n == "1.251"
    assert msg.vel_e == "2.452"
    assert msg.vel_d == "1.245"
    assert msg.grd_spd == "2.752"
    assert msg.spd == "3.021"
    assert msg.heading == "180.512"
    assert msg.grd_spd_acc == "0.124"
    assert msg.spd_acc == "0.254"
    assert msg.heading_acc == "0.25"

def test_pqtmcfgodo():
    """Test PQTMCFGODO with a successful response."""
    data = "$PQTMCFGODO,OK,1,100*36"
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.qtm.QTMCFGODO
    assert msg.sentence_type == "CFGODO"
    assert msg.status == "OK"
    assert msg.state == "1"
    assert msg.init_dist == "100"
    assert msg.get_state_description() == "Enabled"

def test_pqtmodo():
    """Test PQTMODO with example data"""
    data = "$PQTMODO,1,120635.000,1,112.3*6E"
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.qtm.QTMODO
    assert msg.sentence_type == "ODO"
    assert msg.msg_ver == "1"
    assert msg.time == "120635.000"
    assert msg.state == "1"
    assert msg.dist == "112.3"
    assert msg.get_state_description() == "Enabled"

