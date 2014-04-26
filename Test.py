#!/usr/bin/python

# sudo pip install mockito

import unittest
import datetime
import os
from mockito import when, any, verify

from Receive import main
from Receive import extractDateNText
from TeuxDeux import TeuxDeux

def do_nothing(*p):
  pass

class MockDate(datetime.date):
  @classmethod
  def today(self):
    return self(2012, 5, 24)

class Tests(unittest.TestCase):
  
  def setUp(self):
    TeuxDeux.__init__ = do_nothing
    when(TeuxDeux).create(any()).thenReturn("")
    datetime.date = MockDate
  
  def testConcat(self):
    os.environ = {
      'SMS_1_NUMBER':'02',
      'SMS_0_TEXT':'Yello',
      'SMS_1_TEXT':' man!'}

    main()

    verify(TeuxDeux).create("Yello man!", MockDate.today())

  def testDate(self):
    os.environ = {
      'SMS_1_NUMBER':'02',
      'SMS_0_TEXT':'1/2 do stuff'}

    main()

    verify(TeuxDeux).create("do stuff", MockDate(2012, 2, 1))

  def testExtractDateNText(self):
    year = MockDate.today().year
    month = MockDate.today().month

    self.assertEqual(extractDateNText('28 text'), ('28 text', MockDate.today()) )

    self.assertEqual(extractDateNText('28/ text'), ('text', MockDate(year, month, 28)))
    self.assertEqual(extractDateNText('28/text'),  ('text', MockDate(year, month, 28)))
    self.assertEqual(extractDateNText('8/ text'),  ('text', MockDate(year, month, 8)))
    self.assertEqual(extractDateNText('8/'), ('', MockDate(year, month, 8)) )

    self.assertEqual(extractDateNText('9/5 text'), ('text', MockDate(year, 5, 9)))
    
    self.assertEqual(extractDateNText('28/3 text'), ('text', MockDate(year, 3, 28)) )
    self.assertEqual(extractDateNText('28/3text'), ('text', MockDate(year, 3, 28)) )
    self.assertEqual(extractDateNText('8/3 text'), ('text', MockDate(year, 3, 8)) )
    self.assertEqual(extractDateNText('8/3'), ('', MockDate(year, 3, 8)) )

    self.assertEqual(extractDateNText('28/3/2018 text'), ('text', MockDate(2018, 3, 28)))
    self.assertEqual(extractDateNText('28/3/2018text'), ('text', MockDate(2018, 3, 28)))
    self.assertEqual(extractDateNText('8/3/2018 text'), ('text', MockDate(2018, 3, 8)))
    self.assertEqual(extractDateNText('8/3/2018'), ('',MockDate(2018, 3, 8)) )


if __name__ == '__main__':
  unittest.main()