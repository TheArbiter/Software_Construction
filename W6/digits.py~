#!/usr/bin/python2.7

from __future__ import print_function;
import fileinput, re;

for line in fileinput.input():
   print (re.sub("[6-9]",">", re.sub("[0-4]","<",line)), end = '');
