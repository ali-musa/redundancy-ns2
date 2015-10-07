package require tdom

# Open config file and read into a variable
set config_file [open config.xml r]
set config [read $config_file]
close $config_file

# Parse the config and get all config elements
set config_parse [dom parse $config]
set params [$config_parse getElementsByTagName config]

# Set the various config params
set exp_num [[$params selectNodes experiment_number/text()] data]
set simulation_time [[$params selectNodes simulation_time/text()] data]
set logging [[$params selectNodes logging/text()] data]
set log_dir [[$params selectNodes log_dir/text()] data]
set plot_dir [[$params selectNodes plot_dir/text()] data]
set N [[$params selectNodes number_of_servers/text()] data]
set k [[$params selectNodes copies/text()] data]
set percentageLoad [[$params selectNodes percent_load/text()] data]
set failures [[$params selectNodes failures/text()] data]
set numFlows [[$params selectNodes number_of_flows/text()] data]
set priQ [[$params selectNodes use_different_priorities/text()] data]
set chunkSize [[$params selectNodes chunk_size/text()] data]
set linkBW [[$params selectNodes link_bandwidth/text()] data]


#TODO: fix failures
#TODO: fix coded levels per cbq class

#trace start start time
set traceStartTime $logging
#trace start end time
set traceEndTime $logging

#Create a simulator object
set ns [new Simulator]

Agent/TCP set window_ 100000
Agent/TCP set packetSize_ 1000 


# set var [open "trace.tr" w]
# $ns trace-all $var


#Define a 'finish' procedure
proc finish {} {
	global starttracefile endtracefile traceStartTime traceEndTime startTimes endTimes N k percentageLoad failures numFlows priQ log_dir exp_num
	#flow start trace file
	if ($traceStartTime) {
		append starttracefileName $log_dir "exp" $exp_num "/starts" $N "_" $k "_" $percentageLoad "_" $failures "_" $numFlows "_" $priQ ".tr"
		set starttracefile [ open $starttracefileName w ]
		puts $starttracefile $startTimes
		close $starttracefile
	}
	#flow end trace file
	if ($traceEndTime) {
		append endtracefileName $log_dir "exp" $exp_num "/ends" $N "_" $k "_" $percentageLoad "_" $failures "_" $numFlows "_" $priQ ".tr"
		set endtracefile [ open $endtracefileName w ]
		puts $endtracefile $endTimes 
		close $endtracefile
	}
	exit 0

}

proc make_fmon cbqlink {

	$self instvar ns_ fmon_

	set fmon_ [$ns_ makeflowmon Fid]

	$ns_ attach-fmon $cbqlink $fmon_

}

Simulator instproc makeCBQlink {node1 node2 timeLink} {
	global priQ numFlows k

	set topClass [new CBQClass]

	set lowerClass [new CBQClass]

	# set lowerClass2 [new CBQClass]

	# set lowerClass3 [new CBQClass]

	# set lowerClass4 [new CBQClass]

	# set lowerClass5 [new CBQClass]

	# set lowerClass6 [new CBQClass]

	# set lowerClass7 [new CBQClass]


	set q1 [new Queue/DropTail]

	$q1 set limit_ 500

	$topClass install-queue $q1

	set q2 [new Queue/DropTail]

	$q2 set limit_ 500

	$lowerClass install-queue $q2

	# set q3 [new Queue/DropTail]

	# $q3 set limit_ 500

	# $lowerClass3 install-queue $q3

	# set q4 [new Queue/DropTail]

	# $q4 set limit_ 500

	# $lowerClass4 install-queue $q4

	# set q5 [new Queue/DropTail]

	# $q5 set limit_ 500

	# $lowerClass5 install-queue $q5

	# set q6 [new Queue/DropTail]

	# $q6 set limit_ 500

	# $lowerClass6 install-queue $q6

	# set q7 [new Queue/DropTail]

	# $q7 set limit_ 500

	# $lowerClass7 install-queue $q7

	# $cbqclass setparams parent okborrow allot maxidle prio level


	set cbqlink [$self link $node1 $node2]

	$topClass setparams none true 1.00 auto 0 1 0

	$lowerClass setparams none false 1.0 auto 1 1 0

	# $lowerClass2 setparams none false 1.0 auto 2 1 0

	# $lowerClass3 setparams none false 1.0 auto 3 1 0

	# $lowerClass4 setparams none false 1.0 auto 4 1 0

	# $lowerClass5 setparams none false 1.0 auto 5 1 0

	# $lowerClass6 setparams none false 1.0 auto 6 1 0

	# $lowerClass7 setparams none false 1.0 auto 7 1 0

	$cbqlink insert $topClass

	$cbqlink insert $lowerClass

	# $cbqlink insert $lowerClass2

	# $cbqlink insert $lowerClass3

	# $cbqlink insert $lowerClass4

	# $cbqlink insert $lowerClass5

	# $cbqlink insert $lowerClass6

	# $cbqlink insert $lowerClass7

	#$self make_fmon $cbqlink
	if {$priQ} {
		$cbqlink bind $topClass 1 $numFlows
		$cbqlink bind $lowerClass [expr $numFlows+1] [expr $numFlows*$k+1]
	} else {
		$cbqlink bind $topClass 1 [expr $numFlows*$k]
	}

		# $cbqlink bind $lowerClass2 10001 20000

		# $cbqlink bind $lowerClass3 20001 30000

		# $cbqlink bind $lowerClass4 30001 40000

		# $cbqlink bind $lowerClass5 40001 50000

		# $cbqlink bind $lowerClass6 50001 60000

		# $cbqlink bind $lowerClass7 60001 70000
}

#generate flows after a random interval
proc generateFlow {src dst size priority } {
	global ns
	
	set tcp [new Agent/TCP]
	$ns attach-agent $src $tcp

	set sink [new Agent/TCPSink]
	$ns attach-agent $dst $sink


	$tcp set fid_ $priority
	$sink set fid_ $priority

	$ns connect $tcp $sink

	$tcp set minrto_ 0
	#$tcp set maxrto_ 0.001
	$tcp set tcpTick_ 0.0001

	#Setup a FTP over TCP connection
	set ftp [new Application/FTP]
	$ftp attach-agent $tcp
	$ftp set type_ FTP
	$ftp send $size
}


proc generateFlows {flowsLeft priority} {
	global ns arrival_ chunkSize traceStartTime starttracefile fileSize_ servers n0 N numFlows k startTimes randServer randServer2

	if {$flowsLeft >= 1} {
		set primaryServerId -1
		
		for {set i 0} {$i < $k} {incr i} {
			#TODO: Duplicates must not hit the same server!
			#TODO?: make this generic for priorities
			set curr_priority [expr $i*$numFlows+$priority]
			set serverId -1
			if {$i==0} {
				#primary flow
				set serverId [format "%-1.0f" [$randServer value]]
				set primaryServerId $serverId
			} else {
				set serverId [format "%-1.0f" [$randServer2 value]]
				#duplicate flow should not collide with the primary server
				while {$serverId==$primaryServerId} {
					set serverId [format "%-1.0f" [$randServer2 value]]				
				}
			}
			set now [$ns now]	
			$ns at $now "generateFlow $servers($serverId) $n0 $chunkSize $curr_priority"
			if ($traceStartTime) {
				append startTimes $now " " [expr $curr_priority] " " [expr $serverId+1] "\n"
			}
		}
				
		#update arguments
		set priority [expr $priority+1]
		set flowsLeft [expr $flowsLeft-1]

		set nextArrival [expr $now+[format "%-8.3f" [$arrival_ value]]]
		# set nextArrival [expr $now+$arrivalTimes([expr $numFlows-$flowsLeft-1])]
		#call the function again after time
		$ns at $nextArrival "generateFlows $flowsLeft $priority"
		# $ns at [expr $now+$meanInterArrivalTime] "generateFlow $src $dst $flowsLeft $priority"

	}

}

proc generateFailures { src dst } {
	global ns u n1 n2 rtmodel
	set now [$ns now]
	# puts $now
	$ns rtmodel-at 4.2 down $n1 $n2
	# $ns rtmodel-at $now down $n1 $n2
	set recoverAt [expr 80+$now]
	# $ns at $recoverAt "recoverFailures $src $dst"

}


proc recoverFailures { src dst } {
	global ns u n1 n2
	set now [$ns now]
	$ns rtmodel-at $now up $n1 $n2
	set failAt [expr [$u value]+$now]
	$ns at $failAt "generateFailures $src $dst"
}


#topology
#
#		n0
#	   /| \
#	  / |  \
#	 /  |	\
#	n1 n2...nN



#create sink
set n0 [$ns node]

array set servers {}
#Create N servers
for {set i 0} {$i <$N} {incr i} {
	set servers($i) [$ns node]
	$ns simplex-link $n0 $servers($i) $linkBW 0.00ms CBQ
	$ns simplex-link $servers($i) $n0 $linkBW 0.00ms CBQ
	$ns queue-limit $n0 $servers($i) 1000
	$ns queue-limit $servers($i) $n0 1000
	$ns makeCBQlink $n0 $servers($i) 1
	$ns makeCBQlink $servers($i) $n0 1
}


#calculate inter arrvial time
set BW [expr [string range $linkBW 0 [string length $linkBW]-3]*1000000.0]
# puts $BW
set size [expr $chunkSize*8.0]
set loadFactor [expr 100.0/$percentageLoad]
set meanInterArrivalTime [expr $size*$loadFactor/$BW]
#for N servers
set meanInterArrivalTime [expr $meanInterArrivalTime/$N]

#arrival distribution
$defaultRNG seed 101
set arrivalRNG [new RNG]
set arrival_ [new RandomVariable/Exponential]
$arrival_ set avg_ $meanInterArrivalTime
$arrival_ use-rng $arrivalRNG

#file size distribution
set fileSizeRng [new RNG]
set fileSize_ [new RandomVariable/Exponential]
$fileSize_ set avg_ $chunkSize
$fileSize_ use-rng $fileSizeRng

#primary server selection distribution
set serverRNG [new RNG]
set randServer [new RandomVariable/Uniform]
$randServer set min_ 0
$randServer set max_ [expr $N-1]
$randServer use-rng $serverRNG

#secondary server selection distribution
set server2RNG [new RNG]
set randServer2 [new RandomVariable/Uniform]
$randServer2 set min_ 0
$randServer2 set max_ [expr $N-1]
$randServer2 use-rng $server2RNG


$ns at 4.0 "generateFlows $numFlows 1"

if {$failures == 1} {
	#failures
	puts "generating failures"
	set uRNG [new RNG]
	set u [new RandomVariable/Uniform]
	$u set min_ 0.2
	$u set max_ 1
	$u use-rng $uRNG
	set rRNG [new RNG]
	set r [new RandomVariable/Uniform]
	$r set min_ 0.2
	$r set max_ 1
	$r use-rng $rRNG
	set failAt 4

	for {set j 0} {$j <2000} {incr j} {
		# puts $failAt
		$ns rtmodel-at $failAt down $n1 $n2
		set recoverAt [expr $failAt+[format "%-8.3f" [$r value]]]
		$ns rtmodel-at $recoverAt up $n1 $n2
		set failAt [expr $recoverAt+[format "%-8.3f" [$u value]]]
	}
	# set firstFailureAt [expr $now+4]
	# $ns at $firstFailureAt "generateFailures $n1 $n2"
	# $ns rtmodel-at 4.2 down $n1 $n2
	# $ns at 4.2 "generateFailures $n1 $n2"


	# $ns rtmodel-at 9.0 up $n2 $n1
	# $ns rtmodel-at 7.1 down $n3 $n4
	
} else {
	#no failures
	puts "generating no failures"
}
Agent/TCP instproc done {} {
	global ns endtracefile traceEndTime endTimes
	if ($traceEndTime) {
		set now [$ns now]
		set thisNode [$self set node_]
		append endTimes $now " " [$self set fid_] " " [$thisNode id] "\n"
	}
}

#Call the finish procedure after 5 seconds of simulation time

$ns at $simulation_time "finish"


#Run the simulation

$ns run
