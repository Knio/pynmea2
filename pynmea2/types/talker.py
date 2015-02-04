from ..nmea import TalkerSentence
from ..nmea_utils import *
from decimal import Decimal

class AAM(TalkerSentence):
    """ Waypoint Arrival Alarm
    """
    fields = (
        ("Arrival Circle Entered", "arrival_circ_entered"),
        ("Perpendicular Passed", "perp_passed"),
        ("Circle Radius", "circle_rad"),
        ("Nautical Miles", "circle_rad_unit"),
        ("Waypoint ID", "waypoint_id")
    )

class ALM(TalkerSentence):
    """ GPS Almanac data
    """
    fields = (
        ("Total number of messages", "total_num_msgs"),
        ("Message number", "msg_num"),
        ("Satellite PRN number", "sat_prn_num"), # 01 - 32
        ("GPS week number", "gps_week_num"), # Week since Jan 6 1980
        ("SV Health, bits 17-24 of each almanac page", "sv_health"),
        ("Eccentricity", "eccentricity"),
        ("Almanac Reference Time", "alamanac_ref_time"),
        ("Inclination Angle", "inc_angle"),
        ("Rate of right ascension", "rate_right_asc"),
        ("Root of semi-major axis", "root_semi_major_axis"),
        ("Argument of perigee", "arg_perigee"),
        ("Longitude of ascension node", "lat_asc_node"),
        ("Mean anomaly", "mean_anom"),
        ("F0 Clock parameter", "f0_clock_param"),
        ("F1 Clock parameter", "f1_clock_param")
    )


class APA(TalkerSentence):
    """ Autopilot Sentence "A"
    """

    fields = (
        ("General Status", "status_gen"),
        ("Cycle lock Status", "status_cycle_lock"),
        ("Cross Track Error Magnitude", "cross_track_err_mag"),
        ("Direction to Steer (L or R)", "dir_steer"),
        ("Cross Track Units (Nautical Miles or KM)", "cross_track_unit"),
        ("Arrival Circle Entered", "arr_circle_entered"), # A = True
        ("Perpendicular passed at waypoint", "perp_passed"), # A = True
        ("Bearing origin to destination", "bearing_to_dest"),
        ("Bearing type", "bearing_type"), # M = Magnetic, T = True
        ("Destination waypoint ID", "dest_waypoint_id")
    )


class APB(TalkerSentence):
    """ Autopilot Sentence "B"
    """

    fields = (
        ("General Status", "status_gen"),
        ("Cycle lock Status", "status_cycle_lock"),
        ("Cross Track Error Magnitude", "cross_track_err_mag"),
        ("Direction to Steer (L or R)", "dir_steer"),
        ("Cross Track Units (Nautical Miles or KM)", "cross_track_unit"),
        ("Arrival Circle Entered", "arr_circle_entered"), # A = True
        ("Perpendicular passed at waypoint", "perp_passed"), # A = True
        ("Bearing origin to destination", "bearing_to_dest"),
        ("Bearing type", "bearing_type"), # M = Magnetic, T = True
        ("Destination waypoint ID", "dest_waypoint_id"),
        ("Bearing, present position to dest", "bearing_pres_dest"),
        ("Bearing to destination, type", "bearing_pres_dest_type"), # M = Magnetic, T = True
        ("Heading to steer to destination", "heading_to_dest"),
        ("Heading to steer to destination type", "heading_to_dest_type")
    ) # M = Magnetic, T = True


class BEC(TalkerSentence):
    """ Bearing & Distance to Waypoint, Dead Reckoning
    """
    fields = (
        ("Timestamp", "timestamp", timestamp),
        ("Waypoint Latitude", "waypoint_lat"),
        ("Waypoint Latitude direction", "waypoint_lat_dir"),
        ("Waypoint Longitude", "waypoint_lon"),
        ("Waypoint Longitude direction", "waypoint_lon_dir"),
        ("Bearing, true", "bearing_true"),
        ("Bearing True symbol", "bearing_true_sym"), # T = true
        ("Bearing Magnetic", "bearing_mag"),
        ("Bearing Magnetic symbol", "bearing_mag_sym"),
        ("Nautical Miles", "nautical_miles"),
        ("Nautical Miles symbol", "nautical_miles_sym"),
        ("Waypoint ID", "waypoint_id"),
        ("FAA mode indicator", "faa_mode")
    )


class BOD(TalkerSentence):
    # 045.
    # ,T,023.,M,DEST,START
    fields = (
        ('Bearing True', 'bearing_t', Decimal),
        ('Bearing True Type', 'bearing_t_type'),
        ('Bearing Magnetic', 'bearing_mag', Decimal),
        ('Bearing Magnetic Type', 'bearing_mag_type'),
        ('Destination', 'dest'),
        ('Start', 'start')
    )

    @property
    def bearing_true(self):
        return ','.join([self.bearing_t, self.bearing_t_type])

    @property
    def bearing_magnetic(self):
        return ','.join([self.bearing_mag, self.bearing_mag_type])

    @property
    def destination(self):
        return self.dest

    @property
    def origin(self):
        return self.start

class BWC(TalkerSentence):
    fields = (
        ('Timestamp', 'timestamp', timestamp),
        ('Latitude of next Waypoint', 'lat_next'),
        ('Latitude of next Waypoint Direction', 'lat_next_direction'),
        ('Longitude of next Waypoint', 'lon_next'),
        ('Longitude of next Waypoint Direction', 'lon_next_direction'),
        ('True track to waypoint', 'true_track'),
        ('True Track Symbol', 'true_track_sym'),
        ('Magnetic track to waypoint', 'mag_track'),
        ('Magnetic Symbol', 'mag_sym'),
        ('Range to waypoint', 'range_next'),
        ('Unit of range', 'range_unit'),
        ('Waypoint Name', 'waypoint_name')
    )

class BWR(TalkerSentence):
    fields = (
        ('Timestamp', 'timestamp', timestamp),
        ('Latitude of next Waypoint', 'lat_next'),
        ('Latitude of next Waypoint Direction', 'lat_next_direction'),
        ('Longitude of next Waypoint', 'lon_next'),
        ('Longitude of next Waypoint Direction', 'lon_next_direction'),
        ('True track to waypoint', 'true_track'),
        ('True Track Symbol', 'true_track_sym'),
        ('Magnetic track to waypoint', 'mag_track'),
        ('Magnetic Symbol', 'mag_sym'),
        ('Range to waypoint', 'range_next'),
        ('Unit of range', 'range_unit'),
        ('Waypoint Name', 'waypoint_name')
    )

class GGA(TalkerSentence, LatLonFix):
    fields = (
        ('Timestamp', 'timestamp', timestamp),
        ('Latitude', 'lat'),
        ('Latitude Direction', 'lat_dir'),
        ('Longitude', 'lon'),
        ('Longitude Direction', 'lon_dir'),
        ('GPS Quality Indicator', 'gps_qual'),
        ('Number of Satellites in use', 'num_sats'),
        ('Horizontal Dilution of Precision', 'horizontal_dil'),
        ('Antenna Alt above sea level (mean)', 'altitude', float),
        ('Units of altitude (meters)', 'altitude_units'),
        ('Geoidal Separation', 'geo_sep'),
        ('Units of Geoidal Separation (meters)', 'geo_sep_units'),
        ('Age of Differential GPS Data (secs)', 'age_gps_data'),
        ('Differential Reference Station ID', 'ref_station_id')
    )

class GNS(TalkerSentence, LatLonFix):
    fields = (
        ('Timestamp', 'timestamp', timestamp),
        ('Latitude', 'lat'),
        ('Latitude Direction', 'lat_dir'),
        ('Longitude', 'lon'),
        ('Longitude Direction', 'lon_dir'),
        ('Mode indicator', 'mode_inticator'),
        ('Total number of satelites in use', 'num_sats'),
        ('HDROP', 'hdop'),
        ('Antenna altitude, meters', 'altitude'),
        ('Goeidal separation meters', 'geo_sep'),
        ('Age of diferential data', 'age_gps_data'),
        ('Differential reference station ID', 'diferential')
    )

class BWW(TalkerSentence):
    """ Bearing, Waypoint to Waypoint
    """
    fields = (
        ("Bearing degrees True", "bearing_deg_true"),
        ("Bearing degrees True Symbol", "bearing_deg_true_sym"),
        ("Bearing degrees Magnitude", "bearing_deg_mag"),
        ("Bearing degrees Magnitude Symbol", "bearing_deg_mag_sym"),
        ("Destination Waypoint ID", "waypoint_id_dest"),
        ("Origin Waypoint ID", "waypoint_id_orig")
    )

class GLL(TalkerSentence, LatLonFix):
    fields = (
        ('Latitude', 'lat'),
        ('Latitude Direction', 'lat_dir'),
        ('Longitude', 'lon'),
        ('Longitude Direction', 'lon_dir'),
        ('Timestamp', 'timestamp', timestamp),
        ('Data Validity', "data_valid"),
        ("FAA mode indicator", "faa_mode")
    )

class GSA(TalkerSentence):
    fields = (
        ('Mode', 'mode'),
        ('Mode fix type', 'mode_fix_type'),
        ('SV ID01', 'sv_id01'),
        ('SV ID02', 'sv_id02'),
        ('SV ID03', 'sv_id03'),
        ('SV ID04', 'sv_id04'),
        ('SV ID05', 'sv_id05'),
        ('SV ID06', 'sv_id06'),
        ('SV ID07', 'sv_id07'),
        ('SV ID08', 'sv_id08'),
        ('SV ID09', 'sv_id09'),
        ('SV ID10', 'sv_id10'),
        ('SV ID11', 'sv_id11'),
        ('SV ID12', 'sv_id12'),
        ('PDOP (Dilution of precision)', 'pdop'),
        ('HDOP (Horizontal DOP)', 'hdop'),
        ('VDOP (Vertical DOP)', 'vdop')
            )


class GST(TalkerSentence):
    fields = (
        ('UTC time of the GGA or GNS fix associated with this sentence.', 'timestamp', timestamp),
        ('RMS value of the standard deviation of the range inputs to the navigation process. Range inputs include preudoranges & DGNSS corrections.', 'rms', float),
        ('Standard deviation of semi-major axis of error ellipse (meters)', 'std_dev_major', float),
        ('Standard deviation of semi-minor axis of error ellipse (meters)', 'std_dev_minor', float),
        ('Orientation of semi-major axis of error ellipse (degrees from true north)', 'orientation', float),
        ('Standard deviation of latitude error (meters)', 'std_dev_latitude', float),
        ('Standard deviation of longitude error (meters)', 'std_dev_longitude', float),
        ('Standard deviation of altitude error (meters)', 'std_dev_altitude', float),
    )


class GSV(TalkerSentence):
    fields = (
        ('Number of messages of type in cycle', 'num_messages'),
        ('Message Number', 'msg_num'),
        ('Total number of SVs in view', 'num_sv_in_view'),
        ('SV PRN number 1', 'sv_prn_num_1'),
        ('Elevation in degrees 1', 'elevation_deg_1'), # 90 max
        ('Azimuth, deg from true north 1', 'azimuth_1'), # 000 to 159
        ('SNR 1', 'snr_1'), # 00-99 dB
        ('SV PRN number 2', 'sv_prn_num_2'),
        ('Elevation in degrees 2', 'elevation_deg_2'), # 90 max
        ('Azimuth, deg from true north 2', 'azimuth_2'), # 000 to 159
        ('SNR 2', 'snr_2'), # 00-99 dB
        ('SV PRN number 3', 'sv_prn_num_3'),
        ('Elevation in degrees 3', 'elevation_deg_3'), # 90 max
        ('Azimuth, deg from true north 3', 'azimuth_3'), # 000 to 159
        ('SNR 3', 'snr_3'), # 00-99 dB
        ('SV PRN number 4', 'sv_prn_num_4'),
        ('Elevation in degrees 4', 'elevation_deg_4'), # 90 max
        ('Azimuth, deg from true north 4', 'azimuth_4'), # 000 to 159
        ('SNR 4', 'snr_4')
    )  # 00-99 dB


class HDG(TalkerSentence):
    """ NOTE! This is a GUESS as I cannot find an actual spec
        telling me the fields. Updates are welcome!
    """
    fields = (
        ("Heading", "heading", Decimal),
        ("Deviation", "deviation", Decimal),
        ("Deviation Direction", "dev_dir"),
        ("Variation", "variation", Decimal),
        ("Variation Direction", "var_dir")
    )


class HDT(TalkerSentence):
    fields = (
        ("Heading", "heading", Decimal),
        ("True", "hdg_true")
    )


class RMA(TalkerSentence):
    fields = (
        ("Data status", "data_status"),
        ("Latitude", "lat"),
        ("Latitude Direction", "lat_dir"),
        ("Longitude", "lon"),
        ("Longitude Direction", "lon_dir"),
        ("Not Used 1", "not_used_1"),
        ("Not Used 2", "not_used_2"),
        ("Speed over ground", "spd_over_grnd"), # Knots
        ("Course over ground", "crse_over_grnd"),
        ("Variation", "variation"),
        ("Variation Direction", "var_dir")
    )

class RMB(TalkerSentence):
    """ Recommended Minimum Navigation Information
    """
    fields = (
        ("Data Validity", "validity"),
        ("Cross Track Error", "cross_track_error"), # nautical miles, 9.9 max
        ("Cross Track Error, direction to corrent", "cte_correction_dir"),
        ("Origin Waypoint ID", "origin_waypoint_id"),
        ("Destination Waypoint ID", "dest_waypoint_id"),
        ("Destination Waypoint Latitude", "dest_lat"),
        ("Destination Waypoint Lat Direction", "dest_lat_dir"),
        ("Destination Waypoint Longitude", "dest_lon"),
        ("Destination Waypoint Lon Direction", "dest_lon_dir"),
        ("Range to Destination", "dest_range"), # Nautical Miles
        ("True Bearing to Destination", "dest_true_bearing"),
        ("Velocity Towards Destination", "dest_velocity"), # Knots
        ("Arrival Alarm", "arrival_alarm")
    ) # A = Arrived, V = Not arrived

class RMC(TalkerSentence, LatLonFix, DatetimeFix):
    """ Recommended Minimum Specific GPS/TRANSIT Data
    """
    fields = (
        ("Timestamp", "timestamp", timestamp),
        ("Data Validity", "data_validity"),
        ("Latitude", "lat"),
        ("Latitude Direction", "lat_dir"),
        ("Longitude", "lon"),
        ("Longitude Direction", "lon_dir"),
        ("Speed Over Ground", "spd_over_grnd", float),
        ("True Course", "true_course", float),
        ("Datestamp", "datestamp", datestamp),
        ("Magnetic Variation", "mag_variation"),
        ("Magnetic Variation Direction", "mag_var_dir")
    )

class RTE(TalkerSentence):
    """ Routes
    """
    fields = (
        ("Number of sentences in sequence", "num_in_seq"),
        ("Sentence Number", "sen_num"),
        ("Start Type", "start_type"), # The first in the list is either current route or waypoint
        ("Name or Number of Active Route", "active_route_id"),
    )

    @property
    def waypoint_list(self):
        return self.data[4:]

    @waypoint_list.setter
    def waypoint_list(self, val):
        self.data[4:] = val


class R00(TalkerSentence):
    fields = ()
    @property
    def waypoint_list(self):
        return self.data[:]

    @waypoint_list.setter
    def waypoint_list(self, val):
        self.data[:] = val


class STN(TalkerSentence):
    """ NOTE: No real data could be found for examples of the actual spec so
            it is a guess that there may be a checksum on the end
    """
    fields = (
        ("Talker ID Number", "talker_id_num"),
    ) # 00 - 99


class TRF(TalkerSentence):
    """ Transit Fix Data
    """
    fields = (
        ("Timestamp (UTC)", "timestamp", timestamp),
        ("Date (DD/MM/YY", "date"),
        ("Latitude", "lat"),
        ("Latitude Direction", "lat_dir"),
        ("Longitude", "lon"),
        ("Longitude Direction", "lon_dir"),
        ("Elevation Angle", "ele_angle"),
        ("Number of Iterations", "num_iterations"),
        ("Number of Doppler Intervals", "num_doppler_intervals"),
        ("Update Distance", "update_dist"), # Nautical Miles
        ("Satellite ID", "sat_id")
    )


class TXT(TalkerSentence):
    """ Text Transmission
    """
    fields = (
        ("Number of Messages", "num_msg"),
        ("Message Number", "msg_num"),
        ("Type of Message", "msg_type"),
        ("Text", "text")
    )


class VBW(TalkerSentence):
    """ Dual Ground/Water Speed
    """
    fields = (
        ("Longitudinal Water Speed", "lon_water_spd", Decimal), # Knots
        ("Transverse Water Speed", "trans_water_spd", Decimal), # Knots
        ("Water Speed Data Validity", "data_validity_water_spd"),
        ("Longitudinal Ground Speed", "lon_grnd_spd", Decimal), # Knots
        ("Transverse Ground Speed", "trans_grnd_spd", Decimal), # Knots
        ("Ground Speed Data Validity", "data_validity_grnd_spd")
    )

class VTG(TalkerSentence):
    """
    Track Made Good and Ground Speed
    """
    fields = (
        ("True Track made good", "true_track", float),
        ("True Track made good symbol", "true_track_sym"),
        ("Magnetic Track made good", "mag_track", Decimal),
        ("Magnetic Track symbol", "mag_track_sym"),
        ("Speed over ground knots", "spd_over_grnd_kts", Decimal),
        ("Speed over ground symbol", "spd_over_grnd_kts_sym"),
        ("Speed over ground kmph", "spd_over_grnd_kmph", float),
        ("Speed over ground kmph symbol", "spd_over_grnd_kmph_sym"),
        ("FAA mode indicator", "faa_mode")
    )


class WCV(TalkerSentence):
    """ Waypoint Closure Velocity
    """
    fields = (
        ("Velocity", "velocity"),
        ("Velocity Units", "vel_units"), # Knots
        ("Waypoint ID", "waypoint_id")
    )


class WNC(TalkerSentence):
    """ Distance, Waypoint to Waypoint
    """
    fields = (
        ("Distance, Nautical Miles", "dist_nautical_miles"),
        ("Distance Nautical Miles Unit", "dist_naut_unit"),
        ("Distance, Kilometers", "dist_km"),
        ("Distance, Kilometers Unit", "dist_km_unit"),
        ("Origin Waypoint ID", "waypoint_origin_id"),
        ("Destination Waypoint ID", "waypoint_dest_id")
    )


class WPL(TalkerSentence):
    """ Waypoint Location
    """
    fields = (
        ("Latitude", "lat"),
        ("Latitude Direction", "lat_dir"),
        ("Longitude", "lon"),
        ("Longitude Direction", "lon_dir"),
        ("Waypoint ID", "waypoint_id")
    )


class XTE(TalkerSentence):
    """ Cross-Track Error, Measured
    """
    fields = (
        ("General Warning Flag", "warning_flag"),
        ("Lock flag (Not Used)", "lock_flag"),
        ("Cross Track Error Distance", "cross_track_err_dist"),
        ("Correction Direction (L or R)", "correction_dir"),
        ("Distance Units", "dist_units")
    )


class ZDA(TalkerSentence):
    fields = (
        ("Timestamp", "timestamp", timestamp), # hhmmss.ss = UTC
        ("Day", "day", int), # 01 to 31
        ("Month", "month",  int), # 01 to 12
        ("Year", "year",  int), # Year = YYYY
        ("Local Zone Description", "local_zone",  int), # 00 to +/- 13 hours
        ("Local Zone Minutes Description", "local_zone_minutes",  int) # same sign as hours
    )

    @property
    def datestamp(self):
        return datetime.date(year=self.year, month=self.month, day=self.day)

    @property
    def tzinfo(self):
        return TZInfo(self.local_zone, self.local_zone_minutes)

    @property
    def datetime(self):
        d = datetime.datetime.combine(self.datestamp, self.timestamp)
        return d.replace(tzinfo=self.tzinfo)




# Implemented by Janez Stupar for Visionect
class RSA(TalkerSentence):
    """ Rudder Sensor Angle
    """
    fields = (
        ("Starboard rudder sensor","rsa_starboard", Decimal),
        ("Starboard rudder sensor status","rsa_starboard_status"),
        ("Port rudder sensor","rsa_port", Decimal),
        ("Port rudder sensor status","rsa_port_status"),
    )

class HSC(TalkerSentence):
    """ Heading Steering Command
    """
    fields = (

        ("Heading","heading_true", Decimal),
        ("True","true"),
        ("Heading Magnetic","heading_magnetic", Decimal),
        ("Magnetic","magnetic"),

    )
class MWD(TalkerSentence):
    """ Wind Direction
    NMEA 0183 standard Wind Direction and Speed, with respect to north.
    """
    fields = (
        ("Wind direction true","direction_true", Decimal),
        ("True","true"),
        ("Wind direction magnetic","direction_magnetic", Decimal),
        ("Magnetic","magnetic"),
        ("Wind speed knots","wind_speed_knots", Decimal),
        ("Knots","knots"),
        ("Wind speed meters/second","wind_speed_meters", Decimal),
        ("Wind speed","meters"),
    )

class MWV(TalkerSentence):
    """ Wind Speed and Angle
    NMEA 0183 standard Wind Speed and Angle, in relation to the vessel's
    bow/centerline.
    """
    fields = (
        ("Wind angle","wind_angle", Decimal), # in relation to vessel's centerline
        ("Reference","reference"), # relative (R)/true(T)
        ("Wind speed","wind_speed", Decimal),
        ("Wind speed units","wind_speed_units"), # K/M/N
        ("Status","status"),
    )

class DBT(TalkerSentence):
    """ Depth Below Transducer
    """
    fields = (
        ("Depth feet","depth_feet", Decimal),
        ("Feet","feet"),
        ("Depth meters","depth_meters", Decimal),
        ("Meters","meters"),
        ("Depth fathoms","depth_fathoms", Decimal),
        ("fathoms","fathoms"),
    )

class DPT(TalkerSentence):
    """ Depth of Water
    """
    fields = (
        ("Depth meters","depth", Decimal),
        ("Offset from transducer","offset", Decimal),
        ("Maximum range on scale","max_range", Decimal)
    )

class HDM(TalkerSentence):
    """
    Heading, Magnetic
    """
    fields = (
        ("Heading degrees","heading", Decimal),
        ("Magnetic","magnetic"),
    )

class MTW(TalkerSentence):
    """ Water Temperature
    """
    fields = (
        ('Water temperature','temperature', Decimal),
        ('Unit of measurement','units')
    )

class VHW(TalkerSentence):
    """ Water Speed and Heading
    """
    fields = (
        ('Heading true degrees','heading_true', Decimal),
        ('heading true','true'),
        ('Heading Magnetic degrees','heading_magnetic', Decimal),
        ('Magnetic','magnetic'),
        ('Water speed knots','water_speed_knots', Decimal),
        ('Knots','knots'),
        ('Water speed kilometers','water_speed_km', Decimal),
        ('Kilometers','kilometers'),
    )

class VLW(TalkerSentence):
    """ Distance Traveled through the Water
    """
    fields = (

        ('Water trip distance','trip_distance', Decimal),
        ('Trip distance nautical miles','trip_distance_miles'),
        ('Water trip distance since reset','trip_distance_reset', Decimal),
        ('Trip distance nautical miles since reset','trip_distance_reset_miles'),

    )
# --------------------- Implemented by Joachim Bakke (joabakk)---------------- #
# ---------------------------------------------------------------------------- #

class ROT(TalkerSentence):
    """ Rate of Turn
    """
    fields = (
        ("Rate of turn", "rate_of_turn"), #- indicates bow turn to port
        ("valid data","valid_data"), #A=valid data, B= invalid data
    )

class RPM(TalkerSentence):
    """ Revolutions
    """
#        1 2 3   4   5 6
#        | | |   |   | |
# $--RPM,a,x,x.x,x.x,A*hh<CR><LF>

# Field Number:
#  1) Sourse, S = Shaft, E = Engine
#  2) Engine or shaft number
#  3) Speed, Revolutions per minute
#  4) Propeller pitch, % of maximum, "-" means astern
#  5) Status, A means data is valid
#  6) Checksum

    fields = (
        ("Source", "source"), #S = Shaft, E = Engine
        ("Engine or shaft number", "engine_no", int),
        ("Speed", "speed", float), #RPM
        ("Propeller pitch", "pitch"), #- means astern
        ("Status", "status"), #A means valid
    )


class VPW(TalkerSentence):
    """ Speed, Measured Parallel to Wind
    """
    fields = (
        ("Speed knots", "speed_kn", float),#- means downwind
        ("Unit knots", "unit_knots"),#N means knots
        ("Speed m/s", "speed_ms", float),
        ("Unit m/s", "unit_ms"),#M means m/s
    )

# VPW - Speed - Measured Parallel to Wind

#       1   2 3   4 5
#       |   | |   | |
#$--VPW,x.x,N,x.x,M*hh<CR><LF>

# Field Number:
#  1) Speed, "-" means downwind
#  2) N = Knots
#  3) Speed, "-" means downwind
#  4) M = Meters per second
#  5) Checksum

class VDR(TalkerSentence):
    fields = (
        ("Degrees True", "deg_t", float),
        ("TRUE", "true"),#T means true
        ("Degrees Magnetic", "deg_m", float),
        ("Magnetic", "magnetic"),#M means magnetic
        ("Speed of Current", "current", float),
        ("Unit", "unit_kn"), #N means knots
    )

# VDR - Set and Drift

#        1   2 3   4 5   6 7
#        |   | |   | |   | |
# $--VDR,x.x,T,x.x,M,x.x,N*hh<CR><LF>

# Field Number:
#  1) Degress True
#  2) T = True
#  3) Degrees Magnetic
#  4) M = Magnetic
#  5) Knots (speed of current)
#  6) N = Knots
#  7) Checksum

class VWR(TalkerSentence):
    fields = (
        ("Degrees Rel", "deg_r", float),
        ("Left/Right", "l_r"),#R means right
        ("Wind speed kn", "wind_speed_kn", float),
        ("Knots", "unit_knots"),#N means knots
        ("Wind Speed m/s", "wind_speed_ms", float),
        ("m/s", "unit_ms"),#M means m/s
        ("Wind Speed Km/h", "wind_speed_km", float),
        ("Knots", "unit_km"), #K means Km
    )

    # TODO
    # getters/setters that normalize units,
    # apply L/R sign, and sync all fields
    # when setting the speed

#VWR - Relative Wind Speed and Angle

#         1  2  3  4  5  6  7  8 9
#         |  |  |  |  |  |  |  | |
# $--VWR,x.x,a,x.x,N,x.x,M,x.x,K*hh<CR><LF>

# Field Number:
#  1) Wind direction magnitude in degrees
#  2) Wind direction Left/Right of bow
#  3) Speed
#  4) N = Knots
#  5) Speed
#  6) M = Meters Per Second
#  7) Speed
#  8) K = Kilometers Per Hour
#  9) Checksum

# ---------------------------------- Not Yet Implemented --------------------- #
# ---------------------------------------------------------------------------- #


#class FSI(TalkerSentence):
#    """ Frequency Set Information
#    """
    #    fields = (
    # )

#class GLC(TalkerSentence):
#    """ Geographic Position, Loran-C
#    """
    #    fields = (
    # )

#class GXA(TalkerSentence):
#    """ TRANSIT Position
#    """
    #    fields = (
    # )

#class LCD(TalkerSentence):
#    """ Loran-C Signal Data
#    """
    #    fields = (
    # )

#class MTA(TalkerSentence):
#    """ Air Temperature (to be phased out)
#    """
    #    fields = (
    # )

#class OLN(TalkerSentence):
#    """ Omega Lane Numbers
#    """
    #    fields = (
    # )

#class OSD(TalkerSentence):
#    """ Own Ship Data
#    """
    #    fields = (
    # )

#class RSD(TalkerSentence):
#    """ RADAR System Data
#    """
    #    fields = (
    # )

#class SFI(TalkerSentence):
#    """ Scanning Frequency Information
#    """
    #    fields = (
    # )

#class TTM(TalkerSentence):
#    """ Tracked Target Message
#    """
    #    fields = (
    # )

#class XDR(TalkerSentence):
#    """ Transducer Measurements
#    """
    #    fields = (
    # )

#class XTR(TalkerSentence):
#    """ Cross-Track Error, Dead Reckoning
#    """
    #    fields = (
    # )

#class ZFO(TalkerSentence):
#    """ UTC & Time from Origin Waypoint
#    """
    #    fields = (
    # )

#class ZTG(TalkerSentence):
#    """ UTC & Time to Destination Waypoint
#    """
    #    fields = (
    # )

# ---------------------------------------------------------------------------- #
# -------------------------- Unknown Formats --------------------------------- #
# ---------------------------------------------------------------------------- #

#class ASD(TalkerSentence):
#    """ Auto-pilot system data (Unknown format)
#    """
    #    fields = (
    # )

# ---------------------------------------------------------------------------- #
# -------------------------- Obsolete Formats -------------------------------- #
# ---------------------------------------------------------------------------- #

#class DCN(TalkerSentence):
#    """ Decca Position (obsolete)
#    """
    #    fields = (
    # )


