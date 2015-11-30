#!/usr/bin/python
import sys
if len(sys.argv)<=1:
	print "usage: "+ sys.argv[0] + " <seed>"
	exit()

import os
import time


for load in [1,10,20,30,40,50,60,70,80,90,95]:

	print load

	# spawn job
	os.system("sbatch llvr.tcl "+str(load)+" "+sys.argv[1])
	os.system("wait")
	time.sleep(0.25)
print "done"
