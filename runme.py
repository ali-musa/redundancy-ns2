from xml.dom import minidom
import os
import time
import os.path

copy="1"
priQ="0"
purging="0"
failures="0"

cluster=0

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
configurations[0].getElementsByTagName('purging')[0].childNodes[0].replaceWholeText(purging)
configurations[0].getElementsByTagName('failures')[0].childNodes[0].replaceWholeText(failures)

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

if cluster:
	os.system("python "+batch_file)
else:
	os.system("screen -S \"main_experiment"+str(exp_num)+"\" -d -m sh "+batch_file)
	os.system("sleep 1")

os.system("wait")
time.sleep(0.5)
os.system("cd "+working_dir)


chunk_size=configurations[0].getElementsByTagName('chunk_size')[0].childNodes[0].nodeValue
file_size_distribution=configurations[0].getElementsByTagName('file_size_distribution')[0].childNodes[0].nodeValue
conf.unlink()
# if(not os.path.isfile(fname)):

with open("../details.txt", "a") as text_file:
    text_file.write("Experiment Number: %s\n" % exp_num)
    text_file.write("Chunk Size: %s\n" % chunk_size)
    text_file.write("File Size Distribution: %s\n" % file_size_distribution)
    text_file.write("Copies: %s\n" % copy)
    text_file.write("Failures: %s\n" % failures)
    text_file.write("Using Queues: %s\n" % priQ)
    text_file.write("Purging: %s\n-----------------------\n\n" % purging) 

print "experiment "+str(exp_num)+" spawned"