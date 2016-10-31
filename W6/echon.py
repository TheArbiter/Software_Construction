#!/usr/bin/python2.7

from __future__ import print_function;
import sys;

if len(sys.argv) != 3:
   print ("Usage: ./echon.py <number of lines> <string>\n", end = '');
else :
   print ((sys.argv[2]+"\n") * int(sys.argv[1]), end = '');
