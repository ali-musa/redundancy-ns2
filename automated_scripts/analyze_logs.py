 #TODO: fix this for different priorities

# import itertools
from __future__ import division
from xml.dom import minidom
import numpy as np
import os.path
import sys
import re


#helper
#ref:nedbatchelder.com/blog/200712/human_sorting.html
def tryint(s):
    try:
        return int(s)
    except:
        return s
    
def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

#ref:http://stackoverflow.com/questions/10919664/averaging-list-of-lists-python
def mean(a):
    return sum(a) / len(a)    
##############################################################################



if len(sys.argv)<=1:
	print "usage: "+ sys.argv[0] + " <experiment number(s)>"
	exit()

#load configurations
mainconf = minidom.parse('../main_config.xml')
mainconfigurations = mainconf.getElementsByTagName('config')
log_dir=mainconfigurations[0].getElementsByTagName('log_dir')[0].childNodes[0].nodeValue
log_dir="../"+log_dir
plot_dir=mainconfigurations[0].getElementsByTagName('plot_dir')[0].childNodes[0].nodeValue
plot_dir="../"+plot_dir

#globals
load=-1

for exp_num in sys.argv[1:]:
	print "Analysing experiment "+exp_num+" ..."
	conf = minidom.parse(log_dir+'exp'+exp_num+'/config.xml')
	configurations = conf.getElementsByTagName('config')
	N=configurations[0].getElementsByTagName('number_of_servers')[0].childNodes[0].nodeValue
	k=configurations[0].getElementsByTagName('copies')[0].childNodes[0].nodeValue
	failures=configurations[0].getElementsByTagName('failures')[0].childNodes[0].nodeValue
	numFlows=configurations[0].getElementsByTagName('number_of_flows')[0].childNodes[0].nodeValue
	priQ=configurations[0].getElementsByTagName('use_different_priorities')[0].childNodes[0].nodeValue
	flow_size=configurations[0].getElementsByTagName('chunk_size')[0].childNodes[0].nodeValue
	link_bw=configurations[0].getElementsByTagName('link_bandwidth')[0].childNodes[0].nodeValue


	write_directory=log_dir+"exp"+exp_num+"/analysis/"
	if not os.path.exists(write_directory):
		os.mkdir( write_directory );
	else:
		os.system("rm -r "+write_directory+"*")
	class FlowTime:
		def __init__(self, time, label):
			self.time = time
			self.label = label
	#helper functions
	#ref: http://stackoverflow.com/questions/477486/python-decimal-range-step-value
	def drange(start, stop, step):
		r = start
		while r < stop:
			yield r
			r += step


	#function definitions
	def calculateAfct(startList, endList, seed_value):
		global load
		total_flows=0
		total_redundant_flows=0
		faster_redundant_flows=0
		equiflows=0
		# equi_margin=((flow_size*8.0)/(link_bw*1000000.0))/20.0 #within 1/20th of the flow completion time under low loads
		flowCompletionTimes = [None]*int(numFlows)
		for flowId in xrange(len(endList)):
			if endList[flowId] is not None:
				total_flows+=1
				if flowId>=int(numFlows):
					total_redundant_flows+=1
				currentFlowCompletionTime = endList[flowId][0]-startList[flowId][0]
				if flowCompletionTimes[flowId%int(numFlows)] is not None:
					if currentFlowCompletionTime < flowCompletionTimes[flowId%int(numFlows)]:
						faster_redundant_flows+=1 #TODO: check if this is reasonable for more than 2 copies
						flowCompletionTimes[flowId%int(numFlows)] = currentFlowCompletionTime
					elif currentFlowCompletionTime == flowCompletionTimes[flowId%int(numFlows)]:
						equiflows+=1
					else:
						pass
				else:
					flowCompletionTimes[flowId%int(numFlows)] = currentFlowCompletionTime
			else:
				pass
		flowCompletionTimes = [x for x in flowCompletionTimes if x is not None]
		afct = sum(flowCompletionTimes) / float(len(flowCompletionTimes))

		with open(write_directory+"afct"+seed_value+".csv", 'a') as csvfile:
		   csvfile.write(load)
		   csvfile.write(",")
		   csvfile.write(str(afct))
		   csvfile.write("\n")

	   	with open(write_directory+"fasterRedundant"+seed_value+".csv", 'a') as csvfile:
			csvfile.write(load)
			csvfile.write(",")
			if(total_redundant_flows is not 0):
				csvfile.write(str(float(faster_redundant_flows)/total_redundant_flows))
			else:
				csvfile.write(str(0))
			csvfile.write("\n")

		with open(write_directory+"equiflows"+seed_value+".csv", 'a') as csvfile:
			csvfile.write(load)
			csvfile.write(",")
			if(total_redundant_flows is not 0):
				csvfile.write(str(float(equiflows)/total_redundant_flows))
			else:
				csvfile.write(str(0))
			csvfile.write("\n")

		with open(write_directory+"fasterOrEqualRedundant"+seed_value+".csv", 'a') as csvfile:
			csvfile.write(load)
			csvfile.write(",")
			if(total_redundant_flows is not 0):
				csvfile.write(str(float(equiflows+faster_redundant_flows)/total_redundant_flows))
			else:
				csvfile.write(str(0))
			csvfile.write("\n")


		# print "AFCT"+k+"_"+load+": "+str(afct)
		# print "total_flows:"+str(total_flows)
		# print "faster_redundant_flows:"+str(faster_redundant_flows)
		# print "equiflows:"+str(equiflows)
		# return afct

	def calculatePercentile(startList, endList,percentile, seed_value):
		global load
		flowCompletionTimes = [None]*int(numFlows)
		for flowId in xrange(len(endList)):
			if endList[flowId] is not None:
				currentFlowCompletionTime = endList[flowId][0]-startList[flowId][0]
				if flowCompletionTimes[flowId%int(numFlows)] is not None:
					if currentFlowCompletionTime < flowCompletionTimes[flowId%int(numFlows)]:
						flowCompletionTimes[flowId%int(numFlows)] = currentFlowCompletionTime
					else:
						pass
				else:
					flowCompletionTimes[flowId%int(numFlows)] = currentFlowCompletionTime
			else:
				pass
		flowCompletionTimes = [x for x in flowCompletionTimes if x is not None]
		fcts_numpy = np.array(flowCompletionTimes)

		p = np.percentile(fcts_numpy,percentile)

		with open(write_directory+"percentile_"+str(percentile)+"_"+seed_value+".csv", 'a') as csvfile:
		   csvfile.write(load)
		   csvfile.write(",")
		   csvfile.write(str(p))
		   csvfile.write("\n")
	   	
		# print "Percentile"+k+"_"+load+"_"+str(percentile)+": "+str(p)
		# return p


		

	# def getOverlap(a, b):
	# 	return max(0, min(a[1], b[1]) - max(a[0], b[0]))
			
	def calculateTimeOverlap(startList, endList, seed_value):
		global load
		with open(write_directory+"contention_"+load+".csv", 'w') as csvfile:
			for server in xrange(1,int(N)+1):
				flowTimes = []
				for flowId in xrange(len(endList)):
					if endList[flowId] is not None:
						if endList[flowId][1] == server:
							flowTimes.append(FlowTime(endList[flowId][0],"endTime"))
							flowTimes.append(FlowTime(startList[flowId][0],"startTime")) #assumption is that flows will start and end at the same server and not switch


			 	sortedFlowTimes = sorted(flowTimes, key=lambda x: x.time)
			 	# print [x.time for x in sortedFlowTimes]
			 	contention = [0]*len(sortedFlowTimes)
			 	currContention = 0
			 	for index in xrange(len(contention)):
			 		if (sortedFlowTimes[index].label=="startTime"):
			 			currContention+=1
		 			elif (sortedFlowTimes[index].label=="endTime"):
		 				currContention-=1
	 				contention[index]=currContention
				csvfile.write(str(server))
				csvfile.write(",")
				csvfile.write(str(contention))
				csvfile.write(str([x.time for x in sortedFlowTimes]))
				csvfile.write("\n")
				with open(write_directory+"contention_"+load+"_sampled_"+seed_value+".csv", 'a') as csvfile2:
					contention_sampled=[]
					sampled_at=[]
					sample_generator=drange(4.0,sortedFlowTimes[-1].time, (sortedFlowTimes[-1].time -4.0)/10.0)
					for x in sample_generator:
						sampled_at.append(x)
						for index in range(len(sortedFlowTimes)):
							if x<sortedFlowTimes[index].time:
								contention_sampled.append(contention[index-1])
								break
		
					csvfile2.write(str(server))
					csvfile2.write(",")
					csvfile2.write(str(contention_sampled))
					csvfile2.write(str(sampled_at))
					csvfile2.write("\n")		
				# print contention_sampled

	def calculateRedundantOverlap(startList, endList, seed_value):
		global load
		contention_list=[[]]*int(N)
		times_list=[[]]*int(N)
		with open(write_directory+"contentionRedundant_"+load+"_"+seed_value+".csv", 'w') as csvfile:
			for server in xrange(1,int(N)+1):
				flowTimes = []
				for flowId in xrange(len(endList)):
					if flowId>=int(numFlows): #redundant only overlap
						if endList[flowId] is not None:
							if endList[flowId][1] == server:
								flowTimes.append(FlowTime(endList[flowId][0],"endTime"))
								flowTimes.append(FlowTime(startList[flowId][0],"startTime")) #assumption is that flows will start and end at the same server and not switch

			 	sortedFlowTimes = sorted(flowTimes, key=lambda x: x.time)
			 	# print [x.time for x in sortedFlowTimes]
			 	contention = [0]*len(sortedFlowTimes)
			 	currContention = 0
			 	for index in xrange(len(contention)):
			 		if (sortedFlowTimes[index].label=="startTime"):
			 			currContention+=1
		 			elif (sortedFlowTimes[index].label=="endTime"):
		 				currContention-=1
					contention[index]=currContention
				csvfile.write(str(server))
				csvfile.write(",")
				csvfile.write(str(contention))
				csvfile.write(str([x.time for x in sortedFlowTimes]))
				csvfile.write("\n")
				if len(sortedFlowTimes)>0:
					with open(write_directory+"contentionRedundant_"+load+"_sampled_"+seed_value+".csv", 'a') as csvfile2:
						contention_sampled=[]
						sampled_at=[]
						sample_generator=drange(4.0,sortedFlowTimes[-1].time, (sortedFlowTimes[-1].time -4.0)/10.0)
						for x in sample_generator:
							sampled_at.append(x)
							for index in range(len(sortedFlowTimes)):
								if x<sortedFlowTimes[index].time:
									contention_sampled.append(contention[index-1])
									break
			
						csvfile2.write(str(server))
						csvfile2.write(",")
						csvfile2.write(str(contention_sampled))
						csvfile2.write(str(sampled_at))
						csvfile2.write("\n")		
				contention_list[server-1]=contention
				times_list[server-1]=[x.time for x in sortedFlowTimes]		
		return contention_list, times_list

	def calculateOriginalOverlap(startList, endList, seed_value):
		global load
		contention_list=[[]]*int(N)
		times_list=[[]]*int(N)
		with open(write_directory+"contentionOriginal_"+load+"_"+seed_value+".csv", 'w') as csvfile:
			for server in xrange(1,int(N)+1):
				flowTimes = []
				for flowId in xrange(len(endList)):
					if flowId>=int(numFlows): #original only overlap
						# print "THIS LINE SHOULD NOT BE PRINTED FOR 1 COPY!!!"
						break
					if endList[flowId] is not None:
						if endList[flowId][1] == server:
							flowTimes.append(FlowTime(endList[flowId][0],"endTime"))
							flowTimes.append(FlowTime(startList[flowId][0],"startTime")) #assumption is that flows will start and end at the same server and not switch
				# 		print flowId
				# raise Exception


			 	sortedFlowTimes = sorted(flowTimes, key=lambda x: x.time)
			 	# print [x.time for x in sortedFlowTimes]
			 	contention = [0]*len(sortedFlowTimes)
			 	currContention = 0
			 	for index in xrange(len(contention)):
			 		if (sortedFlowTimes[index].label=="startTime"):
			 			currContention+=1
		 			elif (sortedFlowTimes[index].label=="endTime"):
		 				currContention-=1
					contention[index]=currContention
				csvfile.write(str(server))
				csvfile.write(",")
				csvfile.write(str(contention))
				csvfile.write(str([x.time for x in sortedFlowTimes]))
				csvfile.write("\n")
				if len(sortedFlowTimes)>0:
					with open(write_directory+"contentionOriginal_"+load+"_sampled_"+seed_value+".csv", 'a') as csvfile2:
						contention_sampled=[]
						sampled_at=[]
						sample_generator=drange(4.0,sortedFlowTimes[-1].time, (sortedFlowTimes[-1].time -4.0)/10.0)
						for x in sample_generator:
							sampled_at.append(x)
							for index in range(len(sortedFlowTimes)):
								if x<sortedFlowTimes[index].time:
									contention_sampled.append(contention[index-1])
									break
			
						csvfile2.write(str(server))
						csvfile2.write(",")
						csvfile2.write(str(contention_sampled))
						csvfile2.write(str(sampled_at))
						csvfile2.write("\n")
				contention_list[server-1]=contention
				times_list[server-1]=[x.time for x in sortedFlowTimes]		
		return contention_list, times_list

	def calculateFlowContention(startList, endList,seed_value):
		global load
		contentionOriginal, timesOriginal = calculateOriginalOverlap(startList, endList, seed_value)
		contentionRedundant, timesRedundant = calculateRedundantOverlap(startList, endList, seed_value)
		flow_contention_list = [[]]*int(k)

		for copies in xrange(0,int(k)):
			curr_contention_list = [None]*int(numFlows)
			with open(write_directory+"flowContentions"+load+"_"+seed_value+"_"+str(copies+1)+".csv", 'w') as csvfile:
				for flowNumber in xrange(0,int(numFlows)):
					flowId = (int(numFlows)*copies) + flowNumber
					if endList[flowId] is not None:
						c=None
						server=endList[flowId][1]-1
						if copies>0: #redundant flows
							#find the contention a flow experiences when it starts
							c=findContention(contentionRedundant[server],timesRedundant[server], startList[flowId][0])
							c=c-1 #subtracting the contention that the flow creates itself
							curr_contention_list[flowId%int(numFlows)]=c
						else: #original flows
							#find the contention a flow experiences when it starts
							c=findContention(contentionOriginal[server],timesOriginal[server], startList[flowId][0])
							c=c-1 #subtracting the contention that the flow creates itself
							curr_contention_list[flowId%int(numFlows)]=c
						csvfile.write(str(flowId+1))
						csvfile.write(",")
						csvfile.write(str(c))
						csvfile.write("\n")

			flow_contention_list[copies]=curr_contention_list


	def findContention(contention,times,t):
		# TODO: the contention is negative, FIX!!!
		for index in range(len(times)):
			if times[index]>t:
				return contention[index-1]
		#TODO:fix this if not found!
		raise LookupError("Unable to find contention for flow arriving at: %s. Max time for which contention is available: %s" % (str(t), str(times[-1])) )



	def calculateAverageOverSeeds(startswith):
		#afct
		loads_list=[]
		y_list=[]
		for file in sorted(os.listdir(write_directory),key=alphanum_key):
			loads=[]
			y=[]
			# print "%s" % str(file)
			if file.startswith(startswith):
				with open(write_directory+file, "r") as f1:
					for line in f1:
						loads.append(float(line.split(",")[0]))
						y.append(float(line.split("\n")[0].split(",")[1]))
						
				loads_list.append(loads) #TODO: check if all the loads are the same
				y_list.append(y)

		avg_y= map(mean, zip(*y_list))

		if not os.path.exists(write_directory+"/averages"):
			os.mkdir( write_directory+"/averages" )

		for index in range(len(loads_list[0])):
			with open(write_directory+"/averages/" +startswith+".csv", 'a') as csvfile:
			   csvfile.write(str(loads_list[0][index]))
			   csvfile.write(",")
			   csvfile.write(str(avg_y[index]))
			   csvfile.write("\n")






	

	# for percent_load in [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95]:

	read_dir=log_dir+"exp"+exp_num+"/"
	for file in sorted(os.listdir(read_dir),key=alphanum_key):
		# print file
		if file.startswith("ends"):
			#variable initializations
			flowStarts = [None]*(int(numFlows)*int(k)) #will contain the start time and the server number, flow ids will be the index
			flowEnds = [None]*(int(numFlows)*int(k)) #will contain the end time and the server number, flow ids will be the index
			
			endsFilename=file
			load = file.split("_")[0][4:]
			seed_value = file.split("_")[1].split(".")[0]
			startsFilename = "starts"+load+"_"+seed_value+".tr"

			#read and parse the files
			with open(read_dir+startsFilename, "r") as f1:
				for line in f1:
					lineList = line.split()
					if len(lineList)>0:
					 	flowStarts[int(lineList[1])-1] = [float(lineList[0]), int(lineList[2])]

			with open(read_dir+endsFilename, "r") as f1:
				for line in f1:
					lineList = line.split()
					if len(lineList)>0:
					 	flowEnds[int(lineList[1])-1] = [float(lineList[0]), int(lineList[2])]


			calculateAfct(flowStarts, flowEnds, seed_value)
			calculateTimeOverlap(flowStarts, flowEnds, seed_value)
			calculatePercentile(flowStarts, flowEnds, 95, seed_value) 
			calculatePercentile(flowStarts, flowEnds, 99, seed_value)
			calculatePercentile(flowStarts, flowEnds, 50, seed_value)
			# calculateFlowContention(flowStarts,flowEnds, seed_value)

		else:
			continue
	
	calculateAverageOverSeeds("afct")
	calculateAverageOverSeeds("fasterOrEqualRedundant")
	calculateAverageOverSeeds("fasterRedundant")
	calculateAverageOverSeeds("equiflows")
	calculateAverageOverSeeds("percentile_95")
	calculateAverageOverSeeds("percentile_99")
	calculateAverageOverSeeds("percentile_50")
	print "Experiment "+exp_num+" analysis complete\n************************************\n"
	





