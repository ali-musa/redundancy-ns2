#set params
loads="1 10 20 30 40 50"
copies="1 2"


#read last experiment number
exp_num=$(xmlstarlet sel -t -m "/config" -v "experiment_number" config.xml)
#update experiment number
exp_num=$((exp_num + 1))

echo "Exp"$exp_num": starting runs..."
 #read log dir path
log_dir=$(xmlstarlet sel -t -m "/config" -v "log_dir" config.xml)
mkdir ""$log_dir"exp"$exp_num""

#update config file
xmlstarlet ed -L -u "//config/experiment_number" -v $exp_num config.xml

screenNo=1
# for failures in 0 1
# do
	for copy in $copies
	do
        for load in $loads
        do
            #update config file
            xmlstarlet ed -L -u "//config/percent_load" -v $load config.xml
            xmlstarlet ed -L -u "//config/copies" -v $copy config.xml  

        	#deploy screen
            screen -S "exp"$exp_num"" -d -m ns llvr.tcl
            # ns llvr.tcl
            # wait
            sleep 1
            echo "screen "$screenNo" spawned and detached"
            screenNo=$((screenNo + 1))
	    done
        # echo "waiting for screens to terminate..."
        # while screen -list | grep -q "exp"$exp_num""
        # do
        #     sleep 2
        # done
	done
# done
echo "deployed all screens"

#wait for any running screens
echo "waiting for screens to terminate..."
while screen -list | grep -q "exp"$exp_num""
do
    sleep 2
done
echo "all screens terminated"

#analyze logs
echo "analyzing logs..."

# for failures in 0 1
# do
    for copy in $copies
    do
        for load in $loads
        do
           
            #update config file
            xmlstarlet ed -L -u "//config/percent_load" -v $load config.xml
            xmlstarlet ed -L -u "//config/copies" -v $copy config.xml  

            python analyze_logs.py
            wait
        done
    done
# done

echo "analysis complete"

echo "plotting graphs..."
python plot_afcts.py
wait
echo "plotting complete"
echo "simulation complete exiting..."