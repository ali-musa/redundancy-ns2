#!/bin/sh

function read_exp_num {
	rdom () { local IFS=\> ; read -d \< E C ;}
	while rdom; do
	    if [[ $E = experiment_number ]]; then
	        echo $C
	        exit
	    fi
	done < config.xml
}
exp_num=$(read_exp_num)

#set params
loads="1 10 20 30 40 50 60 70 80 90 95"

echo "Exp"$exp_num": starting runs..."

screenNo=1

for load in $loads
do
	#deploy screen
    screen -S "exp"$exp_num"" -d -m ns llvr.tcl "$load" "$1"
    sleep 1
    echo "screen "$screenNo" spawned and detached"
    screenNo=$((screenNo + 1))
done
echo "deployed all screens"

#wait for any running screens
echo "waiting for screens to terminate..."
while screen -list | grep -q "exp"$exp_num""
do
    sleep 2
done
echo "all screens terminated"

echo "simulation complete exiting..."