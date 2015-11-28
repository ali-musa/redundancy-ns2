# generates script that starts experiments on emulab

copy="2"
priQ="0"
purging="0"

source_file="llvr.tcl"
output_script_path="run_emulab_exps.sh"
password="emulab2014"
experiment_name="redundancy3"

f = open(output_script_path,'w')
f.write("#!/bin/sh -e\n")
f.write("sshpass -p "+password+" scp "+source_file+" alimusa@nodespare."+experiment_name+".comp150.emulab.net:/users/alimusa/redundancy/\n\n")
for load in [1,10,20,30,40,50,60,70,80,90,95]:
	f.write("echo \"spawning exp for "+str(load)+"% load\"\n")
	f.write("sshpass -p "+password+" ssh -oStrictHostKeyChecking=no alimusa@node"+str(load)+"."+experiment_name+".comp150.emulab.net 'bash -s' <<'ENDSSH'\n")
	f.write("load="+str(load)+"\n")
	f.write("copy="+copy+"\n")
	f.write("priQ="+priQ+"\n")
	f.write("purging="+purging+"\n")
	f.write("path=\"/users/alimusa/redundancy/\"\n")

	#read last experiment number
	f.write("exp_num=$(xmlstarlet sel -t -m \"/config\" -v \"experiment_number\" \"$path\"config.xml)\n")
	
	#update config file
	f.write("xmlstarlet ed -L -u \"//config/percent_load\" -v ${load} \"$path\"config.xml\n")
	f.write("xmlstarlet ed -L -u \"//config/copies\" -v ${copy} \"$path\"config.xml\n")
	f.write("xmlstarlet ed -L -u \"//config/use_different_priorities\" -v ${priQ} \"$path\"config.xml\n")
	f.write("xmlstarlet ed -L -u \"//config/purging\" -v ${purging} \"$path\"config.xml\n")
	if load==1:
		#update experiment number
		f.write("exp_num=$((exp_num + 1))\n")
		f.write("xmlstarlet ed -L -u \"//config/experiment_number\" -v $exp_num \"$path\"config.xml\n")
		#copy config
		f.write("log_dir=$(xmlstarlet sel -t -m \"/config\" -v \"log_dir\" \"$path\"config.xml)\n")
		f.write("mkdir \"\"$log_dir\"exp\"$exp_num\"\"\n")
		f.write("cp \"\"$path\"config.xml\" \"\"$log_dir\"exp\"$exp_num\"/config.xml\"\n")

	f.write("cd ${path}\n")
	f.write("sleep 2\n")
	f.write("screen -S \"exp\"$exp_num\"\" -d -m ~/./ns llvr.tcl\n")
	f.write("sleep 3\n")
	f.write("ENDSSH\n")
	f.write("wait\n")
	f.write("echo \"exp for "+str(load)+"% load spawned\"\n\n")
f.close()
##################


# echo "spawning exp for 10% load"
# sshpass -p emulab2014 ssh -oStrictHostKeyChecking=no alimusa@node10.redundancy.comp150.emulab.net 'bash -s' <<'ENDSSH'
# load=10
# copy=1
# priQ=1
# purging=0
# path="/users/alimusa/redundancy/"

# #read experiment number
# exp_num=$(xmlstarlet sel -t -m "/config" -v "experiment_number" "$path"config.xml)

# log_dir=$(xmlstarlet sel -t -m "/config" -v "log_dir" "$path"config.xml)


# xmlstarlet ed -L -u "//config/percent_load" -v ${load} "$path"config.xml
# xmlstarlet ed -L -u "//config/copies" -v ${copy} "$path"config.xml
# xmlstarlet ed -L -u "//config/use_different_queues" -v ${priQ} "$path"config.xml
# xmlstarlet ed -L -u "//config/purging" -v ${purging} "$path"config.xml

# cd ${path}
# screen -S "exp"$exp_num"" -d -m ~/./ns llvr.tcl
# sleep 1
# ENDSSH
# wait
# echo "exp for 10% load spawned"






# # f.write("#!/bin/sh -e\n")
# # f.write("#!/bin/sh -e\n")
# # f.write("#!/bin/sh -e\n")
# # f.write("#!/bin/sh -e\n")
# # f.write("#!/bin/sh -e\n")
# f.close()

