# This is a simple ns script. Comments start with #.
set ns [new Simulator]
source tb_compat.tcl
set node1 [$ns node]
tb-set-node-os $node1 UBUNTU14-64-STD
tb-set-node-startcmd $node1 "sh /users/alimusa/startup.sh"
set node10 [$ns node]
tb-set-node-os $node10 UBUNTU14-64-STD
tb-set-node-startcmd $node10 "sh /users/alimusa/startup.sh"
set node20 [$ns node]
tb-set-node-os $node20 UBUNTU14-64-STD
tb-set-node-startcmd $node20 "sh /users/alimusa/startup.sh"
set node30 [$ns node]
tb-set-node-os $node30 UBUNTU14-64-STD
tb-set-node-startcmd $node30 "sh /users/alimusa/startup.sh"
set node40 [$ns node]
tb-set-node-os $node40 UBUNTU14-64-STD
tb-set-node-startcmd $node40 "sh /users/alimusa/startup.sh"
set node50 [$ns node]
tb-set-node-os $node50 UBUNTU14-64-STD
tb-set-node-startcmd $node50 "sh /users/alimusa/startup.sh"
set node60 [$ns node]
tb-set-node-os $node60 UBUNTU14-64-STD
tb-set-node-startcmd $node60 "sh /users/alimusa/startup.sh"
set node70 [$ns node]
tb-set-node-os $node70 UBUNTU14-64-STD
tb-set-node-startcmd $node70 "sh /users/alimusa/startup.sh"
set node80 [$ns node]
tb-set-node-os $node80 UBUNTU14-64-STD
tb-set-node-startcmd $node80 "sh /users/alimusa/startup.sh"
set node90 [$ns node]
tb-set-node-os $node90 UBUNTU14-64-STD
tb-set-node-startcmd $node90 "sh /users/alimusa/startup.sh"
set node95 [$ns node]
tb-set-node-os $node95 UBUNTU14-64-STD
tb-set-node-startcmd $node95 "sh /users/alimusa/startup.sh"
set nodespare [$ns node]
tb-set-node-os $nodespare UBUNTU14-64-STD
tb-set-node-startcmd $nodespare "sh /users/alimusa/startup.sh"


$ns rtproto Static
$ns run