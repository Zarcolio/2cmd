#!/bin/bash

scriptname="2cmd.py"

pip3 install -r requirements.txt

dir=$(pwd)

2ulb 2&>/dev/null
	if [ $? -eq 127 ]
	then	
		while true; do
			read -p "2ulb not found, install 2ulb? [y/n]: " yn
			case $yn in
			    [Yy]*) cd .. ; git clone https://github.com/Zarcolio/2ulb ; sudo python3 2ulb/2ulb.py 2ulb/2ulb.py ; cd $dir ; sudo 2ulb $scriptname; exit 0 ;;  
			    [Nn]*) echo "Aborted" ; exit 1 ;;
			esac
		done
	else
		sudo 2ulb $scriptname
	fi
