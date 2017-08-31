# pylint: disable=invalid-name
class SeaTalk(object):
    '''Mixin to add Seatalk functionality. Based on Thomas knauf's work
    http://www.thomasknauf.de/seatalk.htm'''
    byte_to_command = {
        '00': 'Depth below transducer',
        '01': 'Equipment ID',
        '05': 'Engine RPM and PITCH',
        '10': 'Apparent Wind Angle',
        '11': 'Apparent Wind Speed',
        '20': 'Speed through water',
        '50': 'LAT position',
        '51': 'LON position',
        '52': 'Speed over Ground',
        '53': 'Course over Ground',
        '82': 'Target waypoint name',
        '84': 'Compass heading  Autopilot course and Rudder position',
        '9C': 'Compass heading and Rudder position'
    }

    # pylint: disable=no-member
    @property
    def command_name(self):
        '''Get seatalk command's meaning'''
        return self.byte_to_command.get(self.cmd, 'Unknown Command')


