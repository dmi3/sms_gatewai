#!/usr/bin/python
import os
import sys
import logging
import traceback
import datetime
import re
from TeuxDeux import TeuxDeux

def extractDateNText(text):  
  day = datetime.date.today().day
  month = datetime.date.today().month
  year = datetime.date.today().year

  date_n_text=re.findall(r'^([1-3]?\d{1})/(1?\d?)/?(\d{0,4})\s?(.*)',text)
  if len(date_n_text)>0 and len(date_n_text[0])==4:
    
    if date_n_text[0][0]!='':
      day = int(date_n_text[0][0])

    if date_n_text[0][1]!='':
      month = int(date_n_text[0][1])

    if date_n_text[0][2]!='':
      year = int(date_n_text[0][2])

    text = date_n_text[0][3]

  return text, datetime.date(year, month, day)

def main():
  text = ''
  for env in os.environ:
    if (re.match(r'SMS_[0-9]*_TEXT', env) != None):
      text += os.environ[env]

  logging.debug('Number %s have sent text: %s' % (os.environ['SMS_1_NUMBER'], text))

  td=TeuxDeux("user","pass")
  td.create(*extractDateNText(text))

def log_except_hook(*exc_info):
  logging.exception("".join(traceback.format_exception(*exc_info)))

if __name__ == '__main__':
  logging.basicConfig(filename=os.path.dirname(os.path.realpath(__file__))+'/log.txt', 
    level=logging.DEBUG, 
    format='%(asctime)s %(levelname)s %(message)s')
  sys.excepthook = log_except_hook
  main()

