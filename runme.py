from xml.dom import minidom
import os
import os.path

#config params
copy="2"
priQ="1"
cancellation="1"
purging="1"
failures="0"
file_size_distribution="deterministic" #deterministic or pareto
queue_limit="300"
average_over_runs = 5
chunk_size=10000000.0 #in bytes

cluster=1

source_file="llvr.tcl"
config_file="config.xml"
if cluster:
	batch_file="run_batch_loads.py"
else:
	batch_file="run_batch_loads.sh"
working_dir = os.getcwd()


#load configurations
mainconf = minidom.parse('main_config.xml')
mainconfigurations = mainconf.getElementsByTagName('config')
log_dir=mainconfigurations[0].getElementsByTagName('log_dir')[0].childNodes[0].nodeValue

conf = minidom.parse(config_file)
configurations = conf.getElementsByTagName('config')

#read last experiment number
exp_num=configurations[0].getElementsByTagName('experiment_number')[0].childNodes[0].nodeValue
exp_num=int(exp_num)+1

print "spawning experiment "+str(exp_num)+" ..."
# update config file
configurations[0].getElementsByTagName('experiment_number')[0].childNodes[0].replaceWholeText(exp_num)
configurations[0].getElementsByTagName('copies')[0].childNodes[0].replaceWholeText(copy)
configurations[0].getElementsByTagName('use_different_priorities')[0].childNodes[0].replaceWholeText(priQ)
configurations[0].getElementsByTagName('cancellation')[0].childNodes[0].replaceWholeText(cancellation)
configurations[0].getElementsByTagName('purging')[0].childNodes[0].replaceWholeText(purging)
configurations[0].getElementsByTagName('failures')[0].childNodes[0].replaceWholeText(failures)
configurations[0].getElementsByTagName('file_size_distribution')[0].childNodes[0].replaceWholeText(file_size_distribution)
configurations[0].getElementsByTagName('queue_limit')[0].childNodes[0].replaceWholeText(queue_limit)
configurations[0].getElementsByTagName('chunk_size')[0].childNodes[0].replaceWholeText(chunk_size)

file_handle = open(config_file,"wb")
conf.writexml(file_handle)
file_handle.flush()
os.fsync(file_handle)

#copy config and make exp directory
os.system("mkdir "+log_dir+"exp"+str(exp_num))
os.system("cp "+config_file+" "+log_dir+"exp"+str(exp_num))
os.system("cp "+source_file+" "+log_dir+"exp"+str(exp_num))
os.system("cp ./automated_scripts/"+batch_file+" "+log_dir+"exp"+str(exp_num))

os.chdir(log_dir+"exp"+str(exp_num)+"/")
os.system("sleep 0.5")
os.system("wait")

for seed in xrange(1,average_over_runs+1):
    print "running for seed: "+str(seed)
    if cluster:
    	os.system("python "+batch_file+" "+str(seed))
    else:
    	os.system("screen -S \"main_experiment"+str(exp_num)+"\" -d -m sh "+batch_file+" "+str(seed))
    	os.system("sleep 1")
    os.system("sleep 1")
os.system("cd "+working_dir)
os.system("sleep 0.25")

conf.unlink()
# if(not os.path.isfile(fname)):

with open("../details.txt", "a") as text_file:
    text_file.write("Experiment Number: %s\n" % exp_num)
    text_file.write("Average Over Runs: %s\n" % average_over_runs)
    text_file.write("Chunk Size: %s\n" % chunk_size)
    text_file.write("File Size Distribution: %s\n" % file_size_distribution)
    text_file.write("Queue Limit: %s\n" % queue_limit)
    text_file.write("Copies: %s\n" % copy)
    text_file.write("Failures: %s\n" % failures)
    text_file.write("Using Queues: %s\n" % priQ)
    text_file.write("Cancellation: %s\n" % cancellation) 
    text_file.write("Purging: %s\n-----------------------\n\n" % purging) 

print "experiment "+str(exp_num)+" spawned"