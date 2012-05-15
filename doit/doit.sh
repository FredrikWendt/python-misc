#!/usr/bin/env bash

BASE=`pwd`

for i in `cat projects.txt` ; do

	echo $i
	cd "$BASE"
	if [ -d "$i" ] ; then
		cd "$i"
		"$@"
		if [ $? -gt 0 ] ; then
			if [ "$1 $2" != "hg out" ] ; then
				echo "Aborting!"
				exit $? 
			fi
		fi
	else
		echo "Skipping - no such directory"
	fi
	echo

done

