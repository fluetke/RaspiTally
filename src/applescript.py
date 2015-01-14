#!/usr/bin/python
#applescript module by "Dr. Drang" - http://www.leancrew.com/all-this/2013/03/combining-python-and-applescript/, checked 14.01.2015

import subprocess

def asrun(ascript):
  "Run the given AppleScript and return the standard output and error."

  osa = subprocess.Popen(['osascript', '-'],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE)
  return osa.communicate(ascript)[0]

def asquote(astr):
  "Return the AppleScript equivalent of the given string."
  
  astr = astr.replace('"', '" & quote & "')
  return '"{}"'.format(astr)
