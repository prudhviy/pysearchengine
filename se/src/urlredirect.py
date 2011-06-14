#!/usr/bin/python
#

import cgi

#form = cgi.FieldStorage()
try:
  print "Content-type: text/html\n\n"
  print "Location: http://www.bsdpython.org/\n\n"
except KeyError:
  print "Content-type: text/plain"
  print ""
  print "Bad call to redirect.py: url not set"
