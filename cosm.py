#!/usr/bin/python

import urllib
import unittest

# _key='Hq_cC9Ff8HGu5he9tkK0H8OCNxSSAKxLV3dYSkcyVU9hND0g' #74540 dogi

# feed= '74539'

TONG2_FEED = "74539"
DOKGI_FEED = "74540"
 
class CosmClient:
  url_template = 'http://api.cosm.com/v2/feeds/%s.json?key=%s&amp;timezone=%s' 
  def __init__(self, key, feed, timezone):
    self.url = self.url_template  % (feed, key, timezone)

  def read_json(self):
    self.json = urllib.urlopen(self.url).read()
    return self.json


class SeeOhClient:
  HUMIDITY = 0
  LIGHT = 1
  MOISTURE = 2
  TEMPERATURE = 3

  def __init__(self, _feed):
    if _feed == TONG2_FEED:
      _key='h6MsqOTg4cofjLLv8oJE3riBbCaSAKxpVVJTUDlTMVladz0g' #74539 tongi
    elif _feed == DOKGI_FEED:
      _key='Hq_cC9Ff8HGu5he9tkK0H8OCNxSSAKxLV3dYSkcyVU9hND0g' #74540 dogi
    self.cosm = CosmClient(_key, _feed, '+9')

  def read_value(self, sensor_type):
    json = self.cosm.read_json()
    return eval(json)['datastreams'][sensor_type]['current_value']

  def get_temperature(self):
    return self.read_value(self.TEMPERATURE)

  def get_humidity(self):
    return self.read_value(self.HUMIDITY)

  def get_moisture(self):
    return self.read_value(self.MOISTURE)

  def get_light(self):
    return self.read_value(self.LIGHT)


class TestCosmReader(unittest.TestCase):
  def setUp(self):
    pass

  def test_read_json(self):
    _key='h6MsqOTg4cofjLLv8oJE3riBbCaSAKxpVVJTUDlTMVladz0g' #74539 tongi
    c = CosmClient(key=_key, feed='74539', timezone='+9')
    self.assertTrue('donghee' in c.read_json())

class TestSeeOhCient(unittest.TestCase):
  def test_read_temperature(self):
    c = SeeOhClient(_feed='74539')
    self.assertEquals('77', c.get_humidity())
    self.assertEquals('0', c.get_light())
    self.assertEquals('74', c.get_moisture())
    self.assertEquals('28', c.get_temperature())

if __name__ == '__main__':
  unittest.main()
