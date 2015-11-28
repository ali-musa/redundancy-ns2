#!/bin/sh -e
echo "checking for exp31"
echo "Checking exp for 1% load"
sshpass -p emulab2014 ssh -oStrictHostKeyChecking=no alimusa@node1.redundancy3.comp150.emulab.net 'bash -s' <<'ENDSSH'
if screen -ls | grep exp31 
then
echo "working for laod 1"
else
echo "NOT working for laod 1"
fi
sleep 3
ENDSSH
wait
echo "Checking exp for 10% load"
sshpass -p emulab2014 ssh -oStrictHostKeyChecking=no alimusa@node10.redundancy3.comp150.emulab.net 'bash -s' <<'ENDSSH'
if screen -ls | grep exp31 
then
echo "working for laod 10"
else
echo "NOT working for laod 10"
fi
sleep 3
ENDSSH
wait
echo "Checking exp for 20% load"
sshpass -p emulab2014 ssh -oStrictHostKeyChecking=no alimusa@node20.redundancy3.comp150.emulab.net 'bash -s' <<'ENDSSH'
if screen -ls | grep exp31 
then
echo "working for laod 20"
else
echo "NOT working for laod 20"
fi
sleep 3
ENDSSH
wait
echo "Checking exp for 30% load"
sshpass -p emulab2014 ssh -oStrictHostKeyChecking=no alimusa@node30.redundancy3.comp150.emulab.net 'bash -s' <<'ENDSSH'
if screen -ls | grep exp31 
then
echo "working for laod 30"
else
echo "NOT working for laod 30"
fi
sleep 3
ENDSSH
wait
echo "Checking exp for 40% load"
sshpass -p emulab2014 ssh -oStrictHostKeyChecking=no alimusa@node40.redundancy3.comp150.emulab.net 'bash -s' <<'ENDSSH'
if screen -ls | grep exp31 
then
echo "working for laod 40"
else
echo "NOT working for laod 40"
fi
sleep 3
ENDSSH
wait
echo "Checking exp for 50% load"
sshpass -p emulab2014 ssh -oStrictHostKeyChecking=no alimusa@node50.redundancy3.comp150.emulab.net 'bash -s' <<'ENDSSH'
if screen -ls | grep exp31 
then
echo "working for laod 50"
else
echo "NOT working for laod 50"
fi
sleep 3
ENDSSH
wait
echo "Checking exp for 60% load"
sshpass -p emulab2014 ssh -oStrictHostKeyChecking=no alimusa@node60.redundancy3.comp150.emulab.net 'bash -s' <<'ENDSSH'
if screen -ls | grep exp31 
then
echo "working for laod 60"
else
echo "NOT working for laod 60"
fi
sleep 3
ENDSSH
wait
echo "Checking exp for 70% load"
sshpass -p emulab2014 ssh -oStrictHostKeyChecking=no alimusa@node70.redundancy3.comp150.emulab.net 'bash -s' <<'ENDSSH'
if screen -ls | grep exp31 
then
echo "working for laod 70"
else
echo "NOT working for laod 70"
fi
sleep 3
ENDSSH
wait
echo "Checking exp for 80% load"
sshpass -p emulab2014 ssh -oStrictHostKeyChecking=no alimusa@node80.redundancy3.comp150.emulab.net 'bash -s' <<'ENDSSH'
if screen -ls | grep exp31 
then
echo "working for laod 80"
else
echo "NOT working for laod 80"
fi
sleep 3
ENDSSH
wait
echo "Checking exp for 90% load"
sshpass -p emulab2014 ssh -oStrictHostKeyChecking=no alimusa@node90.redundancy3.comp150.emulab.net 'bash -s' <<'ENDSSH'
if screen -ls | grep exp31 
then
echo "working for laod 90"
else
echo "NOT working for laod 90"
fi
sleep 3
ENDSSH
wait
echo "Checking exp for 95% load"
sshpass -p emulab2014 ssh -oStrictHostKeyChecking=no alimusa@node95.redundancy3.comp150.emulab.net 'bash -s' <<'ENDSSH'
if screen -ls | grep exp31 
then
echo "working for laod 95"
else
echo "NOT working for laod 95"
fi
sleep 3
ENDSSH
wait
