#!/bin/sh

BASE=`pwd`

for i in `cat projects.txt` ; do

	echo $i
	cd "$BASE/$i"
	"$@"
	echo

done
