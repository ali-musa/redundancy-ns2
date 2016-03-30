#!/cluster/home/aiftik01/redundancy/ns-allinone-2.35/bin/ns
set percentageLoad -1
if { $argc < 1 } {
        puts "Usage: <*.tcl> <%load> <seed (optional)>"
        exit
    } else {
       set percentageLoad [lindex $argv 0]
    }

set seed_value 1
if {$argc>1} {
	set seed_value [lindex $argv 1]
}
expr srand($seed_value)


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
set logging [[$params selectNodes logging/text()] data]
set N [[$params selectNodes number_of_servers/text()] data]
set k [[$params selectNodes copies/text()] data]
# set percentageLoad [[$params selectNodes percent_load/text()] data]
set failures [[$params selectNodes failures/text()] data]
set numFlows [[$params selectNodes number_of_flows/text()] data]
set priQ [[$params selectNodes use_different_priorities/text()] data]
set chunkSize [[$params selectNodes chunk_size/text()] data]
set linkBW [[$params selectNodes link_bandwidth/text()] data]
set cancellation [[$params selectNodes cancellation/text()] data]
set purging [[$params selectNodes purging/text()] data]
set file_size_distribution [[$params selectNodes file_size_distribution/text()] data]
set queue_limit [[$params selectNodes queue_limit/text()] data]


puts "percent_load: $percentageLoad"
puts "copies: $k"
puts "priority queues: $priQ"
puts "cancellation: $cancellation"
puts "purging: $purging"
puts "file_size_distribution: $file_size_distribution"
puts "queue_limit: $queue_limit"
puts "experiment_number: $exp_num"



array set ftp {}
array set sink {}
#for purging
array set flowID_to_server_map {}
# array set running_flows {}



set fct_ideal 0
#TODO: fix failures
#TODO: fix coded levels per cbq class

#Create a simulator object
set ns [new Simulator]
#$ns rtproto DV


Agent/TCP set window_ 100000
# Agent/TCP set packetSize_ 1000 

# set var [open "trace.tr" w]
# $ns trace-all $var


#Define a 'finish' procedure
proc finish {} {
	# global failureTrace logging startTimes endTimes N k percentageLoad failures numFlows priQ failures
	global failureTrace logging startTimes endTimes percentageLoad failures seed_value
	if ($logging) {
		#flow start trace file
		# append starttracefileName "./starts" $N "_" $k "_" $percentageLoad "_" $failures "_" $numFlows "_" $priQ ".tr"
		append starttracefileName "./starts" $percentageLoad "_" $seed_value ".tr"
		set starttracefile [ open $starttracefileName w ]
		puts $starttracefile $startTimes
		close $starttracefile
		#flow end trace file
		# append endtracefileName "./ends" $N "_" $k "_" $percentageLoad "_" $failures "_" $numFlows "_" $priQ ".tr"
		append endtracefileName "./ends" $percentageLoad "_" $seed_value ".tr"
		set endtracefile [ open $endtracefileName w ]
		puts $endtracefile $endTimes 
		close $endtracefile
		if ($failures) {
			#failure trace file
			# append failureTraceFilename "./failures" $N "_" $k "_" $percentageLoad "_" $failures "_" $numFlows "_" $priQ ".tr"
			append failureTraceFilename "./failures" $percentageLoad "_" $seed_value ".tr"
			set failureTraceFile [ open $failureTraceFilename w ]
			puts $failureTraceFile $failureTrace 
			close $failureTraceFile
		}
	}
	exit 0

}

proc make_fmon cbqlink {

	$self instvar ns_ fmon_

	set fmon_ [$ns_ makeflowmon Fid]

	$ns_ attach-fmon $cbqlink $fmon_

}

Simulator instproc makeCBQlink {node1 node2 timeLink} {
	global priQ numFlows k queue_limit

	set topClass [new CBQClass]

	set lowerClass [new CBQClass]

	# set lowerClass2 [new CBQClass]

	# set lowerClass3 [new CBQClass]

	# set lowerClass4 [new CBQClass]

	# set lowerClass5 [new CBQClass]

	# set lowerClass6 [new CBQClass]

	# set lowerClass7 [new CBQClass]


	set q1 [new Queue/DropTail]

	$q1 set limit_ [expr $queue_limit/2]

	$topClass install-queue $q1

	set q2 [new Queue/DropTail]

	$q2 set limit_ [expr $queue_limit/2]

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
	return $cbqlink

}
#generate flows after a random interval
proc generateFlow {src dst size priority } {
	global ns numFlows ftp sink
	
	set tcp [new Agent/TCP]
	$ns attach-agent $src $tcp

	set sink($priority) [new Agent/TCPSink]
	$ns attach-agent $dst $sink($priority)

	$tcp set fid_ $priority
	$sink($priority) set fid_ $priority

	$ns connect $tcp $sink($priority)

	$tcp set minrto_ 0
	#$tcp set maxrto_ 0.001
	$tcp set tcpTick_ 0.0001

	#Setup a FTP over TCP connection
	set ftp($priority) [new Application/FTP]
	$ftp($priority) attach-agent $tcp
	$ftp($priority) set type_ FTP
	# set running_flows($priority) 1
	$ftp($priority) send $size;
}


proc generateFlows {flowsLeft priority} {
	global ns arrival_ chunkSize logging fileSize_ servers n0 N numFlows k startTimes\
	 randServer randServer2 simulation_time primary_server_distribution file_size_distribution\
	 flowID_to_server_map


	set now [$ns now]	
	#adding some extra time do let all the flows complete
	if {($flowsLeft >= 1) && ($now< [expr $simulation_time/3])} {
		# set primaryServerId -1
		array set serversUsed {}

		#file_size_distribution
		set fileSizeToSend [format {%0.0f} [$fileSize_ value]]

		# set now [$ns now]

		for {set i 0} {$i < $k} {incr i} {
		
			set uniqueServerNotFound 1
			set curr_priority [expr $i*$numFlows+$priority]
			while {$uniqueServerNotFound} {
			
				if {$i==0} {
					#primary flow
					set serverId $primary_server_distribution([expr $curr_priority-1])
					# set serverId [expr round([$randServer value])]
				} else {
					# #duplicate flow should not collide with the primary server
					set serverId [expr {int(rand()*$N) + 0}]
					# set serverId [expr round([$randServer2 value])]

				}
				set uniqueServerNotFound 0
				for {set j 0} {$j < [array size serversUsed]} {incr j} {
					if {$serversUsed($j)==$serverId} {
						set uniqueServerNotFound 1
						break
					}
				}
 				
				if {$uniqueServerNotFound==0} {
					set serversUsed($i) $serverId	
				}
			}



			if {$file_size_distribution == "pareto"} {
				$ns at $now "generateFlow $servers($serverId) $n0 $fileSizeToSend $curr_priority"
							
			} elseif {$file_size_distribution == "deterministic"} {
				$ns at $now "generateFlow $servers($serverId) $n0 $chunkSize $curr_priority"
			}
			if ($logging) {
				append startTimes $now " " [expr $curr_priority] " " [expr $serverId+1] "\n"
			}
            #add to flow id to server map, used for purging
            set flowID_to_server_map($curr_priority) $serverId
		}

		#update arguments
		set priority [expr $priority+1]
		set flowsLeft [expr $flowsLeft-1]

		set nextArrival [expr $now+[$arrival_ value]]
		# set nextArrival [expr $now+$arrivalTimes([expr $numFlows-$flowsLeft-1])]
		#call the function again after time
		$ns at $nextArrival "generateFlows $flowsLeft $priority"
		# $ns at [expr $now+$meanInterArrivalTime] "generateFlow $src $dst $flowsLeft $priority"

	}

}



#topology
#
#	    n0
#	   /| \
#	  / |  \
#	 /  |	\
#	n1 n2...nN



#create sink
set n0 [$ns node]

array set servers {}
array set linksA {}
array set linksB {}
array set down_links {}
array set up_links {}
#Create N servers
for {set i 0} {$i <$N} {incr i} {
	set servers($i) [$ns node]
	# set linksA($i) [$ns simplex-link $n0 $servers($i) $linkBW 0.00ms CBQ]
	# set linksB($i) [$ns simplex-link $servers($i) $n0 $linkBW 0.00ms CBQ]
	$ns simplex-link $n0 $servers($i) $linkBW 0.025ms CBQ
	$ns simplex-link $servers($i) $n0 $linkBW 0.025ms CBQ
	$ns queue-limit $n0 $servers($i) $queue_limit
	$ns queue-limit $servers($i) $n0 $queue_limit
	$ns makeCBQlink $n0 $servers($i) 1
	$ns makeCBQlink $servers($i) $n0 1
    set down_links($i) [$ns makeCBQlink $n0 $servers($i) 1]
    set up_links($i) [$ns makeCBQlink $servers($i) $n0 1]
}

proc generateFailure { } {
	global ns n0 servers rtmodel fct_ideal N failureTrace logging simulation_time
	set serverIdToFail [expr {int(rand()*$N)}]
	#TODO: check if server is not already failed
	set now [$ns now]
	$ns rtmodel-at $now down $servers($serverIdToFail) $n0
	$ns rtmodel-at $now down $n0 $servers($serverIdToFail)
	# puts $ns $n0 up?
	# $ns rtmodel-at $now down $n1 $n2
	# set recoverAt [expr $now+[expr 200.0*$fct_ideal]]
	set recoverAt [expr $now+[expr $simulation_time/3.00]]
	$ns at $recoverAt "recoverFailure $serverIdToFail"
	if ($logging) {
		append failureTrace "server: $serverIdToFail, failed at: $now\n"
	}

}


proc recoverFailure { serverIdToRecover } {
	global ns n0 servers rtmodel fct_ideal failureTrace logging
	set now [$ns now]
	$ns rtmodel-at $now up $servers($serverIdToRecover) $n0
	$ns rtmodel-at $now up $n0 $servers($serverIdToRecover)
	set failAt [expr $now+[expr 100.0*$fct_ideal]]
	$ns at $failAt "generateFailure"
	if ($logging) {
		append failureTrace "server: $serverIdToRecover, recovered at: $now\n"
	}
}

#calculate inter arrvial time
set BW [expr [string range $linkBW 0 [string length $linkBW]-3]*1000000.0]
# puts $BW
set size [expr $chunkSize*8.0]
set loadFactor [expr 100.0/$percentageLoad]
set meanInterArrivalTime [expr $size*$loadFactor/$BW]
#for N servers
set meanInterArrivalTime [expr $meanInterArrivalTime/$N]

#ideal fct without load
set fct_ideal [expr $size/$BW]

$defaultRNG seed $seed_value
#arrival distribution
set arrivalRNG [new RNG]
set arrival_ [new RandomVariable/Exponential]
$arrival_ set avg_ $meanInterArrivalTime
$arrival_ use-rng $arrivalRNG

#file size distribution
set fileSizeRng [new RNG]
set fileSize_ [new RandomVariable/Pareto]
$fileSize_ set avg_ $chunkSize
#shape from conext 13
$fileSize_ set shape_ 2.1
$fileSize_ use-rng $fileSizeRng

# prepopulate primary server distribution
array set primary_server_distribution {}
for {set i 0} {$i < $numFlows} {incr i} {
	set primary_server_distribution($i) [expr {int(rand()*$N)}];
}
# set serverRNG [new RNG]
# set randServer [new RandomVariable/Uniform]
# $randServer set min_ 0
# $randServer set max_ [expr $N-1]
# $randServer use-rng $serverRNG

# #secondary server selection distribution
# set server2RNG [new RNG]
# set randServer2 [new RandomVariable/Uniform]
# $randServer2 set min_ 0
# $randServer2 set max_ [expr $N-1]
# $randServer2 use-rng $server2RNG


$ns at 4.0 "generateFlows $numFlows 1"

if {$failures == 1} {
	#failures
	puts "generating failures"

	# $linksA(0) down
	# $linksB(0) down
	# $ns rtmodel-at 0.1 down $n0 $servers(5)
	# $ns rtmodel-at 4.1 down $n0 $servers(1)
	# $ns rtmodel-at 4.1 down $n0 $servers(2)
	# $ns rtmodel-at 4.1 down $n0 $servers(3)
	# $ns rtmodel-at 4.1 down $n0 $servers(4)
	# $ns rtmodel-at 4.1 down $n0 $servers(5)
	# $ns rtmodel-at 4.1 down $n0 $servers(6)
	# $ns rtmodel-at 4.1 down $n0 $servers(7)
	# $ns rtmodel-at 4.1 down $n0 $servers(8)

	# $ns rtmodel-at 0.2 up $n0 $servers(5)
	# $ns rtmodel-at 4.5 up $n0 $servers(1)
	# $ns rtmodel-at 4.5 up $n0 $servers(2)
	# $ns rtmodel-at 4.5 up $n0 $servers(3)
	# $ns rtmodel-at 4.5 up $n0 $servers(4)
	# $ns rtmodel-at 4.5 up $n0 $servers(5)
	# $ns rtmodel-at 4.5 up $n0 $servers(6)
	# $ns rtmodel-at 4.5 up $n0 $servers(7)
	# $ns rtmodel-at 4.5 up $n0 $servers(8)
	
	#first failure
	# for {set i 0} {$i < $number_of_failures} {incr i} {
	# 	$ns at [expr 4.0+[expr $fct_ideal*100.0]] generateFailure
	# }

	# set uRNG [new RNG]
	# set u [new RandomVariable/Uniform]
	# $u set min_ 0.2
	# $u set max_ 1
	# $u use-rng $uRNG
	# set rRNG [new RNG]
	# set r [new RandomVariable/Uniform]
	# $r set min_ 0.2
	# $r set max_ 1
	# $r use-rng $rRNG
	# set failAt 4

	# for {set j 0} {$j <2000} {incr j} {
	# 	# puts $failAt
	# 	$ns rtmodel-at $failAt down $n1 $n2
	# 	set recoverAt [expr $failAt+[format "%-8.3f" [$r value]]]
	# 	$ns rtmodel-at $recoverAt up $n1 $n2
	# 	set failAt [expr $recoverAt+[format "%-8.3f" [$u value]]]
	# }
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
	global ns logging endTimes purging cancellation
	set flowID [$self set fid_];
	# puts "FlowID: $flowID completed"
	if ($logging) {
		set now [$ns now]
		set thisNode [$self set node_]
		append endTimes $now " " $flowID " " [$thisNode id] "\n"
	}
	# purging turns on cancellation by default
	if {$cancellation || $purging} {
		stopRedundantFlows $flowID
	}
}

proc stopRedundantFlows { flowID } {
	global numFlows k ftp purging
	set baseID [expr $flowID%$numFlows]
	if {$baseID==0} {
		set baseID $numFlows		
	}

	for {set i 0} {$i < $k} {incr i} {
		set id [expr $baseID+[expr $i*$numFlows]]
		if {[info exists ftp($id)]} {
			if {$purging} {
				purge $id
				$ftp($id) terminate
			} else {
				$ftp($id) stop	
			}
			
		}
	}
}

# this functions gets the queue mapping of flows and then
# calls the appropriate purge-packets-of-fid on those queues
proc purge { flowID } \
{
    global down_links up_links flowID_to_server_map
    $down_links($flowID_to_server_map($flowID)) purge-packets-of-fid $flowID
    $up_links($flowID_to_server_map($flowID)) purge-packets-of-fid $flowID
    #TODO: this flowID_to_server_map will not work with more elaborate topologies, implement it some other efficient way
}


proc print_curr_time {} {
        global ns simulation_time
        set now [$ns now]
        puts "Current Time: $now"
        $ns at [expr $now+[expr $simulation_time/100.0]] "print_curr_time"
}


proc aggregate_bytes_by_fid { flowID } {
	global numFlows k sink
	set baseID [expr $flowID%$numFlows]
	if {$baseID==0} {
		set baseID $numFlows
	}
	set total_bytes 0
	for {set i 0} {$i < $k} {incr i} {
		set id [expr $baseID+[expr $i*$numFlows]]
		if {[info exists sink($id)]} {
			set total_bytes [expr $total_bytes + [$sink($id) set bytes_]]
		}
	}
	return total_bytes
}


set pkt_sz [Agent/TCP set packetSize_]
set rtt_ideal [expr (2.0*$pkt_sz)/$BW]

proc check_aggregate_bytes {} {
	global ns numFlows chunkSize rtt_ideal
	for {set i 0} {$i < $numFlows} {incr i} {
		set flowID [expr $i+1]
		if { [aggregate_bytes_by_fid $flowID] > $chunkSize } {
			stopRedundantFlows $flowID
		}
	}
	set now [$ns now]

	$ns at [expr $now+($rtt_ideal*4)] "check_aggregate_bytes"
}

proc calculate_simultaion_time {} {
	global N fct_ideal numFlows
	#4+ to add start buffer
	#3x to add end buffer
	return [expr (($fct_ideal*$numFlows/$N)+4)*3] 
}
set simulation_time [calculate_simultaion_time]
puts "simulation_time: $simulation_time"

print_curr_time
# check_aggregate_bytes

#Call the finish procedure after 5 seconds of simulation time

$ns at $simulation_time "finish"

#Run the simulation

$ns run
