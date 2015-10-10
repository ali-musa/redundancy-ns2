import pylab as pl
from xml.dom import minidom


#load configurations
conf = minidom.parse('config.xml')
configurations = conf.getElementsByTagName('config')

exp_num=configurations[0].getElementsByTagName('experiment_number')[0].childNodes[0].nodeValue
log_dir=configurations[0].getElementsByTagName('log_dir')[0].childNodes[0].nodeValue
plot_dir=configurations[0].getElementsByTagName('plot_dir')[0].childNodes[0].nodeValue
k=configurations[0].getElementsByTagName('copies')[0].childNodes[0].nodeValue
load=configurations[0].getElementsByTagName('percent_load')[0].childNodes[0].nodeValue

#plot each copy on the same graph
# for copy in xrange(1,int(max_copies)+1):
# 	loads = []
# 	afcts = []
with open(log_dir+"exp"+exp_num+"/contention_"+k+"_"+load+".csv", 'r') as csvfile:
	for line in csvfile:
		lineList = line.split("[")
		server =  lineList[0].split(",")[0]
		contentionList = lineList[1].split("]")[0].split(",")
		timeList = lineList[2].split("]")[0].split(",")
		contentionList=map(int, contentionList)
		timeList=map(float, timeList)
		print len(contentionList)
		print len(timeList)
		timeListWidth = [0]+timeList[:-1]
		print len(timeListWidth)
		print 

		# pl.plot(timeList, contentionList, label="server# "+str(server))
		pl.bar(timeList,contentionList, width=[a_i - b_i for a_i, b_i in zip(timeList, timeListWidth)])
		pl.show()
# 	

		exit()
	

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