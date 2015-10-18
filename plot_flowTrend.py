import pylab as pl
from xml.dom import minidom


# #load configurations
# conf = minidom.parse('config.xml')
# configurations = conf.getElementsByTagName('config')

# exp_num=str(37)
# log_dir=configurations[0].getElementsByTagName('log_dir')[0].childNodes[0].nodeValue
# plot_dir=configurations[0].getElementsByTagName('plot_dir')[0].childNodes[0].nodeValue
# max_copies=str(2)

# #plot each copy on the same graph
# for copy in xrange(1,int(max_copies)+1):
# 	loads = []
# 	afcts = []
# 	with open(log_dir+"exp"+exp_num+"/afct_"+str(copy)+"copies.csv", 'r') as csvfile:
# 		for line in csvfile:
# 			lineList = line.split(",")
# 			loads.append(lineList[0])
# 			afcts.append(lineList[1])
# 	pl.plot(loads, afcts, label=str(copy)+'-copies')
# # 	 7.26489263797
# # AFCT2_25: 


# withoutPri = [5.3752277519, 5.7087956232,6.7883223169,7.74471767704,9.2917747478,20.486354142,244.893660869,739.23165331,958.344664736,1080.16962767,1176.27327442,1349.04050847]
# pl.plot([1,10,20,25,30,40,50,60,70,80,90,100], withoutPri, label='2-copies-without queues')
x = [100, 250, 500, 1000, 10000, 30000]
#at 10% load
y1 = [ 0.671809156743,0.623645641542,0.605064186989,0.607981045417,0.602592343757 ] 
# y2 = [0.836567149942, ] #with prio
y2 = [ 0.578029947151,0.569452850507,0.567115298029,0.571337744286, 0.570038477848] #without prio

#at 80% load
y3 = [1.19741103361,1.6885082463,2.18289491144,3.27340268619, 4.09895319544, 3.84059044685]
y4 = [1.59628027361,3.64660594791,7.48475235873,15.9328921131, 112.6437558]

pl.title("without queues, 30 servers, 64MB chunks, 1000Mbps links")
# pl.plot(x,y1, label='10%load_1-copy')
# pl.plot(x,y2, label='10%load_2-copy')
pl.plot(x,y3, label='80%load_1-copy')
# pl.plot(x,y4, label='80%load_2-copy')
pl.legend()	
pl.xlabel("number of flows (logscale)")
pl.ylabel("AFCTs")
pl.grid(True)
pl.xscale('log')
# pl.ylim([4,20])
# pl.xlim([0,100])


# show the plot on the screen
# pl.show()
# pl.savefig(plot_dir+"exp"+exp_num+"_6.png", bbox_inches='tight')
pl.savefig("flowplot_80%_logscale.png", bbox_inches='tight')