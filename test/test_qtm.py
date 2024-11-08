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

def test_qtmuniqid():
    """Test QTMUNIQID Command Response with successful example data."""
    # Example of a successful response
    data_success = "$PQTMUNIQID,OK,8,1A2B3C4D5E6F7A8B*0A"
    msg_success = pynmea2.parse(data_success)

    assert type(msg_success) == pynmea2.qtm.QTMUNIQID
    assert msg_success.sentence_type == "UNIQID"
    assert msg_success.response == "OK"
    assert msg_success.length == "8"  # Length of chip unique ID
    assert msg_success.chip_id == "1A2B3C4D5E6F7A8B"  # Chip unique ID

def test_pqtmjammingstatus():
    """Test PQTMJAMMINGSTATUS with example data."""
    data = "$PQTMJAMMINGSTATUS,1,2*44"  # Example NMEA sentence with MsgVer=1, Status=2
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.qtm.QTMJAMMINGSTATUS
    assert msg.sentence_type == "JAMMINGSTATUS"
    assert msg.msg_ver == "1"
    assert msg.status == "Warning status"  # Status 2 should be "Warning status"

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

def test_pqtmantennastatus():
    """Test PQTMTANTENNASTATUS Message with example data."""
    # Example of a successful message
    data = "$PQTMANTENNASTATUS,3,2,1,1*52"
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.qtm.QTMANTENNASTATUS
    assert msg.sentence_type == "ANTENNASTATUS"
    assert msg.msg_ver == "3"  # Message version
    assert msg.ant_status == "2"  # Open-circuit status
    assert msg.ant_power_ind == "1"  # Power-on
    assert msg.mode_ind == "1"  # Automatic mode, using integrated antenna

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

def test_pqtmls():
    """Test PQTMLS Message with example data."""
    # Example of a PQTMLS message
    data = "$PQTMLS,1,195494,1,2299,18,0,1,,137,7,18*2C"
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.qtm.QTMLS
    assert msg.sentence_type == "MLS"
    assert msg.msg_ver == "1"  # Message version
    assert msg.tow == "195494"  # Time of week
    assert msg.ls_ref == "GPS"  # Leap second reference: GPS
    assert msg.wn == "2299"  # UTC reference week number
    assert msg.ls == "18"  # Current number of leap seconds
    assert msg.flag == "Invalid"  # Leap second flag: Invalid
    assert msg.lsf_ref == "GPS"  # Leap second forecast reference: GPS
    assert msg.reserved == ""  # Reserved field
    assert msg.wnlsf == "137"  # Week number of the new leap second
    assert msg.dn == "7"  # Day of the week: Saturday
    assert msg.lsf == "18"  # Leap second count after changes

def test_pqtmdrcal():
    """Test PQTMDRCAL Message with example data."""
    # Example of a PQTMDRCAL message
    data = "$PQTMDRCAL,1,0,1*5C"
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.qtm.QTMDRCAL
    assert msg.sentence_type == "DRCAL"
    assert msg.msg_ver == "1"  # Message version
    assert msg.cal_state == "Not calibrated"  # DR calibration state
    assert msg.nav_type == "GNSS only"  # Navigation type

def test_pqtmimutype():
    """Test PQTMIMUTYPE Message with example data."""
    # Example of a PQTMIMUTYPE message
    data = "$PQTMIMUTYPE,1,2*52"
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.qtm.QTMIMUTYPE
    assert msg.sentence_type == "IMUTYPE"
    assert msg.msg_ver == "1"  # Message version
    assert msg.status == "IMU initialization successful"  # IMU initialization status

def test_pqtmvehmsg():
    """Test PQTMVEHMSG Message with different MsgVer examples."""

    # Example for MsgVer = 1
    data1 = "$PQTMVEHMSG,1,0,3.6*1C"
    msg1 = pynmea2.parse(data1)
    assert type(msg1) == pynmea2.qtm.QTMVEHMSG
    assert msg1.sentence_type == "VEHMSG"
    assert msg1.msg_ver == "1"
    assert msg1.timestamp == "0"
    assert msg1.parameters["VehSpeed"] == 3.6

    # Example for MsgVer = 2
    data2 = "$PQTMVEHMSG,2,0,100,1*18"
    msg2 = pynmea2.parse(data2)
    assert msg2.msg_ver == "2"
    assert msg2.timestamp == "0"
    assert msg2.parameters["WheelTickCNT"] == 100
    assert msg2.parameters["FWD_Ind"] == "Forward"

    # Example for MsgVer = 3
    data3 = "$PQTMVEHMSG,3,0,3.6,3.6,3.6,3.6*19"
    msg3 = pynmea2.parse(data3)
    assert msg3.msg_ver == "3"
    assert msg3.parameters["LF_Spd"] == 3.6
    assert msg3.parameters["RF_Spd"] == 3.6
    assert msg3.parameters["LR_Spd"] == 3.6
    assert msg3.parameters["RR_Spd"] == 3.6
    assert msg3.parameters["RR_Spd"] == 3.6

    # Example for MsgVer = 4
    data4 = "$PQTMVEHMSG,4,0,100,100,100,100,1*03"
    msg4 = pynmea2.parse(data4)
    assert msg4.msg_ver == "4"
    assert msg4.parameters["LF_TickCNT"] == 100
    assert msg4.parameters["RF_TickCNT"] == 100
    assert msg4.parameters["LR_TickCNT"] == 100
    assert msg4.parameters["RR_TickCNT"] == 100
    assert msg4.parameters["FWD_Ind"] == "Forward"

def test_pqtmins():
    """Test PQTMINS Message with example data."""
    # Example of a PQTMINS message
    data = "$PQTMINS,240951,1,31.82222216,117.11578436,62.555605,-0.004233,0.005535,-0.004011,0.00,0.00,127.41*40"
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.qtm.QTMINS
    assert msg.sentence_type == "INS"
    assert msg.timestamp == "240951"
    assert msg.sol_type == "DR not ready. GNSS, roll, pitch, and relative heading ready."
    assert msg.latitude == "31.82222216"
    assert msg.longitude == "117.11578436"
    assert msg.height == "62.555605"
    assert msg.vel_n == "-0.004233"
    assert msg.vel_e == "0.005535"
    assert msg.vel_d == "-0.004011"
    assert msg.roll == "0.0"
    assert msg.pitch == "0.0"
    assert msg.yaw == "127.41"

def test_pqtmgps():
    """Test PQTMGPS Message with example data."""
    # Example of a PQTMGPS message
    data = "$PQTMGPS,86139,94183,31.82218794,117.11579022,65.755080,0.027,94.68,2.533952,0.555471,0.886183,29,3*6B"
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.qtm.QTMGPS
    assert msg.sentence_type == "GPS"
    assert msg.timestamp == "86139"
    assert msg.tow == "94183"
    assert msg.latitude == "31.82218794"
    assert msg.longitude == "117.11579022"
    assert msg.altitude == "65.755080"
    assert msg.speed == "0.027"
    assert msg.heading == "94.68"
    assert msg.accuracy == "2.533952"
    assert msg.hdop == "0.555471"
    assert msg.pdop == "0.886183"
    assert msg.num_sat_used == "29"
    assert msg.fix_mode == "3D fix (including RTK float or RTK fixed)"

def test_pqtmvehmot():
    """Test PQTMVEHMOT Message with both MsgVer examples."""

    # Example for MsgVer = 1
    data1 = "$PQTMVEHMOT,1,0.288124,0.159930*0A"
    msg1 = pynmea2.parse(data1)
    assert type(msg1) == pynmea2.qtm.QTMVEHMOT
    assert msg1.sentence_type == "VEHMOT"
    assert msg1.msg_ver == "1"
    assert msg1.peak_acceleration == "0.288124"
    assert msg1.peak_angular_rate == "0.159930"

    # Example for MsgVer = 2
    data2 = "$PQTMVEHMOT,2,204159.000,1,2,1,1,,,,,*1D"
    msg2 = pynmea2.parse(data2)
    assert msg2.msg_ver == "2"
    assert msg2.utc == "204159.000"
    assert msg2.veh_type == "1"
    assert msg2.mot_state == "2"
    assert msg2.acc_status == "1"
    assert msg2.turning_status == "1"
    assert msg2.reserved == ["", "", "", "", ""]

def test_pqtmsenmsg():
    """Test PQTMSENMSG Message with both MsgVer examples."""

    # Example for MsgVer = 2
    data2 = "$PQTMSENMSG,2,1000,22.21,0.124521,1.241541,0.912451,0.145785,1.241541,8.954214*2D"
    msg2 = pynmea2.parse(data2)
    assert type(msg2) == pynmea2.qtm.QTMSENMSG
    assert msg2.sentence_type == "SENMSG"
    assert msg2.msg_ver == "2"
    assert msg2.timestamp == "1000"
    assert msg2.imu_temp == "22.21"
    assert msg2.imu_gyro_x == "0.124521"
    assert msg2.imu_gyro_y == "1.241541"
    assert msg2.imu_gyro_z == "0.912451"
    assert msg2.imu_acc_x == "0.145785"
    assert msg2.imu_acc_y == "1.241541"
    assert msg2.imu_acc_z == "8.954214"

    # Example for MsgVer = 4
    data4 = "$PQTMSENMSG,4,1000,22.21,0.124521,1.241541,0.912451,0.145785,1.241541,8.954214*2B"
    msg4 = pynmea2.parse(data4)
    assert msg4.msg_ver == "4"
    assert msg4.timestamp == "1000"
    assert msg4.imu_temp == "22.21"
    assert msg4.imu_gyro_x == "0.124521"
    assert msg4.imu_gyro_y == "1.241541"
    assert msg4.imu_gyro_z == "0.912451"
    assert msg4.imu_acc_x == "0.145785"
    assert msg4.imu_acc_y == "1.241541"
    assert msg4.imu_acc_z == "8.954214"

def test_pqtmdrpva():
    """Test PQTMDRPVA Message with example data."""

    # Example with no fix
    data1 = "$PQTMDRPVA,1,1000,163355.000,0,,,,,,,,,,,*7C"
    msg1 = pynmea2.parse(data1)
    assert type(msg1) == pynmea2.qtm.QTMDRPVA
    assert msg1.sentence_type == "DRPVA"
    assert msg1.msg_ver == "1"
    assert msg1.timestamp == "1000"
    assert msg1.time == "163355.000"
    assert msg1.sol_type == "No fix"  # Human-readable description
    assert msg1.latitude == ""
    assert msg1.longitude == ""
    assert msg1.altitude == ""
    assert msg1.sep == ""
    assert msg1.vel_n == ""
    assert msg1.vel_e == ""
    assert msg1.vel_d == ""
    assert msg1.speed == ""
    assert msg1.roll == ""
    assert msg1.pitch == ""
    assert msg1.heading == ""

    # Example with GNSS + DR fix
    data2 = "$PQTMDRPVA,1,75000,083737.000,2,31.12738291,117.26372910,34.212,5.267,3.212,2.928,0.238,4.346,0.392663,1.300793,0.030088*5E"
    msg2 = pynmea2.parse(data2)
    assert msg2.msg_ver == "1"
    assert msg2.timestamp == "75000"
    assert msg2.time == "083737.000"
    assert msg2.sol_type == "Combination (GNSS + DR)"  # Human-readable description
    assert msg2.latitude == "31.12738291"
    assert msg2.longitude == "117.26372910"
    assert msg2.altitude == "34.212"
    assert msg2.sep == "5.267"
    assert msg2.vel_n == "3.212"
    assert msg2.vel_e == "2.928"
    assert msg2.vel_d == "0.238"
    assert msg2.speed == "4.346"
    assert msg2.roll == "0.392663"
    assert msg2.pitch == "1.300793"
    assert msg2.heading == "0.030088"


def test_pqtmvehatt():
    """Test PQTMVEHATT Message with example data."""

    # Example data
    data = "$PQTMVEHATT,1,1000,10.002154,20.235412,160.145185,1.254123,5.451214,5.012154*3D"
    msg = pynmea2.parse(data)

    assert type(msg) == pynmea2.qtm.QTMVEHATT
    assert msg.sentence_type == "VEHATT"
    assert msg.msg_ver == "1"
    assert msg.timestamp == "1000"
    assert msg.roll == "10.002154"
    assert msg.pitch == "20.235412"
    assert msg.heading == "160.145185"
    assert msg.acc_roll == "1.254123"
    assert msg.acc_pitch == "5.451214"
    assert msg.acc_heading == "5.012154"
