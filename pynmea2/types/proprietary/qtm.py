from ... import nmea

class QTM(nmea.ProprietarySentence):
    sentence_types = {}

    def __new__(_cls, manufacturer, data):
        # Dynamically derive the message class name
        name = manufacturer + data[0]  # Use first data element as part of the name
        cls = _cls.sentence_types.get(name, _cls)
        return super(QTM, cls).__new__(cls)

class QTMVERNO(QTM):
    """
    PQTMVERNO Message

    Supports:
    - $PQTMVERNO,<VerStr>,<BuildDate>,<BuildTime>*<Checksum>
    """
    fields = (
        ('sentence_type', 'sentence_type'),  # VERNO
        ('version', 'version'),  # Example: LC29HAANR01A04S
        ('build_date', 'build_date'),  # Format: YYYY/MM/DD
        ('build_time', 'build_time'),  # Format: HH:MM:SS
    )

    def __init__(self, manufacturer, data):
        super(QTMVERNO, self).__init__(manufacturer, data)
        # print(data)  # Debugging print to confirm input structure

        # Assign attributes using the shared utils for formatting
        self.sentence_type = data[0]
        self.version = data[1]
        self.date = data[2]  # Use the new date parser
        self.build_time = data[3]  # Use the shared timestamp function

    # def __repr__(self):
    #     # Improved __repr__ for better readability
    #     return ("<QTMVERNO(sentence_type={sentence_type}, version='{version}', "
    #             "build_date={build_date}, build_time={build_time})>").format(
    #         sentence_type=self.sentence_type,
    #         version=self.version,
    #         build_date=self.build_date,
    #         build_time=self.build_time
    #     )

class QTMSAVEPAR(QTM):
    """
    PQTM SAVEPAR Message

    Supports:
    - $PQTMSAVEPAR,OK*72
    """
    fields = (
        ('sentence_type', 'sentence_type'),
        ('status', 'status')
    )

    def __init__(self, manufacturer, data):
        super(QTMSAVEPAR, self).__init__(manufacturer, data)
        self.status = data[1]  # Handle status field

class QTMRESTOREPAR(QTM):
    """
    PQTM RESTOREPAR Message

    Supports:
    - $PQTMRESTOREPAR,OK*3B
    """
    fields = (
        ('sentence_type', 'sentence_type'),
        ('status', 'status')
    )

    def __init__(self, manufacturer, data):
        super(QTMRESTOREPAR, self).__init__(manufacturer, data)
        self.status = data[1]  # Handle status field

class QTMEPE(QTM):
    """
    PQTMEPE Message

    Outputs the estimated positioning error.

    Supports:
    - $PQTMEPE,<MsgVer>,<EPE_North>,<EPE_East>,<EPE_Down>,<EPE_2D>,<EPE_3D>*<Checksum>
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # EPE
        ('msg_ver', 'msg_ver'),  # Message version (always 2)
        ('epe_north', 'epe_north'),  # Estimated north error (in meters)
        ('epe_east', 'epe_east'),  # Estimated east error (in meters)
        ('epe_down', 'epe_down'),  # Estimated down error (in meters)
        ('epe_2d', 'epe_2d'),  # Estimated 2D position error (in meters)
        ('epe_3d', 'epe_3d'),  # Estimated 3D position error (in meters)
    )

    def __init__(self, manufacturer, data):
        super(QTMEPE, self).__init__(manufacturer, data)
        # print(data)  # Debugging print to confirm input structure

        # Set attributes based on input data
        self.sentence_type = data[0]
        self.msg_ver = int(data[1])
        self.epe_north = float(data[2])
        self.epe_east = float(data[3])
        self.epe_down = float(data[4])
        self.epe_2d = float(data[5])
        self.epe_3d = float(data[6])

class QTMCFGGEOFENCE(QTM):
    """
    PQTMCFGGEOFENCE Message

    Supports:
    - $PQTMCFGGEOFENCE,OK,<Index>,<Status>,<Reserved>,<Shape>,<Lat0>,<Lon0>,<Lat1/Radius>,
      [<Lon1>,<Lat2>,<Lon2>,<Lat3>,<Lon3>]*<Checksum>
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "CFGGEOGENCE"
        ('Status', 'status'),  # "OK"
        ('Index', 'index'),  # Geofence index (0-3)
        ('Enabled', 'enabled'),  # 0 = Disabled, 1 = Enabled
        ('Reserved', 'reserved'),  # Always 0
        ('Shape', 'shape'),  # Geofence shape (0-3)
        ('Lat0', 'lat0'),  # Latitude of the first point
        ('Lon0', 'lon0'),  # Longitude of the first point
        ('Lat1_or_Radius', 'lat1_or_radius'),  # Latitude/Radius based on shape
        ('Lon1', 'lon1'),  # Longitude of the second point (optional)
        ('Lat2', 'lat2'),  # Latitude of the third point (optional)
        ('Lon2', 'lon2'),  # Longitude of the third point (optional)
        ('Lat3', 'lat3'),  # Latitude of the fourth point (optional)
        ('Lon3', 'lon3')  # Longitude of the fourth point (optional)
    )

    def __init__(self, manufacturer, data):
        super(QTMCFGGEOFENCE, self).__init__(manufacturer, data)
        # print(data)  # Debugging print to confirm input structure

        # Extract and assign the mandatory fields
        self.sentence_type = data[0]  # Should always be "CFGGEOGENCE"
        self.status = data[1]  # Should be "OK"
        self.index = data[2]
        self.enabled = data[3]  # 0 = Disabled, 1 = Enabled
        self.reserved = data[4]
        self.shape = data[5]
        self.lat0 = data[6]
        self.lon0 = data[7]
        self.lat1_or_radius = data[8]

        # Optional fields (only for specific shapes)
        if len(data) > 9:
            self.lon1 = data[9]
        if len(data) > 10:
            self.lat2 = data[10]
        if len(data) > 11:
            self.lon2 = data[11]
        if len(data) > 12:
            self.lat3 = data[12]
        if len(data) > 13:
            self.lon3 = data[13]

class QTMGEOFENCESTATUS(QTM):
    """
    PQTMGEOFENCESTATUS Message

    Supports:
    - $PQTMGEOFENCESTATUS,<MsgVer>,<Time>,<State0>,<State1>,<State2>,<State3>*<Checksum>

    Geofence State Meaning:
    - 0 = Unknown (Not defined)
    - 1 = Inside geofence
    - 2 = Outside geofence
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "GEOFENCESTATUS"
        ('MsgVer', 'msg_ver'),  # Message version (Always 1)
        ('Time', 'time'),  # UTC time (hhmmss.sss)
        ('State0', 'state0'),  # Geofence state 0
        ('State1', 'state1'),  # Geofence state 1
        ('State2', 'state2'),  # Geofence state 2
        ('State3', 'state3')  # Geofence state 3
    )

    def __init__(self, manufacturer, data):
        super(QTMGEOFENCESTATUS, self).__init__(manufacturer, data)
        # print(data)  # Debugging print to confirm input structure

        # Assign the parsed fields
        self.sentence_type = data[0]  # Should always be "GEOFENCESTATUS"
        self.msg_ver = data[1]  # Always 1
        self.time = data[2]  # UTC time in hhmmss.sss format

        # Convert states from raw data to meaningful descriptions
        self.state0 = self.parse_state(data[3])  # Geofence 0 state
        self.state1 = self.parse_state(data[4])  # Geofence 1 state
        self.state2 = self.parse_state(data[5])  # Geofence 2 state
        self.state3 = self.parse_state(data[6])  # Geofence 3 state

    @staticmethod
    def parse_state(state_value):
        """
        Parse the state field and return the corresponding description.
        """
        state_map = {
            "0": "Unknown",
            "1": "Inside geofence",
            "2": "Outside geofence"
        }
        return state_map.get(state_value, "Invalid state")  # Handle unexpected values

class QTMJAMMINGSTATUS(QTM):
    """
    PQTMJAMMINGSTATUS Message

    Supports:
    - $PQTJAMMINGSTATUS,<MsgVer>,<Status>*<Checksum>

    Jamming Detection Status Meaning:
    - 0 = Unknown
    - 1 = No jamming, healthy status
    - 2 = Warning status
    - 3 = Critical status
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "JAMMINGSTATUS"
        ('MsgVer', 'msg_ver'),  # Message version (Always 1)
        ('Status', 'status')  # Jamming detection status
    )

    def __init__(self, manufacturer, data):
        super(QTMJAMMINGSTATUS, self).__init__(manufacturer, data)
        # print(data)  # Debugging print to confirm input structure

        # Assign the parsed fields
        self.sentence_type = data[0]  # Should always be "JAMMINGSTATUS"
        self.msg_ver = data[1]  # Always 1 for this message version
        self.status = self.parse_status(data[2])  # Jamming detection status

    @staticmethod
    def parse_status(status_value):
        """
        Parse the status field and return the corresponding description.
        """
        status_map = {
            "0": "Unknown",
            "1": "No jamming, healthy status",
            "2": "Warning status",
            "3": "Critical status"
        }
        return status_map.get(status_value, "Invalid status")  # Handle unexpected values

class QTMUNIQID(QTM):
    """
    PQTMUNIQID Command Response

    Supports:
    - $PQTMUNIQID,OK,<Length>,<ID>*<Checksum>

    Field Description:
    - Length: Length of the chip unique ID in bytes
    - ID: The chip unique ID in hexadecimal format
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "UNIQID"
        ('Response', 'response'),  # Response type, always "OK" for success
        ('Length', 'length'),  # Length of chip unique ID in bytes
        ('ID', 'chip_id')  # Chip unique ID in hexadecimal
    )

    def __init__(self, manufacturer, data):
        super(QTMUNIQID, self).__init__(manufacturer, data)
        # Assign the parsed fields
        self.sentence_type = "UNIQID"
        self.response = data[1]  # "OK"
        self.length = data[2]  # Length of chip unique ID
        self.chip_id = data[3]  # Chip unique ID in hexadecimal

class QTMANTENNASTATUS(QTM):
    """
    PQTMTANTENNASTATUS Message

    Supports:
    - $PQTMTANTENNASTATUS,<MsgVer>,<AntStatus>,<AntPowerInd>,<ModeInd>*<Checksum>

    Field Descriptions:
    - MsgVer: Message version (Always 3 for this version)
    - AntStatus: Antenna status
        - 0 = Unknown
        - 1 = Normal
        - 2 = Open-circuit
        - 3 = Short-circuit
    - AntPowerInd: Antenna power indicator
        - 0 = Power-off
        - 1 = Power-on
        - 2 = Unknown
    - ModeInd: Antenna mode indicator
        - 0 = Unknown
        - 1 = Automatic mode, using integrated antenna
        - 2 = Automatic mode, using external antenna
        - 3 = Manual mode, using integrated antenna
        - 4 = Manual mode, using external antenna
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "ANTENNASTATUS"
        ('MsgVer', 'msg_ver'),  # Message version, always "3"
        ('AntStatus', 'ant_status'),  # Antenna status
        ('AntPowerInd', 'ant_power_ind'),  # Antenna power indicator
        ('ModeInd', 'mode_ind')  # Antenna mode indicator
    )

    def __init__(self, manufacturer, data):
        super(QTMANTENNASTATUS, self).__init__(manufacturer, data)
        # Assign the parsed fields
        self.sentence_type = "ANTENNASTATUS"
        self.msg_ver = data[1]  # Always 3 for this message version
        self.ant_status = data[2]  # Antenna status
        self.ant_power_ind = data[3]  # Antenna power indicator
        self.mode_ind = data[4]  # Antenna mode indicator

class QTMCFGSVIN(QTM):
    """
    PQTMCFGSVIN Message

    Note: This command is supported on LC29H (DA, EA) only

    Supports:
    - $PQTMCFGSVIN,OK,<Mode>,<MinDur>,<3D_AccLimit>,<ECEF_X>,<ECEF_Y>,<ECEF_Z>*<Checksum>

    Parameters:
    - Mode: Configure the receiver mode (0 = Disable, 1 = Survey-in, 2 = Fixed mode).
    - MinDur: Minimum survey-in duration (0-86400 seconds).
    - 3D_AccLimit: Limit 3D position accuracy in meters (0 = No limit).
    - ECEF_X/Y/Z: WGS84 ECEF X, Y, and Z coordinates in meters.
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # CFGSVIN
        ('status', 'status'),  # OK
        ('mode', 'mode'),  # Receiver mode (0, 1, 2)
        ('min_dur', 'min_dur'),  # Survey-in duration (in seconds)
        ('acc_limit', 'acc_limit'),  # 3D accuracy limit in meters
        ('ecef_x', 'ecef_x'),  # ECEF X coordinate
        ('ecef_y', 'ecef_y'),  # ECEF Y coordinate
        ('ecef_z', 'ecef_z'),  # ECEF Z coordinate
    )

    def __init__(self, manufacturer, data):
        super(QTMCFGSVIN, self).__init__(manufacturer, data)
        # print(data)  # Debugging print to confirm input structure

        # Set attributes based on input data
        self.sentence_type = data[0]  # Always "CFGSVIN"
        self.status = data[1]  # Should be "OK"
        self.mode = data[2]  # Mode (0, 1, or 2)
        self.min_dur = data[3]  # Survey-in minimum duration
        self.acc_limit = data[4]  # 3D accuracy limit
        self.ecef_x = data[5]  # ECEF X coordinate
        self.ecef_y = data[6]  # ECEF Y coordinate
        self.ecef_z = data[7]  # ECEF Z coordinate

class QTMSVINSTATUS(QTM):
    """
    PQTMSVINSTATUS Message

    Outputs the survey-in status.

    Supports:
    - $PQTMSVINSTATUS,<MsgVer>,<TOW>,<Valid>,<Res0>,<Res1>,<Obs>,<CfgDur>,<MeanX>,<MeanY>,
      <MeanZ>,<MeanAcc>*<Checksum>

    Parameters:
    - MsgVer: Message version (Always 1).
    - TOW: GPS Time of Week (milliseconds).
    - Valid: Survey-in position validity flag (0 = Invalid, 1 = In-progress, 2 = Valid).
    - Res0: Reserved field (Always 0).
    - Res1: Reserved field (Always 0).
    - Obs: Number of position observations.
    - CfgDur: Configured duration from the PQTMCFGSVIN command.
    - MeanX/Y/Z: Mean position along the X, Y, and Z axes in meters.
    - MeanAcc: Mean position accuracy in meters.
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "SVINSTATUS"
        ('msg_ver', 'msg_ver'),  # Message version (Always 1)
        ('tow', 'tow'),  # GPS Time of Week (milliseconds)
        ('valid', 'valid'),  # Survey-in validity flag (0, 1, 2)
        ('res0', 'res0'),  # Reserved (Always 0)
        ('res1', 'res1'),  # Reserved (Always 0)
        ('obs', 'obs'),  # Number of observations
        ('cfg_dur', 'cfg_dur'),  # Configured duration
        ('mean_x', 'mean_x'),  # Mean X position in meters
        ('mean_y', 'mean_y'),  # Mean Y position in meters
        ('mean_z', 'mean_z'),  # Mean Z position in meters
        ('mean_acc', 'mean_acc'),  # Mean position accuracy in meters
    )

    def __init__(self, manufacturer, data):
        super(QTMSVINSTATUS, self).__init__(manufacturer, data)
        # print(data)  # Debugging print to confirm input structure

        # Assign the parsed fields to class attributes
        self.sentence_type = data[0]
        self.msg_ver = data[1]
        self.tow = data[2]
        self.valid = self.parse_validity(data[3])
        self.res0 = data[4]
        self.res1 = data[5]
        self.obs = data[6]
        self.cfg_dur = data[7]
        self.mean_x = data[8]
        self.mean_y = data[9]
        self.mean_z = data[10]
        self.mean_acc = data[11]

    @staticmethod
    def parse_validity(value):
        """
        Parse the validity flag to a meaningful description.
        """
        validity_map = {
            "0": "Invalid",
            "1": "In-progress",
            "2": "Valid"
        }
        return validity_map.get(value, "Unknown validity")

class QTMGNSSSTART(QTM):
    """
    PQTMGNSSSTART Message

    Starts the GNSS engine.

    Supports:
    - $PQTMGNSSSTART,OK*<Checksum>

    If successful, the response is:
    - OK
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "GNSSSTART"
        ('status', 'status'),  # Always "OK"
    )

    def __init__(self, manufacturer, data):
        super(QTMGNSSSTART, self).__init__(manufacturer, data)
        # print(data)  # Debugging print to confirm input structure

        # Extract sentence_type and status
        self.sentence_type = data[0]
        self.status = data[1]

class QTMGNSSSTOP(QTM):
    """
    PQTMGNSSSTOP Message

    Stops the GNSS engine.

    Supports:
    - $PQTMGNSSSTOP,OK*<Checksum>

    If successful, the response is:
    - OK
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "GNSSSTOP"
        ('status', 'status'),  # Always "OK"
    )

    def __init__(self, manufacturer, data):
        super(QTMGNSSSTOP, self).__init__(manufacturer, data)
        # print(data)  # Debugging print to confirm input structure

        # Extract sentence_type and status
        self.sentence_type = data[0]
        self.status = data[1]

class QTMPVT(QTM):
    """
    PQTMPVT Message

    Outputs the PVT (GNSS only) result.

    Supports:
    - $PQTMPVT,<MsgVer>,<TOW>,<Date>,<Time>,<Res>,<FixMode>,<NumSatUsed>,<LeapS>,
      <Lat>,<Lon>,<Alt>,<Sep>,<VelN>,<VelE>,<VelD>,<Spd>,<Heading>,<HDOP>,<PDOP>*<Checksum>

    """

    fields = (
        ('sentence_type', 'sentence_type'),  # PVT
        ('msg_ver', 'msg_ver'),  # Always 1
        ('tow', 'tow'),  # Time of week in milliseconds
        ('date', 'date'),  # UTC Date in YYYYMMDD format
        ('time', 'time'),  # UTC Time in hhmmss.sss format
        ('res', 'res'),  # Reserved
        ('fix_mode', 'fix_mode'),  # 0=No fix, 1=Reserved, 2=2D, 3=3D fix
        ('num_sat_used', 'num_sat_used'),  # Number of satellites used
        ('leap_seconds', 'leap_seconds'),  # Leap seconds
        ('latitude', 'lat'),  # Latitude in degrees
        ('longitude', 'lon'),  # Longitude in degrees
        ('altitude', 'alt'),  # Altitude above mean sea-level in meters
        ('geoid_sep', 'sep'),  # Geoid separation in meters
        ('vel_n', 'vel_n'),  # North velocity in m/s
        ('vel_e', 'vel_e'),  # East velocity in m/s
        ('vel_d', 'vel_d'),  # Down velocity in m/s
        ('speed', 'spd'),  # Ground speed in m/s
        ('heading', 'heading'),  # Heading in degrees
        ('hdop', 'hdop'),  # Horizontal dilution of precision
        ('pdop', 'pdop')  # Position dilution of precision
    )

    def __init__(self, manufacturer, data):
        super(QTMPVT, self).__init__(manufacturer, data)
        # print(data)  # Debugging print to confirm input structure

        # Assigning the values from the input data
        self.sentence_type = data[0]
        self.msg_ver = data[1]
        self.tow = data[2]
        self.date = data[3]
        self.time = data[4]
        self.res = data[5]
        self.fix_mode = data[6]
        self.num_sat_used = data[7]
        self.leap_seconds = data[8]
        self.lat = data[9]
        self.lon = data[10]
        self.alt = data[11]
        self.sep = data[12]
        self.vel_n = data[13]
        self.vel_e = data[14]
        self.vel_d = data[15]
        self.spd = data[16]
        self.heading = data[17]
        self.hdop = data[18]
        self.pdop = data[19]

class QTMCFGNMEADP(QTM):
    """
    PQTMCFGNMEADP Message

    Supports:
    - Set command: $PQTMCFGNMEADP,W,<UTC_DP>,<POS_DP>,<ALT_DP>,<DOP_DP>,<SPD_DP>,<COG_DP>*<Checksum><CR><LF>
    - Get command: $PQTMCFGNMEADP,OK,<UTC_DP>,<POS_DP>,<ALT_DP>,<DOP_DP>,<SPD_DP>,<COG_DP>*<Checksum><CR><LF>
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "CFGNMEADP"
        ('Status', 'status'),  # "OK"
        ('UTC_DP', 'utc_dp'),  # Decimal places for UTC seconds in NMEA messages
        ('POS_DP', 'pos_dp'),  # Decimal places for latitude/longitude in NMEA messages
        ('ALT_DP', 'alt_dp'),  # Decimal places for altitude in NMEA messages
        ('DOP_DP', 'dop_dp'),  # Decimal places for DOP in NMEA messages
        ('SPD_DP', 'spd_dp'),  # Decimal places for speed in NMEA messages
        ('COG_DP', 'cog_dp')   # Decimal places for COG in NMEA messages
    )

    def __init__(self, manufacturer, data):
        super(QTMCFGNMEADP, self).__init__(manufacturer, data)
        # print(data)  # Debugging print to confirm input structure

        # Assign the parsed fields from the input data
        self.sentence_type = data[0]  # Should always be "CFGNMEADP"
        self.status = data[1]  # Should be "OK"
        self.utc_dp = int(data[2])
        self.pos_dp = int(data[3])
        self.alt_dp = int(data[4])
        self.dop_dp = int(data[5])
        self.spd_dp = int(data[6])
        self.cog_dp = int(data[7])

class QTMCFGRCVRMODE(QTM):
    """
    PQTMCFGRCVRMODE Message

    Supports:
    - $PQTMCFGRCVRMODE,OK,<Mode>*<Checksum><CR><LF>

    Receiver Working Modes:
    - "0" = Unknown
    - "1" = Rover (Restores to default NMEA output)
    - "2" = Base Station (Disables NMEA output, enables RTCM MSM4 1005 messages)
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "CFGRCVRMODE"
        ('status', 'status'),  # "OK"
        ('mode', 'mode'),  # Mode of operation as a string ("0", "1", or "2")
    )

    def __init__(self, manufacturer, data):
        super(QTMCFGRCVRMODE, self).__init__(manufacturer, data)
        # print(data)  # Debugging print to confirm input structure

        # Assign fields for the successful set response
        self.sentence_type = data[0]  # Should always be "CFGRCVRMODE"
        self.status = data[1]  # Should be "OK"
        self.mode = data[2]  # Mode should be parsed as a string

    def get_mode_description(self):
        """
        Get the description of the mode from the set response.
        """
        mode_map = {
            "0": "Unknown",
            "1": "Rover",
            "2": "Base Station"
        }
        # Return description based on the mode value
        return mode_map.get(self.mode, "Invalid mode")

class QTMPL(QTM):
    """
    PQTMPL Message

    Outputs the protection levels (PL) and uncertainty metrics.

    Supports:
    - $PQTMPL,<MsgVer>,<TOW>,<PUL>,<Res1>,<Res2>,<PL_PosN>,<PL_PosE>,<PL_PosD>,
      <PL_VelN>,<PL_VelE>,<PL_VelD>,<Res3>,<Res4>,<PL_Time>*<Checksum><CR><LF>

    Field Descriptions:
    - <MsgVer>: Message version (Always 1).
    - <TOW>: Time of week (Milliseconds).
    - <PUL>: Probability of uncertainty level per epoch (%).
    - <PL_PosN>, <PL_PosE>, <PL_PosD>: Protection levels for North, East, Down (mm).
    - <PL_VelN>, <PL_VelE>, <PL_VelD>: Protection levels for velocities (mm/s).
    - <PL_Time>: Protection level of time (ns).
    - Reserved fields are always null.
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "PL"
        ('msg_ver', 'msg_ver'),  # Message version (Always 1)
        ('tow', 'tow'),  # Time of week in milliseconds
        ('pul', 'pul'),  # Probability of uncertainty level (%)
        ('res1', 'res1'),  # Reserved (Always 1)
        ('res2', 'res2'),  # Reserved (Always 1)
        ('pl_posn', 'pl_posn'),  # Protection level (North) in mm
        ('pl_pose', 'pl_pose'),  # Protection level (East) in mm
        ('pl_posd', 'pl_posd'),  # Protection level (Down) in mm
        ('pl_veln', 'pl_veln'),  # Protection level of north velocity (mm/s)
        ('pl_vele', 'pl_vele'),  # Protection level of east velocity (mm/s)
        ('pl_veld', 'pl_veld'),  # Protection level of down velocity (mm/s)
        ('res3', 'res3'),  # Reserved (Always null)
        ('res4', 'res4'),  # Reserved (Always null)
        ('pl_time', 'pl_time')  # Protection level of time (ns)
    )

    def __init__(self, manufacturer, data):
        super(QTMPL, self).__init__(manufacturer, data)
        # print(data)  # Debugging print to confirm input structure

        # Assign parsed fields to the instance
        self.sentence_type = data[0]
        self.msg_ver = data[1]
        self.tow = data[2]
        self.pul = data[3]
        self.res1 = data[4]
        self.res2 = data[5]
        self.pl_posn = data[6]
        self.pl_pose = data[7]
        self.pl_posd = data[8]
        self.pl_veln = data[9]
        self.pl_vele = data[10]
        self.pl_veld = data[11]
        self.res3 = data[12] if len(data) > 12 else None  # Optional reserved field
        self.res4 = data[13] if len(data) > 13 else None  # Optional reserved field
        self.pl_time = data[14] if len(data) > 14 else None  # Optional time protection level

class QTMCFGSBAS(QTM):
    """
    PQTMCFGSBAS Message

    Supports:
    - $PQTMCFGSBAS,OK,<Value>*<Checksum><CR><LF>

    SBAS Configuration:
    - Bit 0 = WAAS
    - Bit 2 = EGNOS
    - Bit 4 = MSAS
    - Bit 5 = GAGAN
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "CFGSBAS"
        ('status', 'status'),  # "OK"
        ('value', 'value'),  # SBAS configuration value (Hexadecimal)
    )

    def __init__(self, manufacturer, data):
        super(QTMCFGSBAS, self).__init__(manufacturer, data)
        # print(data)  # Debugging print to confirm input structure

        # Assign fields for the successful set response
        self.sentence_type = data[0]  # Should always be "CFGSBAS"
        self.status = data[1]  # Should be "OK"
        self.value = data[2]  # Hexadecimal value representing SBAS configuration

    def get_sbas_description(self):
        """
        Get the SBAS configuration description based on the hexadecimal value.
        """
        sbas_map = {
            0: "WAAS",
            2: "EGNOS",
            4: "MSAS",
            5: "GAGAN"
        }
        # Convert the hex value to integer and find the bit-enabled services
        services = [sbas_map[bit] for bit in sbas_map if int(self.value, 16) & (1 << bit)]
        return services if services else ["No SBAS Service Enabled"]

class QTMCFGCNST(QTM):
    """
    PQTMCFGCNST Message

    Supports:
    - $PQTMCFGCNST,OK,<GPS>,<GLONASS>,<Galileo>,<BDS>,<QZSS>,<Reserved>*<Checksum><CR><LF>

    Constellation Configuration:
    - <GPS>: 0 = Disable, 1 = Enable
    - <GLONASS>: 0 = Disable, 1 = Enable
    - <Galileo>: 0 = Disable, 1 = Enable
    - <BDS>: 0 = Disable, 1 = Enable
    - <QZSS>: 0 = Disable, 1 = Enable
    - <Reserved>: Always 0
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "CFGCNST"
        ('status', 'status'),  # "OK"
        ('gps', 'gps'),  # GPS Enabled/Disabled
        ('glonass', 'glonass'),  # GLONASS Enabled/Disabled
        ('galileo', 'galileo'),  # Galileo Enabled/Disabled
        ('bds', 'bds'),  # BDS Enabled/Disabled
        ('qzss', 'qzss'),  # QZSS Enabled/Disabled
        ('reserved', 'reserved')  # Always 0
    )

    def __init__(self, manufacturer, data):
        super(QTMCFGCNST, self).__init__(manufacturer, data)
        # print(data)  # Debugging print to confirm input structure

        # Assign fields for the successful set response
        self.sentence_type = data[0]  # Should always be "CFGCNST"
        self.status = data[1]  # Should be "OK"
        self.gps = data[2]
        self.glonass = data[3]
        self.galileo = data[4]
        self.bds = data[5]
        self.qzss = data[6]
        self.reserved = data[7]

    def get_constellation_status(self):
        """
        Get the status of all constellations based on the response.
        """
        status_map = {
            '0': "Disabled",
            '1': "Enabled"
        }
        return {
            "GPS": status_map.get(self.gps, "Invalid"),
            "GLONASS": status_map.get(self.glonass, "Invalid"),
            "Galileo": status_map.get(self.galileo, "Invalid"),
            "BDS": status_map.get(self.bds, "Invalid"),
            "QZSS": status_map.get(self.qzss, "Invalid")
        }

class QTMDOP(QTM):
    """
    PQTMDOP Message

    Supports:
    - $PQTMDOP,<MsgVer>,<TOW>,<GDOP>,<PDOP>,<TDOP>,<VDOP>,<HDOP>,<NDOP>,<EDOP>*<Checksum><CR><LF>

    DOP Values:
    - GDOP: Geometric Dilution of Precision
    - PDOP: Position Dilution of Precision (3D)
    - TDOP: Time Dilution of Precision
    - VDOP: Vertical Dilution of Precision
    - HDOP: Horizontal Dilution of Precision
    - NDOP: Northing Dilution of Precision
    - EDOP: Easting Dilution of Precision

    Note: If the value is invalid, it will be 99.99
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "DOP"
        ('msg_ver', 'msg_ver'),  # Message version (Always 1)
        ('tow', 'tow'),  # Time of week (ms)
        ('gdop', 'gdop'),  # Geometric DOP
        ('pdop', 'pdop'),  # Position DOP
        ('tdop', 'tdop'),  # Time DOP
        ('vdop', 'vdop'),  # Vertical DOP
        ('hdop', 'hdop'),  # Horizontal DOP
        ('ndop', 'ndop'),  # Northing DOP
        ('edop', 'edop'),  # Easting DOP
    )

    def __init__(self, manufacturer, data):
        super(QTMDOP, self).__init__(manufacturer, data)
        # print(data)  # Debugging print to confirm input structure

        # Assign fields from the data
        self.sentence_type = data[0]  # Always "DOP"
        self.msg_ver = data[1]  # Always 1
        self.tow = data[2]  # Time of week in milliseconds
        self.gdop = data[3]
        self.pdop = data[4]
        self.tdop = data[5]
        self.vdop = data[6]
        self.hdop = data[7]
        self.ndop = data[8]
        self.edop = data[9]

    @staticmethod
    def get_dop_status(dop_value):
        """
        Interpret the DOP value and return 'Valid' or 'Invalid'.
        """
        return "Valid" if float(dop_value) < 99.99 else "Invalid"

class QTMCFGFIXRATE(QTM):
    """
    PQTMCFGFIXRATE Message

    Supports:
    - $PQTMCFGFIXRATE,OK*<Checksum><CR><LF> (Successful Set Response)

    Attributes:
    - sentence_type: CFGFIXRATE (always)
    - status: OK (indicates a successful set)
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "CFGFIXRATE"
        ('status', 'status')     # Always "OK"
    )

    def __init__(self, manufacturer, data):
        super(QTMCFGFIXRATE, self).__init__(manufacturer, data)
        # print(data)  # Debugging print to confirm input structure

        # Assign the parsed data to attributes
        self.sentence_type = data[0]  # "CFGFIXRATE"
        self.status = data[1]   # "OK"

class QTMVEL(QTM):
    """
    PQTMVEL Message

    Outputs the velocity information.

    Supports:
    - $PQTMVEL,<Time>,<VelN>,<VelE>,<VelD>,<GrdSpd>,<Spd>,<Heading>,<GrdSpdAcc>,<SpdAcc>,<HeadingAcc>*<Checksum><CR><LF>

    Attributes:
    - time: UTC time (hhmmss.sss)
    - vel_n: North velocity in m/s
    - vel_e: East velocity in m/s
    - vel_d: Down velocity in m/s
    - grd_spd: 2D speed in m/s
    - spd: 3D speed in m/s
    - heading: Heading in degrees (0.00 - 360.00)
    - grd_spd_acc: Estimate of 2D speed accuracy in m/s
    - spd_acc: Estimate of 3D speed accuracy in m/s
    - heading_acc: Estimate of heading accuracy in degrees
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "VEL"
        ('msg_ver', 'msg_ver'),  # Message version (Always 1)
        ('time', 'time'),  # UTC time (hhmmss.sss)
        ('vel_n', 'vel_n'),  # North velocity (m/s)
        ('vel_e', 'vel_e'),  # East velocity (m/s)
        ('vel_d', 'vel_d'),  # Down velocity (m/s)
        ('grd_spd', 'grd_spd'),  # 2D speed (m/s)
        ('spd', 'spd'),  # 3D speed (m/s)
        ('heading', 'heading'),  # Heading (degrees)
        ('grd_spd_acc', 'grd_spd_acc'),  # 2D speed accuracy (m/s)
        ('spd_acc', 'spd_acc'),  # 3D speed accuracy (m/s)
        ('heading_acc', 'heading_acc')  # Heading accuracy (degrees)
    )

    def __init__(self, manufacturer, data):
        super(QTMVEL, self).__init__(manufacturer, data)
        # print(data)  # Debugging print to confirm input structure

        # Assign parsed values to attributes
        self.sentence_type = data[0]
        self.version = data[1]
        self.time = data[2]
        self.vel_n = float(data[3])
        self.vel_e = float(data[4])
        self.vel_d = float(data[5])
        self.grd_spd = float(data[6])
        self.spd = float(data[7])
        self.heading = float(data[8])
        self.grd_spd_acc = float(data[9])
        self.spd_acc = float(data[10])
        self.heading_acc = float(data[11])

class QTMCFGODO(QTM):
    """
    PQTMCFGODO Message

    Supports:
    - $PQTMCFGODO,OK,<State>,<InitDist>*<Checksum><CR><LF>

    Odometer Feature Configuration:
    - State: 0 = Disabled, 1 = Enabled
    - InitDist: Initial distance (meters), default value is 0.
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "CFGODO"
        ('status', 'status'),  # "OK"
        ('state', 'state'),  # 0 = Disabled, 1 = Enabled
        ('init_dist', 'init_dist')  # Initial distance in meters
    )

    def __init__(self, manufacturer, data):
        super(QTMCFGODO, self).__init__(manufacturer, data)
        # print(data)  # Debugging print to confirm input structure

        # Assign fields for the successful set response
        self.sentence_type = data[0]  # Should always be "CFGODO"
        self.status = data[1]  # Should be "OK"
        self.state = data[2]  # Odometer state: 0 = Disabled, 1 = Enabled
        self.init_dist = data[3]  # Initial distance in meters

    def get_state_description(self):
        """
        Get the description of the odometer state.
        """
        state_map = {
            "0": "Disabled",
            "1": "Enabled"
        }
        return state_map.get(self.state, "Unknown state")

class QTMODO(QTM):
    """
    PQTMODO Message

    Outputs the odometer information.

    Supports:
    - $PQTMODO,<MsgVer>,<Time>,<State>,<Dist>*<Checksum><CR><LF>

    Fields:
    - MsgVer: Message version (Always 1).
    - Time: UTC time (hhmmss.sss).
    - State: Odometer status (0 = Disabled, 1 = Enabled).
    - Dist: Distance since last reset (meters).
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "MODO"
        ('msg_ver', 'msg_ver'),  # Message version (1)
        ('time', 'time'),  # UTC time (hhmmss.sss)
        ('state', 'state'),  # Odometer state: 0 = Disabled, 1 = Enabled
        ('dist', 'dist')  # Distance since last reset (meters)
    )

    def __init__(self, manufacturer, data):
        super(QTMODO, self).__init__(manufacturer, data)
        # print(data)  # Debugging print to confirm input structure

        # Assign the parsed fields
        self.sentence_type = data[0]  # Should always be "MODO"
        self.msg_ver = data[1]  # Always 1
        self.time = data[2]  # UTC time in hhmmss.sss format
        self.state = data[3]  # Odometer state
        self.dist = data[4]  # Distance since last reset in meters

    def get_state_description(self):
        """
        Get the description of the odometer state.
        """
        state_map = {
            "0": "Disabled",
            "1": "Enabled"
        }
        return state_map.get(self.state, "Unknown state")

class QTMLS(QTM):
    """
    PQTMLS Message

    Supports:
    - $PQTMLS,<MsgVer>,<TOW>,<LS_Ref>,<WN>,<LS>,<Flag>,<LSF_Ref>,<Reserved>,<WNLSF>,<DN>,<LSF>*<Checksum>

    Field Descriptions:
    - MsgVer: Message version (Always 1)
    - TOW: Time of week in seconds
    - LS_Ref: Referenced constellation for current leap second information
    - WN: UTC reference week number
    - LS: Current number of leap seconds since January 6, 1980
    - Flag: Marker for future occurrences of leap seconds
    - LSF_Ref: Constellation for the leap second forecast
    - Reserved: Always null
    - WNLSF: Week number of the new leap second
    - DN: Day of the week when the leap second takes effect
    - LSF: Leap second count after future changes
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "MLS"
        ('MsgVer', 'msg_ver'),  # Message version
        ('TOW', 'tow'),  # Time of week
        ('LS_Ref', 'ls_ref'),  # Leap second reference
        ('WN', 'wn'),  # UTC reference week number
        ('LS', 'ls'),  # Current number of leap seconds
        ('Flag', 'flag'),  # Leap second availability flag
        ('LSF_Ref', 'lsf_ref'),  # Leap second forecast reference
        ('Reserved', 'reserved'),  # Reserved field
        ('WNLSF', 'wnlsf'),  # Week number of the new leap second
        ('DN', 'dn'),  # Day of the week for the new leap second
        ('LSF', 'lsf')  # Leap second count after future changes
    )

    def __init__(self, manufacturer, data):
        super(QTMLS, self).__init__(manufacturer, data)
        # Assign the parsed fields
        self.sentence_type = "MLS"
        self.msg_ver = data[1]  # Message version
        self.tow = data[2]  # Time of week
        self.ls_ref = self.parse_constellation(data[3])  # Leap second reference constellation
        self.wn = data[4]  # UTC reference week number
        self.ls = data[5]  # Current number of leap seconds
        self.flag = "Available" if data[6] == "1" else "Invalid"  # Leap second flag
        self.lsf_ref = self.parse_constellation(data[7])  # Leap second forecast reference
        self.reserved = data[8]  # Reserved field (null)
        self.wnlsf = data[9]  # Week number of the new leap second
        self.dn = data[10]  # Day of the week for the new leap second
        self.lsf = data[11]  # Leap second count after future changes

    @staticmethod
    def parse_constellation(value):
        """
        Parse the constellation reference and return the corresponding description.
        """
        constellation_map = {
            "0": "No source",
            "1": "GPS",
            "2": "Reserved",
            "3": "Galileo",
            "4": "BDS"
        }
        return constellation_map.get(value, "Unknown")

class QTMDRCAL(QTM):
    """
    PQTMDRCAL Message

    Supports:
    - $PQTMDRCAL,<MsgVer>,<CalState>,<NavType>*<Checksum>

    Field Descriptions:
    - MsgVer: Message version (Always 1)
    - CalState: DR calibration state
        - 0 = Not calibrated
        - 1 = DR is lightly calibrated
        - 2 = DR is fully calibrated
        - 3 = DR is fully calibrated with high-precision heading
    - NavType: Navigation type
        - 0 = No position
        - 1 = GNSS only
        - 2 = DR only
        - 3 = Combination (GNSS + DR)
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "DRCAL"
        ('MsgVer', 'msg_ver'),  # Message version
        ('CalState', 'cal_state'),  # DR calibration state
        ('NavType', 'nav_type')  # Navigation type
    )

    def __init__(self, manufacturer, data):
        super(QTMDRCAL, self).__init__(manufacturer, data)
        # Assign the parsed fields
        self.sentence_type = "DRCAL"
        self.msg_ver = data[1]  # Message version
        self.cal_state = self.parse_cal_state(data[2])  # DR calibration state
        self.nav_type = self.parse_nav_type(data[3])  # Navigation type

    @staticmethod
    def parse_cal_state(value):
        """
        Parse the calibration state and return the corresponding description.
        """
        cal_state_map = {
            "0": "Not calibrated",
            "1": "DR is lightly calibrated",
            "2": "DR is fully calibrated",
            "3": "DR is fully calibrated with high-precision heading"
        }
        return cal_state_map.get(value, "Unknown")

    @staticmethod
    def parse_nav_type(value):
        """
        Parse the navigation type and return the corresponding description.
        """
        nav_type_map = {
            "0": "No position",
            "1": "GNSS only",
            "2": "DR only",
            "3": "Combination (GNSS + DR)"
        }
        return nav_type_map.get(value, "Unknown")

class QTMIMUTYPE(QTM):
    """
    PQTMIMUTYPE Message

    Supports:
    - $PQTMIMUTYPE,<MsgVer>,<Status>*<Checksum>

    Field Descriptions:
    - MsgVer: Message version (Always 1)
    - Status: IMU initialization status
        - 0 = IMU initialization failed
        - Others = IMU initialization successful
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "IMUTYPE"
        ('MsgVer', 'msg_ver'),  # Message version
        ('Status', 'status')  # IMU initialization status
    )

    def __init__(self, manufacturer, data):
        super(QTMIMUTYPE, self).__init__(manufacturer, data)
        # Assign the parsed fields
        self.sentence_type = "IMUTYPE"
        self.msg_ver = data[1]  # Message version
        self.status = self.parse_status(data[2])  # IMU initialization status

    @staticmethod
    def parse_status(value):
        """
        Parse the IMU initialization status and return the corresponding description.
        """
        return "IMU initialization failed" if value == "0" else "IMU initialization successful"

class QTMVEHMSG(QTM):
    """
    PQTMVEHMSG Message

    Supports:
    - $PQTMVEHMSG,<MsgVer>,<Timestamp>,<Param1>,<Param2>,...,<ParamN>*<Checksum>

    Field Descriptions:
    - MsgVer: Message version indicating the type of vehicle information
        - 1: Vehicle speed (in m/s)
        - 2: Cumulative wheel ticks
        - 3: Speeds of four wheels (in m/s)
        - 4: Cumulative wheel ticks of four wheels
    - Timestamp: Time since power-on in milliseconds
    - Parameters: Vary depending on MsgVer
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "VEHMSG"
        ('MsgVer', 'msg_ver'),  # Message version
        ('Timestamp', 'timestamp')  # Timestamp since power-on
    )

    def __init__(self, manufacturer, data):
        super(QTMVEHMSG, self).__init__(manufacturer, data)
        self.sentence_type = "VEHMSG"
        self.msg_ver = data[1]  # Message version
        self.timestamp = data[2]  # Timestamp in milliseconds

        # Parse parameters based on MsgVer
        self.parameters = self.parse_parameters(data[3:], self.msg_ver)

    def parse_parameters(self, params, msg_ver):
        """
        Parse parameters based on MsgVer.
        """
        if msg_ver == "1":
            return {"VehSpeed": float(params[0])}  # Speed in m/s
        elif msg_ver == "2":
            return {
                "WheelTickCNT": int(params[0]),  # Cumulative wheel ticks
                "FWD_Ind": self.parse_fwd_ind(int(params[1]))  # Forward/backward indicator
            }
        elif msg_ver == "3":
            return {
                "LF_Spd": float(params[0]),  # Left front wheel speed
                "RF_Spd": float(params[1]),  # Right front wheel speed
                "LR_Spd": float(params[2]),  # Left rear wheel speed
                "RR_Spd": float(params[3])   # Right rear wheel speed
            }
        elif msg_ver == "4":
            return {
                "LF_TickCNT": int(params[0]),  # Left front wheel tick count
                "RF_TickCNT": int(params[1]),  # Right front wheel tick count
                "LR_TickCNT": int(params[2]),  # Left rear wheel tick count
                "RR_TickCNT": int(params[3]),  # Right rear wheel tick count
                "FWD_Ind": self.parse_fwd_ind(int(params[4]))  # Forward/backward indicator
            }
        else:
            return {}

    @staticmethod
    def parse_fwd_ind(value):
        """
        Parse the forward/backward indicator.
        """
        fwd_ind_map = {
            0: "Invalid state",
            1: "Forward",
            2: "Backward"
        }
        return fwd_ind_map.get(value, "Unknown")

class QTMINS(QTM):
    """
    PQTMINS Message

    Supports:
    - $PQTMINS,<Timestamp>,<SolType>,<Lat>,<Lon>,<Height>,<VEL_N>,<VEL_E>,<VEL_D>,<Roll>,<Pitch>,<Yaw>*<Checksum>

    Field Descriptions:
    - Timestamp: Time since power-on in milliseconds
    - SolType: Solution type
        - 0 = DR not ready. Roll and pitch ready.
        - 1 = DR not ready. GNSS, roll, pitch, and relative heading ready.
        - 2 = GNSS + DR mode. DR calibrated.
        - 3 = DR only mode.
    - Lat: Latitude in degrees
    - Lon: Longitude in degrees
    - Height: Height in meters
    - VEL_N: Northward velocity in m/s
    - VEL_E: Eastward velocity in m/s
    - VEL_D: Downward velocity in m/s
    - Roll: Roll angle in degrees, range: -180.0 to 180.0
    - Pitch: Pitch angle in degrees, range: -90.0 to 90.0
    - Yaw: Heading angle in degrees, range: 0.0 to 360.0
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "INS"
        ('Timestamp', 'timestamp'),  # Time since power-on
        ('SolType', 'sol_type'),  # Solution type
        ('Lat', 'latitude'),  # Latitude
        ('Lon', 'longitude'),  # Longitude
        ('Height', 'height'),  # Height in meters
        ('VEL_N', 'vel_n'),  # Northward velocity
        ('VEL_E', 'vel_e'),  # Eastward velocity
        ('VEL_D', 'vel_d'),  # Downward velocity
        ('Roll', 'roll'),  # Roll angle
        ('Pitch', 'pitch'),  # Pitch angle
        ('Yaw', 'yaw')  # Heading angle
    )

    def __init__(self, manufacturer, data):
        super(QTMINS, self).__init__(manufacturer, data)
        # Assign the parsed fields
        self.sentence_type = "INS"
        self.timestamp = int(data[1])  # Timestamp in milliseconds
        self.sol_type = self.parse_solution_type(int(data[2]))  # Solution type
        self.latitude = float(data[3])  # Latitude
        self.longitude = float(data[4])  # Longitude
        self.height = float(data[5])  # Height in meters
        self.vel_n = float(data[6])  # Northward velocity
        self.vel_e = float(data[7])  # Eastward velocity
        self.vel_d = float(data[8])  # Downward velocity
        self.roll = float(data[9])  # Roll angle
        self.pitch = float(data[10])  # Pitch angle
        self.yaw = float(data[11])  # Heading angle

    @staticmethod
    def parse_solution_type(value):
        """
        Parse the solution type and return the corresponding description.
        """
        solution_type_map = {
            0: "DR not ready. Roll and pitch ready.",
            1: "DR not ready. GNSS, roll, pitch, and relative heading ready.",
            2: "GNSS + DR mode. DR calibrated.",
            3: "DR only mode."
        }
        return solution_type_map.get(value, "Unknown")

class QTMGPS(QTM):
    """
    PQTMGPS Message

    Supports:
    - $PQTMGPS,<Timestamp>,<TOW>,<Lat>,<Lon>,<Altitude>,<Speed>,<Heading>,<Accuracy>,<HDOP>,<PDOP>,<NumSatUsed>,<FixMode>*<Checksum>

    Field Descriptions:
    - Timestamp: Time since power-on in milliseconds (string)
    - TOW: Time of week in seconds (string)
    - Lat: Latitude in degrees (string)
    - Lon: Longitude in degrees (string)
    - Altitude: Altitude in meters (string)
    - Speed: Ground speed in m/s (string)
    - Heading: Heading of vehicle in degrees (string)
    - Accuracy: Horizontal accuracy estimate in meters (string)
    - HDOP: Horizontal dilution of precision (string)
    - PDOP: Position dilution of precision (string)
    - NumSatUsed: Number of satellites used in navigation (string)
    - FixMode: Fix mode (string)
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "GPS"
        ('Timestamp', 'timestamp'),  # Time since power-on
        ('TOW', 'tow'),  # Time of week
        ('Lat', 'latitude'),  # Latitude
        ('Lon', 'longitude'),  # Longitude
        ('Altitude', 'altitude'),  # Altitude in meters
        ('Speed', 'speed'),  # Ground speed in m/s
        ('Heading', 'heading'),  # Heading in degrees
        ('Accuracy', 'accuracy'),  # Horizontal accuracy in meters
        ('HDOP', 'hdop'),  # Horizontal dilution of precision
        ('PDOP', 'pdop'),  # Position dilution of precision
        ('NumSatUsed', 'num_sat_used'),  # Number of satellites used
        ('FixMode', 'fix_mode')  # Fix mode
    )

    def __init__(self, manufacturer, data):
        super(QTMGPS, self).__init__(manufacturer, data)
        # Assign the parsed fields, keeping them as strings
        self.sentence_type = "GPS"
        self.timestamp = data[1]  # Timestamp as string
        self.tow = data[2]  # Time of week as string
        self.latitude = data[3]  # Latitude as string
        self.longitude = data[4]  # Longitude as string
        self.altitude = data[5]  # Altitude as string
        self.speed = data[6]  # Speed as string
        self.heading = data[7]  # Heading as string
        self.accuracy = data[8]  # Accuracy as string
        self.hdop = data[9]  # HDOP as string
        self.pdop = data[10]  # PDOP as string
        self.num_sat_used = data[11]  # NumSatUsed as string
        self.fix_mode = self.parse_fix_mode(data[12])  # FixMode as string

    @staticmethod
    def parse_fix_mode(value):
        """
        Parse the fix mode and return the corresponding description.
        """
        fix_mode_map = {
            "0": "No fix",
            "2": "2D fix",
            "3": "3D fix (including RTK float or RTK fixed)"
        }
        return fix_mode_map.get(value, "Unknown")

class QTMVEHMOT(QTM):
    """
    PQTMVEHMOT Message

    Supports:
    - Version 1: $PQTMVEHMOT,1,<PeakAcceleration>,<PeakAngularRate>*<Checksum>
    - Version 2: $PQTMVEHMOT,2,<UTC>,<VehType>,<MotState>,<AccStatus>,<TurningStatus>,<Res0>,<Res1>,<Res2>,<Res3>,<Res4>*<Checksum>

    Field Descriptions:
    - MsgVer: Message version (1 or 2)
    - Version 1:
        - PeakAcceleration: Peak acceleration of the vehicle (string)
        - PeakAngularRate: Peak angular rate of the vehicle (string)
    - Version 2:
        - UTC: UTC time in hhmmss.sss format (string)
        - VehType: Vehicle type (1 to 4, string)
        - MotState: Motion state of the vehicle (string)
        - AccStatus: Vehicle acceleration status (string)
        - TurningStatus: Vehicle turning status (string)
        - Res0 to Res4: Reserved fields, always null (string)
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "VEHMOT"
        ('MsgVer', 'msg_ver'),  # Message version
    )

    def __init__(self, manufacturer, data):
        super(QTMVEHMOT, self).__init__(manufacturer, data)
        self.sentence_type = "VEHMOT"
        self.msg_ver = data[1]  # Message version

        if self.msg_ver == "1":
            # Version 1: Peak Acceleration and Angular Rate
            self.peak_acceleration = data[2]  # Peak acceleration as string
            self.peak_angular_rate = data[3]  # Peak angular rate as string
        elif self.msg_ver == "2":
            # Version 2: Detailed Vehicle Motion Information
            self.utc = data[2]  # UTC time as string
            self.veh_type = data[3]  # Vehicle type as string
            self.mot_state = data[4]  # Motion state as string
            self.acc_status = data[5]  # Acceleration status as string
            self.turning_status = data[6]  # Turning status as string
            self.reserved = data[7:12]  # Reserved fields as list of strings

    def parse_veh_type(self):
        """
        Parse the vehicle type and return the description.
        """
        veh_type_map = {
            "1": "General-purpose vehicle",
            "2": "Small vehicle",
            "3": "Medium vehicle",
            "4": "Large vehicle"
        }
        return veh_type_map.get(self.veh_type, "Unknown")

    def parse_mot_state(self):
        """
        Parse the motion state and return the description.
        """
        mot_state_map = {
            "1": "Stopped",
            "2": "Moving"
        }
        return mot_state_map.get(self.mot_state, "Unknown")

    def parse_acc_status(self):
        """
        Parse the acceleration status and return the description.
        """
        acc_status_map = {
            "1": "None (No acceleration detected)",
            "2": "Normal acceleration",
            "3": "Rapid acceleration",
            "4": "Normal deceleration",
            "5": "Rapid deceleration"
        }
        return acc_status_map.get(self.acc_status, "Unknown")

    def parse_turning_status(self):
        """
        Parse the turning status and return the description.
        """
        turning_status_map = {
            "1": "None (No turning motion detected)",
            "2": "Normal turn left",
            "3": "Sharp turn left",
            "4": "Normal turn right",
            "5": "Sharp turn right"
        }
        return turning_status_map.get(self.turning_status, "Unknown")

class QTMSENMSG(QTM):
    """
    PQTMSENMSG Message

    Supports:
    - MsgVer = 2: $PQTMSENMSG,2,<TimeStamp>,<IMU_Temp>,<IMU_GYRO_X>,<IMU_GYRO_Y>,<IMU_GYRO_Z>,<IMU_ACC_X>,<IMU_ACC_Y>,<IMU_ACC_Z>*<Checksum>
    - MsgVer = 4: $PQTMSENMSG,4,<TimeStamp>,<IMU_Temp>,<IMU_GYRO_X>,<IMU_GYRO_Y>,<IMU_GYRO_Z>,<IMU_ACC_X>,<IMU_ACC_Y>,<IMU_ACC_Z>*<Checksum>

    Field Descriptions:
    - MsgVer: Message version (2 or 4)
    - TimeStamp: Time since power-on in milliseconds (string)
    - IMU_Temp: IMU temperature in Celsius (string)
    - IMU_GYRO_X/Y/Z: IMU gyroscope values for X, Y, Z axes in degrees per second (string)
    - IMU_ACC_X/Y/Z: IMU accelerometer values for X, Y, Z axes in g (string)
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "SENMSG"
        ('MsgVer', 'msg_ver'),  # Message version
    )

    def __init__(self, manufacturer, data):
        super(QTMSENMSG, self).__init__(manufacturer, data)
        self.sentence_type = "SENMSG"
        self.msg_ver = data[1]  # Message version

        if self.msg_ver in ["2", "4"]:
            # Common fields for both MsgVer = 2 and 4
            self.timestamp = data[2]  # Time since power-on as string
            self.imu_temp = data[3]  # IMU temperature as string
            self.imu_gyro_x = data[4]  # IMU gyroscope X-axis as string
            self.imu_gyro_y = data[5]  # IMU gyroscope Y-axis as string
            self.imu_gyro_z = data[6]  # IMU gyroscope Z-axis as string
            self.imu_acc_x = data[7]  # IMU accelerometer X-axis as string
            self.imu_acc_y = data[8]  # IMU accelerometer Y-axis as string
            self.imu_acc_z = data[9]  # IMU accelerometer Z-axis as string
        else:
            raise ValueError("Unsupported MsgVer: Only 2 and 4 are supported.")

class QTMDRPVA(QTM):
    """
    PQTMDRPVA Message

    Supports:
    - $PQTMDRPVA,<MsgVer>,<Timestamp>,<Time>,<SolType>,<Lat>,<Lon>,<Alt>,<Sep>,<VelN>,<VelE>,<VelD>,<Spd>,<Roll>,<Pitch>,<Heading>*<Checksum>

    Field Descriptions:
    - MsgVer: Message version (Always 1 for this version)
    - Timestamp: Milliseconds since module turn-on (string)
    - Time: UTC time in hhmmss.sss format (string)
    - SolType: Solution type (0 = No fix, 1 = GNSS only, 2 = Combination (GNSS + DR), 3 = DR only) (string)
    - Lat: Latitude in degrees (string)
    - Lon: Longitude in degrees (string)
    - Alt: Altitude in meters (string)
    - Sep: Geoidal separation in meters (string)
    - VelN: North velocity in m/s (string)
    - VelE: East velocity in m/s (string)
    - VelD: Down velocity in m/s (string)
    - Spd: Ground speed in m/s (string)
    - Roll: Roll angle in degrees, range: -180.000000 to 180.000000 (string)
    - Pitch: Pitch angle in degrees, range: -90.000000 to 90.000000 (string)
    - Heading: Heading in degrees, range: 0.000000 to 360.000000 (string)
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "DRPVA"
        ('MsgVer', 'msg_ver'),  # Message version
        ('Timestamp', 'timestamp'),  # Milliseconds since turn-on
        ('Time', 'time'),  # UTC time
        ('SolType', 'sol_type'),  # Solution type
        ('Lat', 'latitude'),  # Latitude
        ('Lon', 'longitude'),  # Longitude
        ('Alt', 'altitude'),  # Altitude
        ('Sep', 'sep'),  # Geoidal separation
        ('VelN', 'vel_n'),  # North velocity
        ('VelE', 'vel_e'),  # East velocity
        ('VelD', 'vel_d'),  # Down velocity
        ('Spd', 'speed'),  # Ground speed
        ('Roll', 'roll'),  # Roll angle
        ('Pitch', 'pitch'),  # Pitch angle
        ('Heading', 'heading')  # Heading
    )

    def __init__(self, manufacturer, data):
        super(QTMDRPVA, self).__init__(manufacturer, data)
        self.sentence_type = "DRPVA"
        self.msg_ver = data[1]  # Message version as string
        self.timestamp = data[2]  # Timestamp as string
        self.time = data[3]  # UTC time as string
        self.sol_type = self.parse_solution_type(data[4])  # Parse Solution type
        self.latitude = data[5]  # Latitude as string
        self.longitude = data[6]  # Longitude as string
        self.altitude = data[7]  # Altitude as string
        self.sep = data[8]  # Geoidal separation as string
        self.vel_n = data[9]  # North velocity as string
        self.vel_e = data[10]  # East velocity as string
        self.vel_d = data[11]  # Down velocity as string
        self.speed = data[12]  # Ground speed as string
        self.roll = data[13]  # Roll angle as string
        self.pitch = data[14]  # Pitch angle as string
        self.heading = data[15]  # Heading as string

    @staticmethod
    def parse_solution_type(value):
        """
        Parse the solution type and return the corresponding description.
        """
        sol_type_map = {
            "0": "No fix",
            "1": "GNSS only",
            "2": "Combination (GNSS + DR)",
            "3": "DR only"
        }
        return sol_type_map.get(value, "Unknown")

class QTMVEHATT(QTM):
    """
    PQTMVEHATT Message

    Supports:
    - $PQTMVEHATT,<MsgVer>,<Timestamp>,<Roll>,<Pitch>,<Heading>,<Acc_Roll>,<Acc_Pitch>,<Acc_Heading>*<Checksum>

    Field Descriptions:
    - MsgVer: Message version (Always 1 for this version)
    - Timestamp: Milliseconds since power-on (string)
    - Roll: Vehicle roll angle in degrees, range: -180.000000 to 180.000000 (string)
    - Pitch: Vehicle pitch angle in degrees, range: -90.000000 to 90.000000 (string)
    - Heading: Vehicle heading angle in degrees, range: 0.000000 to 360.000000 (string)
    - Acc_Roll: Vehicle roll accuracy in degrees, range: 0.000000 to 360.000000 (string)
    - Acc_Pitch: Vehicle pitch accuracy in degrees, range: 0.000000 to 180.000000 (string)
    - Acc_Heading: Vehicle heading accuracy in degrees, range: 0.000000 to 360.000000 (string)
    """

    fields = (
        ('sentence_type', 'sentence_type'),  # Always "VEHATT"
        ('MsgVer', 'msg_ver'),  # Message version
        ('Timestamp', 'timestamp'),  # Milliseconds since power-on
        ('Roll', 'roll'),  # Roll angle
        ('Pitch', 'pitch'),  # Pitch angle
        ('Heading', 'heading'),  # Heading angle
        ('Acc_Roll', 'acc_roll'),  # Roll accuracy
        ('Acc_Pitch', 'acc_pitch'),  # Pitch accuracy
        ('Acc_Heading', 'acc_heading')  # Heading accuracy
    )

    def __init__(self, manufacturer, data):
        super(QTMVEHATT, self).__init__(manufacturer, data)
        self.sentence_type = "VEHATT"
        self.msg_ver = data[1]  # Message version as string
        self.timestamp = data[2]  # Timestamp as string
        self.roll = data[3]  # Roll angle as string
        self.pitch = data[4]  # Pitch angle as string
        self.heading = data[5]  # Heading angle as string
        self.acc_roll = data[6]  # Roll accuracy as string
        self.acc_pitch = data[7]  # Pitch accuracy as string
        self.acc_heading = data[8]  # Heading accuracy as string
