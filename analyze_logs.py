#TODO: fix this for different priorities

# import itertools
from xml.dom import minidom

#load configurations
conf = minidom.parse('config.xml')
configurations = conf.getElementsByTagName('config')

exp_num=configurations[0].getElementsByTagName('experiment_number')[0].childNodes[0].nodeValue
log_dir=configurations[0].getElementsByTagName('log_dir')[0].childNodes[0].nodeValue
N=configurations[0].getElementsByTagName('number_of_servers')[0].childNodes[0].nodeValue
k=configurations[0].getElementsByTagName('copies')[0].childNodes[0].nodeValue
load=configurations[0].getElementsByTagName('percent_load')[0].childNodes[0].nodeValue
failures=configurations[0].getElementsByTagName('failures')[0].childNodes[0].nodeValue
numFlows=configurations[0].getElementsByTagName('number_of_flows')[0].childNodes[0].nodeValue
priQ=configurations[0].getElementsByTagName('use_different_priorities')[0].childNodes[0].nodeValue

class FlowTime:
	def __init__(self, time, label):
		self.time = time
		self.label = label

#function definitions
def calculateAfct(startList, endList):
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
	afct = sum(flowCompletionTimes) / float(len(flowCompletionTimes))

	with open(log_dir+"exp"+exp_num+"/afct_"+k+"copies.csv", 'a') as csvfile:
	   csvfile.write(load)
	   csvfile.write(",")
	   csvfile.write(str(afct))
	   csvfile.write("\n")

	print "AFCT"+k+"_"+load+": "+str(afct)
	return afct


# def getOverlap(a, b):
# 	return max(0, min(a[1], b[1]) - max(a[0], b[0]))
		
def calculateTimeOverlap(startList, endList):
	with open(log_dir+"exp"+exp_num+"/contention_"+k+"_"+load+".csv", 'w') as csvfile:
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
			



	# endTimes =  [endList[a][0] for a in xrange(len(endList))]
	# startTimes = [startList[b][0] for b in xrange(len(startList))]
	# # startServers = [startList[c][1] for c in xrange(len(startList))]
	# for primaryFlowId in xrange(int(numFlows)):
	# 	primaryServer = startList[primaryFlowId][1]
	# 	for flowId in xrange(len(startList)):
	# 		if ((flowId != primaryFlowId) and (startList[flowId][1] == primaryServer)): #server collision
	# 			print getOverlap([startList[primaryServer][0], endList[primaryServer][0]], [startList[flowId][0], endList[flowId][0]])

	# return


	# timeOverlap = 0
	# for flowId in xrange(int(numFlows)):
	# 	if flowId !=0:
	# 		if endTimes[flowId-1]>startTimes[flowId]:
	# 			timeOverlap+=endTimes[flowId-1]


#variable initializations
flowStarts = [None]*(int(numFlows)*int(k)) #will contain the start time and the server number, flow ids will be the index
flowEnds = [None]*(int(numFlows)*int(k)) #will contain the end time and the server number, flow ids will be the index

#read and parse the files
startsFilename = log_dir+"exp"+exp_num+"/"+"starts"+N+"_"+k+"_"+load+"_"+failures+"_"+numFlows+"_"+str(priQ)+".tr"
with open(startsFilename, "r") as f1:
	for line in f1:
		lineList = line.split()
		if len(lineList)>0:
		 	flowStarts[int(lineList[1])-1] = [float(lineList[0]), int(lineList[2])]

endsFilename = log_dir+"exp"+exp_num+"/"+"ends"+N+"_"+k+"_"+str(load)+"_"+failures+"_"+numFlows+"_"+str(priQ)+".tr"
with open(endsFilename, "r") as f1:
	for line in f1:
		lineList = line.split()
		if len(lineList)>0:
		 	flowEnds[int(lineList[1])-1] = [float(lineList[0]), int(lineList[2])]


calculateAfct(flowStarts, flowEnds)
calculateTimeOverlap(flowStarts, flowEnds)