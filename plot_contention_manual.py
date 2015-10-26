import matplotlib
matplotlib.use('Agg')
import pylab as pl
from xml.dom import minidom



#load configurations
mainconf = minidom.parse('config.xml')
mainconfigurations = mainconf.getElementsByTagName('config')
log_dir=mainconfigurations[0].getElementsByTagName('log_dir')[0].childNodes[0].nodeValue
plot_dir=mainconfigurations[0].getElementsByTagName('plot_dir')[0].childNodes[0].nodeValue
exp_nums=[204]
load=str(50)
fig=pl.figure()
for i in exp_nums:
	# print i
	exp_num=str(i)
# exp_num=str(201)
# exp_num2=str(202)
	conf = minidom.parse(log_dir+'exp'+exp_num+'/config.xml')
	configurations = conf.getElementsByTagName('config')
	# max_copies=configurations[0].getElementsByTagName('copies')[0].childNodes[0].nodeValue
	copy=configurations[0].getElementsByTagName('copies')[0].childNodes[0].nodeValue
	max_flows=configurations[0].getElementsByTagName('number_of_flows')[0].childNodes[0].nodeValue
	num_servers=configurations[0].getElementsByTagName('number_of_servers')[0].childNodes[0].nodeValue
	sim_time=configurations[0].getElementsByTagName('simulation_time')[0].childNodes[0].nodeValue
	chunk_size=configurations[0].getElementsByTagName('chunk_size')[0].childNodes[0].nodeValue
	link_bw=configurations[0].getElementsByTagName('link_bandwidth')[0].childNodes[0].nodeValue
	priQ=configurations[0].getElementsByTagName('use_different_priorities')[0].childNodes[0].nodeValue

	if int(priQ):
		priQ_string="using queues"
	else:
		priQ_string="without queues"
	#plot each copy on the same graph

	with open(log_dir+"exp"+exp_num+"/contention_"+str(copy)+"_"+load+".csv", 'r') as csvfile:
		for line in csvfile:
			lineList = line.split("[")
			server =  lineList[0].split(",")[0]
			contentionList = lineList[1].split("]")[0].split(",")
			timeList = lineList[2].split("]")[0].split(",")
			contentionList=map(int, contentionList)
			timeList=map(float, timeList)
			# print len(contentionList)
			# print len(timeList)
			timeListWidth = [0]+timeList[:-1]
			# print len(timeListWidth)
			# print 

			# pl.plot(timeList, contentionList, label="server# "+str(server))
			fig=pl.figure()
			pl.bar(timeList,contentionList, width=[a_i - b_i for a_i, b_i in zip(timeList, timeListWidth)])
			#pl.show()
			pl.xlabel("time (s)")
			pl.ylabel("number of overlapping request")
			pl.title("contention over time")
			pl.xlim([0,int(sim_time)/3])
			pl.ylim([0,20])
			fig.savefig(plot_dir+"/contention/exp"+exp_num+"_"+str(copy)+"_"+load+"_"+server+".png")
			pl.cla()   # Clear axis
			pl.clf()   # Clear figure
			pl.close() # Close a figure window
			# fig.cla()   # Clear axis
				# fig.clf()   # Clear figure
				# fig.close() # Close a figure window
		# 	

		# exit()
	

# 			loads.append(lineList[0])
# 			afcts.append(lineList[1])
# 	pl.plot(loads, afcts, label=str(copy)+'-copies')
# 	pl.legend()
# pl.xlabel("percentage load")
# pl.ylabel("AFCTs")
# pl.grid(True)
# # pl.ylim([0,18])

# # show the plot on the screen
# # pl.show()
# pl.savefig(plot_dir+"exp"+exp_num+".png", bbox_inches='tight')
