# generates script checks experiments on emulab

exp_num="31"

password="emulab2014"
experiment_name="redundancy3"

output_script_path="check_emulab_exps.sh"
f = open(output_script_path,'w')
f.write("#!/bin/sh -e\n")
f.write("echo \"checking for exp"+exp_num+"\"\n")
for load in [1,10,20,30,40,50,60,70,80,90,95]:
	f.write("echo \"Checking exp for "+str(load)+"% load\"\n")
	f.write("sshpass -p "+password+" ssh -oStrictHostKeyChecking=no alimusa@node"+str(load)+"."+experiment_name+".comp150.emulab.net 'bash -s' <<'ENDSSH'\n")
	f.write("if screen -ls | grep exp"+exp_num+" \n")
	f.write("then\n")
	f.write("echo \"working for laod "+str(load)+"\"\n")
	f.write("else\n")
	f.write("echo \"NOT working for laod "+str(load)+"\"\n")
	f.write("fi\n")
	f.write("sleep 3\n")
	f.write("ENDSSH\n")
	f.write("wait\n")
f.close()
