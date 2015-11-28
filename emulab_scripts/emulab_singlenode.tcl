set ns [new Simulator]
source tb_compat.tcl
set singlenode [$ns node]
tb-set-node-os $singlenode UBUNTU14-64-STD
tb-set-node-startcmd $singlenode "sh /users/alimusa/startup.sh"

$ns rtproto Static
$ns run