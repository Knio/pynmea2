'''
Convert a NMEA ascii log file into a GPX file
'''

import argparse
import datetime
import logging
import pathlib
import re
import xml.dom.minidom

log = logging.getLogger(__name__)

try:
  import pynmea2
except ImportError:
  import sys
  import pathlib
  p = pathlib.Path(__file__).parent.parent
  sys.path.append(str(p))
  log.info(sys.path)
  import pynmea2


def main():
  parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('nmea_file')

  args = parser.parse_args()
  nmea_file = pathlib.Path(args.nmea_file)

  if m := re.match(r'^(\d{2})(\d{2})(\d{2})', nmea_file.name):
    date = datetime.date(year=2000 + int(m.group(1)), month=int(m.group(2)), day=int(m.group(3)))
    log.debug('date parsed from filename: %r', date)
  else:
    date = None

  author = 'https://github.com/Knio/pynmea2'
  doc = xml.dom.minidom.Document()
  doc.appendChild(root := doc.createElement('gpx'))
  root.setAttribute('xmlns', "http://www.topografix.com/GPX/1/1")
  root.setAttribute('version', "1.1")
  root.setAttribute('creator', author)
  root.setAttribute('xmlns', "http://www.topografix.com/GPX/1/1")
  root.setAttribute('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
  root.setAttribute('xsi:schemaLocation', "http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd")

  root.appendChild(meta := doc.createElement('metadata'))
  root.appendChild(trk := doc.createElement('trk'))
  meta.appendChild(meta_name := doc.createElement('name'))
  meta.appendChild(meta_author := doc.createElement('author'))
  trk.appendChild(trk_name := doc.createElement('name'))
  trk.appendChild(trkseg := doc.createElement('trkseg'))
  meta_name.appendChild(doc.createTextNode(nmea_file.name))
  trk_name. appendChild(doc.createTextNode(nmea_file.name))
  meta_author.appendChild(author_link := doc.createElement('link'))
  author_link.setAttribute('href', author)
  author_link.appendChild(author_text := doc.createElement('text'))
  author_link.appendChild(author_type := doc.createElement('type'))
  author_text.appendChild(doc.createTextNode('Pynmea2'))
  author_type.appendChild(doc.createTextNode('text/html'))

  for line in open(args.nmea_file):
    try:
      msg = pynmea2.parse(line)
    except Exception as e:
      log.warning('Couldn\'t parse line: %r', e)
      continue

    if not (hasattr(msg, 'latitude') and hasattr(msg, 'longitude')):
      continue

    # if not hasattr(msg, 'altitude'):
    #   continue

    trkseg.appendChild(trkpt := doc.createElement('trkpt'))

    trkpt.setAttribute('lat', f'{msg.latitude:.6f}')
    trkpt.setAttribute('lon', f'{msg.longitude:.6f}')
    if hasattr(msg, 'altitude'):
      trkpt.appendChild(ele := doc.createElement('ele'))
      ele.appendChild(doc.createTextNode(f'{msg.altitude:.3f}'))

    # TODO try msg.datetime

    if date:
      trkpt.appendChild(time := doc.createElement('time'))
      dt = datetime.datetime.combine(date, msg.timestamp)
      dts = dt.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
      time.appendChild(doc.createTextNode(dts))

  xml_data = doc.toprettyxml(
    indent='  ',
    newl='\n',
    encoding='utf8',
  ).decode('utf8')
  print(xml_data)



if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  main()