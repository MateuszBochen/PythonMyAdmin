#!/usr/bin/python2.7
# -*- coding: UTF-8  -*-
import cgitb; cgitb.enable()
import time
import math

def microtime(get_as_float = True):
    if get_as_float:
        return time.time()
    else:
        return '%f %d' % math.modf(time.time())


start = microtime()

 
import sys, os

os.environ["PY_PATH"] = os.path.dirname(__file__)
from System import Kernel
myObject = Kernel.Kernel()

#print "<hr/>----------" 
#print microtime() - start