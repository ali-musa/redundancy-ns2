import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as pl
from xml.dom import minidom

#load configurations
mainconf = minidom.parse('config.xml')
mainconfigurations = mainconf.getElementsByTagName('config')
log_dir=mainconfigurations[0].getElementsByTagName('log_dir')[0].childNodes[0].nodeValue
plot_dir=mainconfigurations[0].getElementsByTagName('plot_dir')[0].childNodes[0].nodeValue

exp_nums=[202,204,206]
base_exp=202

base_afcts=[]

fig=pl.figure()
for i in exp_nums:
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
		priQ_string="with priority queues"
	else:
		priQ_string="without priority queues"
	#plot each copy on the same graph

	# for copy in xrange(1,int(max_copies)+1):
	loads = []
	afcts = []
	with open(log_dir+"exp"+exp_num+"/afct_"+str(copy)+"copies.csv", 'r') as csvfile:
		for line in csvfile:
			lineList = line.rstrip().split(",")
			# lineList = lineList.split("\n")
			loads.append(lineList[0])
			afcts.append(lineList[1])
	if i==base_exp:
		base_afcts = afcts
	else:
		percent_gains = [((float(x)-float(y))/float(x))*100.0 for x, y in zip(base_afcts, afcts)]
		# pl.plot(loads[:-2], percent_gains[:-2], label=str(copy)+'-copies, '+num_servers+' server(s), '
		# 	+priQ_string+'\n'+str(int(sim_time)/3)+'s flow generation, '+max_flows+' max flows'
		# 	,marker='x')
		# pl.plot(loads[:-2], percent_gains[:-2], label=str(copy)+'-copies, '+priQ_string,marker='x')
		if int(priQ):
			pl.plot(loads[:-2], percent_gains[:-2], label="duplicate requests - with RANS",marker='x')

		else:
			pl.plot(loads[:-2], percent_gains[:-2], label="duplicate requests",marker='x')








# pl.plot(loads[1:-1],y2[:-1],label='without cbq')
# pl.title('flows gemerated for 1000s, single server')
# pl.legend(loc='center left', bbox_to_anchor=(1, 0.5),
          # fancybox=True, shadow=True)	
lg=pl.legend(loc='best',
          fancybox=True, shadow=True)
lg.draw_frame(False)	

pl.xlabel("percentage load")
pl.ylabel("percentage gains")
pl.grid(True)
# pl.yscale('log')
# pl.xlim([0,150])
pl.ylim([-20,20])

# show the plot on the screen
# pl.show()
fig.savefig(plot_dir+"/gains/"+str(exp_nums)+"_scaled.png", bbox_inches='tight', dpi=1200, transparent=True)
