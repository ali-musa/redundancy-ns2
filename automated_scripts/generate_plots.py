import sys

if len(sys.argv)<=1:
	print "usage: "+ sys.argv[0] + " <baseline experiment number> <experiment number(s)>"
	exit()
import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as pl
from xml.dom import minidom
import os
import os.path
from mpltools import style


#load configurations
mainconf = minidom.parse('../main_config.xml')
mainconfigurations = mainconf.getElementsByTagName('config')
log_dir=mainconfigurations[0].getElementsByTagName('log_dir')[0].childNodes[0].nodeValue
log_dir="../"+log_dir
plot_dir=mainconfigurations[0].getElementsByTagName('plot_dir')[0].childNodes[0].nodeValue
plot_dir="../"+plot_dir

chunk_size=None
file_size_distribution=None
queue_limit=None

#plot settings
legend_pos = (0.5,-0.2)
style.use('ieee.transaction')
# pl.rcParams['lines.linewidth'] = 2
# pl.rcParams['font.weight']="large"
# pl.rcParams['legend.loc'] = 'best'
# pl.rcParams['legend.set_bbox_to_anchor'] = (1,0.5)
pl.rc('legend', loc='upper center')#, bbox_to_anchor=(1, 0.5))#, color='r')
# pl.rcParams['legend.fancybox']=True#, shadow=True
# pl.rcParams['legend.bbox_to_anchor']=(1, 0.5)
# pl.rcParams['legend.bbox_to_anchor']=(1, 0.5)
# pl.rcParams['bbox_to_anchor']=(1, 0.5)
# pl.legend(bbox_to_anchor=(1, 0.5))
markerslist=["o","v","^","s","*","D","p","<", ">", "H", "1", "2","3", "4"]
# markerslist=["o","o","v","v","^","^","s","s","*","*","D","D","p","p","<","<"]
# markerslist=["x","x","x","x","x"]
pl.rcParams['savefig.dpi']=300

def plot_graphs(exp_nums,filename):
	global markerslist, chunk_size, file_size_distribution, queue_limit
	fig=pl.figure()
	local_marker_list = markerslist[:]
	loads_array=[]
	y_array=[]
	label_array=[]
	for i in exp_nums:
		
		exp_num=str(i)
		read_directory = log_dir+"exp"+exp_num+"/analysis/averages"
		conf = minidom.parse(log_dir+'exp'+exp_num+'/config.xml')
		configurations = conf.getElementsByTagName('config')
		copy=configurations[0].getElementsByTagName('copies')[0].childNodes[0].nodeValue
		priQ=configurations[0].getElementsByTagName('use_different_priorities')[0].childNodes[0].nodeValue
		cancellation=configurations[0].getElementsByTagName('cancellation')[0].childNodes[0].nodeValue
		purging=configurations[0].getElementsByTagName('purging')[0].childNodes[0].nodeValue

		queue_limit=configurations[0].getElementsByTagName('queue_limit')[0].childNodes[0].nodeValue
		file_size_distribution=configurations[0].getElementsByTagName('file_size_distribution')[0].childNodes[0].nodeValue
		chunk_size=configurations[0].getElementsByTagName('chunk_size')[0].childNodes[0].nodeValue
		
		filepath=read_directory+"/"+filename
		
		# if int(i)==104:
		# 	# pl.plot(-1000,-1000,marker=local_marker_list.pop(0)) #dummy 
		# 	pl.plot(-1000,-1000,marker=local_marker_list.pop(0)) #dummy 


		loads = []
		y = []
		with open(filepath, 'r') as csvfile:
			for line in csvfile:
				lineList = line.split(",")
				loads.append(lineList[0])
				y.append(lineList[1].split("\n")[0])

		if(int(copy)==1):
			lab = "Single Request"
		else:
			lab = str(copy)+"-copies"
			#lab = "Two Requests"
			if int(priQ) and int(purging): #by default cancellation is on if purging is on.
				lab+=" - Duplicate\nAware Scheduling"
			else:
				if int(priQ):
					lab=lab+" - with priority queues"
				if int(purging):
					lab=lab+" - with purging"
				elif int(cancellation):
					lab=lab+" - with cancellation"

			
		pl.plot(loads, y, label=lab,marker=local_marker_list.pop(0))
		loads_array.append(loads)
		y_array.append(y)
		label_array.append(lab)




	lg = pl.legend(bbox_to_anchor=legend_pos)#loc='best', fancybox=True)#, shadow=True)
	lg.draw_frame(True)
	# lg = pl.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	# lg.draw_frame(True)
	# pl.title("64MB chunks, 1Gbps links, 10 servers")	
	
	# pl.title(str(float(chunk_size)/1000000)+" MB\n"+file_size_distribution)
	# pl.text(-0.2,-0.2,"queue_limit: "+str(queue_limit), fontsize=8)
	pl.grid(True)
	# pl.yscale('log')
	

	# show the plot on the screen
	# pl.show()
	directory=plot_dir+"exp"+str(exp_nums)
	if not os.path.exists(directory):
		os.mkdir( directory );


	if filename.startswith("afct") or filename.startswith("percentile"):
		pl.xlabel("Load (%)")
		pl.ylabel("Request Completion Time (s)")
		# pl.ylim([0.0008,0.0014])
		# pl.ylim([0.0008,0.005])
		# pl.ylim([0.0005,0.004])
		pl.ylim([0.05,20])
		pl.xlim([0,90])
		# # pl.yscale('log')
		# fig.savefig(directory+"/"+filename[:-4]+"_scaled.png", bbox_inches='tight', dpi=resolution, transparent=False)
		# pl.ylim([0.0,0.025])
		# pl.xlim([0.0,80])
		# pl.ylim([0,0.18])
	elif filename.startswith("fasterRedundant"):
		pl.xlabel("Load (%)")
		pl.ylabel("fraction of redundant requests completing first")
	elif filename.startswith("equiflows"):
		pl.xlabel("Load (%)")
		pl.ylabel("fraction of redundant requests completing at the same time as original")
	elif filename.startswith("flowContentions"):
		pl.xlabel("original flows over time")
		pl.ylabel("contention experienced")
	elif filename.startswith("fasterOrEqualRedundant"):
		pl.xlabel("Load (%)")
		pl.ylabel("fraction of redundant requests completing within(<=) the time of original")
	fig.savefig(directory+"/"+filename[:-4]+".png", bbox_inches='tight', transparent=False)

	pl.cla()   # Clear axis
	pl.clf()   # Clear figure
	pl.close() # Close a figure window
	return loads_array, y_array, label_array

def plot_flow_contentions(exp_num, exp_nums):
	global markerslist
	exp_num=str(exp_num)
	read_directory = log_dir+"exp"+exp_num+"/analysis/averages"
	conf = minidom.parse(log_dir+'exp'+exp_num+'/config.xml')
	configurations = conf.getElementsByTagName('config')
	copies=configurations[0].getElementsByTagName('copies')[0].childNodes[0].nodeValue
	priQ=configurations[0].getElementsByTagName('use_different_priorities')[0].childNodes[0].nodeValue
	purging=configurations[0].getElementsByTagName('purging')[0].childNodes[0].nodeValue

	directory=plot_dir+"exp"+str(exp_nums)
	if not os.path.exists(directory):
		os.mkdir( directory );

	files=[]
	for file in os.listdir(read_directory):
		if file.startswith("flowContentions"):
			files.append(file)
	
	while files:
		current_files = []
		current_files.append(files.pop())
		# print current_files[0][:-5]
		for k in xrange(1,int(copies)+1):
			try:
				i=files.index(current_files[0][:-5]+str(k)+".csv")
				current_files.append(files.pop(i))
				# print i
			except:
				pass
		#plot figure
		# print current_files
		fig=pl.figure()
		local_marker_list = markerslist[:]
		for f in current_files:
			flowIds=[]
			contentions=[]
			with open(read_directory+"/"+f, 'r') as csvfile:
				for line in csvfile:
					lineList = line.split(",")
					flowIds.append(lineList[0])
					contentions.append(lineList[1].split("\n")[0])
			lab=f[-5:-4]
			pl.plot(flowIds, contentions, label=lab,marker=local_marker_list.pop(0))
		lg = pl.legend(bbox_to_anchor=legend_pos)#(loc='center left', bbox_to_anchor=(1, 0.5))
		lg.draw_frame(True)
		t =f[-8:-6]
		if int(priQ):
			t=t+" - with queues"
		if int(purging):
			t=t+" - with purging"
		pl.title(t)
		pl.ylim([0,25])
		pl.xlim([2000,2500])

		fig.savefig(directory+"/exp"+exp_num+"_"+f[-8:-6]+".png", bbox_inches='tight',  transparent=False)
		pl.cla()   # Clear axis
		pl.clf()   # Clear figure
		pl.close() # Close a figure window



exp_nums=[] 
for exp_num_str in sys.argv[1:]:
# 	# exp_nums.append(int(exp_num_str)) #first exp number is the baseline
	exp_nums.append(exp_num_str) #first exp number is the baseline
print "Plotting experiment(s) "+str(exp_nums)+" ..."

for file in os.listdir(log_dir+"exp"+str(exp_nums[0])+"/analysis/averages"):
	if not file.startswith("contention") and not file.startswith("flowContentions"):
		# print file
		a,b,c = plot_graphs(exp_nums,file)
		if(len(exp_nums)>=2):
			#plot gains
			if (file.startswith("afct") or file.startswith("percentile")):
				i=0
				fig2=pl.figure()
				local_marker_list = markerslist[:]
				# pl.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'y','c', 'm', 'y', 'k']) +
	   #                     cycler('linestyle', ['-', '--', ':', '-.'])))
				for y in b[1:]:

					i+=1
					x= [((float(m)-float(n))/float(m))*100.0 for m, n in zip(b[0], y) if float(m) is not 0.0]
					if i==1:
						pl.plot(a[i],x,marker=local_marker_list.pop(0), visible=False) #dummy 
					pl.plot(a[i], x, label=c[i],marker=local_marker_list.pop(0))
					# if i==3:
					# 	pl.plot(-1000,-1000,marker=local_marker_list.pop(0)) #dummy 

					# print file
					# print c[i]
					# print x
				# pl.title("64MB chunks, 1Gbps links, 10 servers")	
				pl.ylim([-5,100])
				# pl.ylim([0,20])
				# pl.xlim([0,70])
				pl.axhline(0, color='black', linestyle='--')

				lg = pl.legend(bbox_to_anchor=legend_pos)#(loc='best', fancybox=True)#, shadow=True)
				lg.draw_frame(True)
				pl.title(str(float(chunk_size)/1000000)+" MB\n"+file_size_distribution)
				# pl.text(-0.2,-0.2,"queue_limit: "+str(queue_limit), fontsize=8)


				# lg = pl.legend(loc='center left', bbox_to_anchor=(1, 0.5))
				# lg.draw_frame(True)

				# pl.xlim([0,80])
				# pl.ylim([0,50])
				pl.xlabel("Load (%)")
				pl.grid(True)
				if (file.startswith("afct")):
					pl.ylabel("Average Improvement (%)")
				else:
					pl.ylabel(file[-6:-4]+"th Percentile Improvement (%)")
				fig2.savefig(plot_dir+"exp"+str(exp_nums)+"/"+file[:-4]+"_gains.png", bbox_inches='tight',  transparent=False)


# for exp_num in exp_nums:
	# plot_flow_contentions(exp_num, exp_nums)
print "Experiment(s) "+str(exp_nums)+" plotting complete\n************************************\n"
	