#!/usr/bin/python
import os
import sys
import logging
import traceback
import datetime
import re
from Settings import *
from TeuxDeux import TeuxDeux

def extractDateNText(text):  
  date = datetime.date.today()
  day = date.day
  month = date.month
  year = date.year

  dot_or_slash = '[\./]'
  _1_to_31 = '[0-3]?\d{1}'
  _1_to_12 = '[01]?\d?'
  _0000_to_2000 = '\d{0,4}'

  date_n_text=re.findall(r'^('+_1_to_31+')'+dot_or_slash+'('+_1_to_12+')'+dot_or_slash+'?('+_0000_to_2000+')\s?(.*)',text)
  if len(date_n_text)>0 and len(date_n_text[0])==4:
    
    if date_n_text[0][0]!='':
      day = int(date_n_text[0][0])

    if date_n_text[0][1]!='':
      month = int(date_n_text[0][1])

    if date_n_text[0][2]!='':
      year = int(date_n_text[0][2])

    try:
      parsed_date = datetime.date(year, month, day)
      if parsed_date > date:
        date = parsed_date
        if date_n_text[0][3].strip()!='':
          text = date_n_text[0][3]
    except ValueError:
      pass

  return text, date

def main():
  text = ''
  for env in os.environ:
    if (re.match(r'SMS_[0-9]*_TEXT', env) != None):
      text += os.environ[env]

  logging.debug('Number %s have sent text: %s' % (os.environ['SMS_1_NUMBER'], text))
  logging.debug('Connecting to todo with %s:%s****' % (username, password[0]))

  td=TeuxDeux(username, password)
  td.create(*extractDateNText(text))

def log_except_hook(*exc_info):
  logging.exception("".join(traceback.format_exception(*exc_info)))

if __name__ == '__main__':
  logging.basicConfig(filename=os.path.dirname(os.path.realpath(__file__))+'/log.txt', 
    level=logging.DEBUG, 
    format='%(asctime)s %(levelname)s %(message)s')
  sys.excepthook = log_except_hook
  main()

