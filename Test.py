#!/usr/bin/python

# sudo pip install mockito

import unittest
import datetime
import os
from mockito import when, any, verify

import Settings
from Receive import main
from Receive import extractDateNText
from TeuxDeux import TeuxDeux


year = 2012
month = 5
day = 24

def do_nothing(*p):
  pass

class MockDate(datetime.date):
  @classmethod
  def today(self):
    return self(year, month, day)

class ReceiveTest(unittest.TestCase):
  
  def setUp(self):
    TeuxDeux.__init__ = do_nothing
    when(TeuxDeux).create(any()).thenReturn("")
    datetime.date = MockDate

  def testSettings(self):
    global constructor_called
    constructor_called = False    
    
    def verify_constructor(s, user, pwd):
      global constructor_called
      self.assertEqual(user, Settings.username)
      self.assertEqual(pwd, Settings.password)
      constructor_called = True

    TeuxDeux.__init__ = verify_constructor

    main()

    self.assertTrue(constructor_called)
  
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
      'SMS_0_TEXT':'1/8 do stuff'}

    main()

    verify(TeuxDeux).create("do stuff", MockDate(year, 8, 1))

class DateTest(unittest.TestCase):
  
  def setUp(self):
    when(TeuxDeux).create(any()).thenReturn("")
    datetime.date = MockDate

  def testTrailingZeros(self):
    self.assertEqual(extractDateNText('08.07 text'), ('text', MockDate(year, 7, 8)))
    self.assertEqual(extractDateNText('28.06 text'),  ('text', MockDate(year, 6, 28)))
    self.assertEqual(extractDateNText('28.06.2018 text'),  ('text', MockDate(2018, 6, 28)))    

  def testDotDelimeter(self):
    self.assertEqual(extractDateNText('28. text'), ('text', MockDate(year, month, 28)))
    self.assertEqual(extractDateNText('28.6.2018 text'),  ('text', MockDate(2018, 6, 28)))
    self.assertEqual(extractDateNText('28.6.2018 text'),  ('text', MockDate(2018, 6, 28)))    

  def testDatesWithoutText(self):
    self.assertEqual(extractDateNText('29/5'), ('29/5', MockDate(year, 5, 29)))
    self.assertEqual(extractDateNText('8/3/2018   '), ('8/3/2018   ',MockDate(2018, 3, 8)) )

  def testDatesInPast(self):
    self.assertEqual(extractDateNText('28/%s/%s text' % (month-1,year)), ('28/%s/%s text' % (month-1,year), MockDate.today()))
    self.assertEqual(extractDateNText('8/ text'),  ('8/ text', MockDate.today()))
    self.assertEqual(extractDateNText('8/'), ('8/', MockDate.today() ))
    self.assertEqual(extractDateNText('8/5 text'), ('8/5 text', MockDate.today()) )
    self.assertEqual(extractDateNText('8/5'), ('8/5', MockDate.today()))

  def testNotDates(self):
    self.assertEqual(extractDateNText(' 28.8.2018 text'), (' 28.8.2018 text', MockDate.today()) )
    self.assertEqual(extractDateNText('28 text'), ('28 text', MockDate.today()) )
    self.assertEqual(extractDateNText('32/13/2015 imposibiru'), ('32/13/2015 imposibiru', MockDate.today()) )

  def testSlashDelimeter(self):
    self.assertEqual(extractDateNText('28/ text'), ('text', MockDate(year, month, 28)))
    self.assertEqual(extractDateNText('28/text'),  ('text', MockDate(year, month, 28)))

    self.assertEqual(extractDateNText('31/5/ text'), ('text', MockDate(year, 5, 31)))  
    self.assertEqual(extractDateNText('28/5 text'), ('text', MockDate(year, 5, 28)) )
    self.assertEqual(extractDateNText('28/5text'), ('text', MockDate(year, 5, 28)) )

    self.assertEqual(extractDateNText('28/3/2018 text'), ('text', MockDate(2018, 3, 28)))
    self.assertEqual(extractDateNText('28/3/2018text'), ('text', MockDate(2018, 3, 28)))
    self.assertEqual(extractDateNText('8/3/2018 text'), ('text', MockDate(2018, 3, 8)))    

if __name__ == '__main__':
  unittest.main()