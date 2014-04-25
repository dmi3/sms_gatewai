#!/usr/bin/python

# sudo pip install mockito

import unittest
import os
from mockito import when, any, verify

from Receive import main
from TeuxDeux import TeuxDeux

def do_nothing(s, n, p):
  pass

TeuxDeux.__init__=do_nothing
os.environ = {
  'SMS_1_NUMBER':'02',
  'SMS_0_TEXT':'Yello',
  'SMS_1_TEXT':' man!'}
when(TeuxDeux).create(any()).thenReturn("")


class Tests(unittest.TestCase):
  
  def testOne(self):
    main()

    verify(TeuxDeux).create("Yello man!")


if __name__ == '__main__':
  unittest.main()