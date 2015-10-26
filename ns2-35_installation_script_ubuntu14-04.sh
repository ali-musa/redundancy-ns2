#!/bin/sh -e
sudo apt-get update
# sudo apt-get -y dist-upgrade
# sudo apt-get -y update
sudo apt-get -y install build-essential autoconf automake
sudo apt-get -y install tcl8.5-dev tk8.5-dev
sudo apt-get -y install perl xgraph libxt-dev libx11-dev libxmu-dev
sudo apt-get -y install gcc-4.4
cd ~/
wget http://downloads.sourceforge.net/project/nsnam/allinone/ns-allinone-2.35/ns-allinone-2.35.tar.gz
tar -xzf ns-allinone-2.35.tar.gz
sudo apt-get -y install libc6-dev g++ gcc
sudo apt-get -y install xorg-dev
sudo apt-get -y install gnuplot
cd ~/ns-allinone-2.35

sed -i '137s/.*/	void eraseAll() { this->erase(baseMap::begin(), baseMap::end()); }/' ~/ns-allinone-2.35/ns-2.35/linkstate/ls.h

./install

export PATH=$PATH:~/ns-allinone-2.35/bin:~/ns-allinone-2.35/tcl8.5.10/unix/:~/ns-allinone-2.35/tk8.5.10/unix/
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/ns-allinone-2.35/otcl-1.14/:~/ns-allinone-2.35/lib
export TCL_LIBRARY=~/ns-allinone-2.35/tcl8.5.10/library/:~/ns-allinone-2.35/tk8.5.10/library/
export NS=~/ns-allinone-2.35/ns-2.35
export NSVER=2.35
ln -s ~/ns-allinone-2.35/bin/ns ns
cd ~/ns-allinone-2.35/tcl8.5.10/library/
wget https://github.com/downloads/tDOM/tdom/tDOM-0.8.3.tgz
tar -xvzf tDOM-0.8.3.tgz
cd tDOM-0.8.3/
./configure
make 
make test
make install
cd ~
