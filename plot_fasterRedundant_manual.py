import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as pl
from xml.dom import minidom

#load configurations
mainconf = minidom.parse('config.xml')
mainconfigurations = mainconf.getElementsByTagName('config')
log_dir=mainconfigurations[0].getElementsByTagName('log_dir')[0].childNodes[0].nodeValue
plot_dir=mainconfigurations[0].getElementsByTagName('plot_dir')[0].childNodes[0].nodeValue

exp_nums=[206]
fig=pl.figure()
for i in exp_nums:
	print i
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
		priQ_string=" - with priority queues"
	else:
		priQ_string=""
	#plot each copy on the same graph

	# for copy in xrange(1,int(max_copies)+1):
	loads = []
	percentFaster = []
	with open(log_dir+"exp"+exp_num+"/fasterRedundant_"+str(copy)+"copies_manual.csv", 'r') as csvfile:
		for line in csvfile:
			lineList = line.split(",")
			loads.append(lineList[0])
			percentFaster.append(lineList[1])
	# pl.plot(loads, percentFaster, label=str(copy)+'-copies'+priQ_string,marker='x')
	pl.plot(loads, percentFaster, label="duplicate request - with RANS",marker='x')



# conf = minidom.parse(log_dir+'exp'+exp_num2+'/config.xml')
# configurations = conf.getElementsByTagName('config')
# max_copies=configurations[0].getElementsByTagName('copies')[0].childNodes[0].nodeValue
# max_flows=configurations[0].getElementsByTagName('number_of_flows')[0].childNodes[0].nodeValue
# num_servers=configurations[0].getElementsByTagName('number_of_servers')[0].childNodes[0].nodeValue
# sim_time=configurations[0].getElementsByTagName('simulation_time')[0].childNodes[0].nodeValue
# chunk_size=configurations[0].getElementsByTagName('chunk_size')[0].childNodes[0].nodeValue
# link_bw=configurations[0].getElementsByTagName('link_bandwidth')[0].childNodes[0].nodeValue
# priQ=configurations[0].getElementsByTagName('use_different_priorities')[0].childNodes[0].nodeValue

# if int(priQ):
# 	priQ_string="using queues"
# else:
# 	priQ_string="without queues"
# #plot each copy on the same graph
# # fig=pl.figure()
# for copy in xrange(1,int(max_copies)+1):
# 	loads = []
# 	afcts = []
# 	with open(log_dir+"exp"+exp_num2+"/afct_"+str(copy)+"copies.csv", 'r') as csvfile:
# 		for line in csvfile:
# 			lineList = line.split(",")
# 			loads.append(lineList[0])
# 			afcts.append(lineList[1])
# 	pl.plot(loads, afcts, label=str(copy)+'-copies, '+num_servers+' server(s), '+priQ_string+'\n'+str(int(sim_time)/3)+'s flow generation, '+max_flows+' max flows')


# y=[0.536999050124
# ,0.5535295046
# ,0.59883677086
# ,0.707405446887
# ,0.856723028971
# ,1.09702644377
# ,1.48850090808
# ,2.03591704841
# ,2.80059602609
# ,3.67739562934
# ,4.5172303477]
# pl.plot(loads,y, label='2-copies with priority queues')

y2=[0.640090700034
,0.695813831832
,0.83333438198
,1.02984648709
,1.29095171578
,1.60550417687
,2.05484581137
,3.15099354773
,5.9117910034
,30.9861941568]

# pl.plot(loads[1:-1],y2[:-1],label='without cbq')
# pl.title('flows gemerated for 1000s, single server')
# pl.legend(loc='center left', bbox_to_anchor=(1, 0.5),
#           fancybox=True, shadow=True)
lg = pl.legend(loc='best',
          fancybox=True, shadow=True)
lg.draw_frame(False)
# pl.title("64MB chunks, 1Gbps links, 10 servers")	
pl.xlabel("% load")
pl.ylabel("% redundant requests completing first")
pl.grid(True)

# pl.yscale('log')
# pl.xlim([50,100])
# pl.ylim([0,5])

# show the plot on the screen
# pl.show()
fig.savefig(plot_dir+"/manual/exps"+str(exp_nums)+"_faster.png", bbox_inches='tight', dpi=1200, transparent=True)
