#!/usr/bin/python
import os
import sys
import logging
import traceback
import re
from TeuxDeux import TeuxDeux

def main():
  text = ''
  for env in os.environ:
    if (re.match(r'SMS_[0-9]*_TEXT', env) != None):
      text += os.environ[env]

  logging.debug('Number %s have sent text: %s' % (os.environ['SMS_1_NUMBER'], text))

  td=TeuxDeux("user","pass")
  td.create(text)

def log_except_hook(*exc_info):
  logging.exception("".join(traceback.format_exception(*exc_info)))

if __name__ == '__main__':
  logging.basicConfig(filename=os.path.dirname(os.path.realpath(__file__))+'/log.txt', 
    level=logging.DEBUG, 
    format='%(asctime)s %(levelname)s %(message)s')
  sys.excepthook = log_except_hook
  main()

