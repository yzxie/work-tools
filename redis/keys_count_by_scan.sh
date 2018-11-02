#!/bin/bash

A=$0
B=${A##*/}
C=${B%.*}
running_file_name=$C
running_flag="run.$running_file_name"
REDIS_CLIENT='redis-cli -h 0.0.0.0 -p 6379 -x'

function process {
	echo $0
	index=-1
	count=0
	step=100000

	while ((index!=0))
	do
		if [ $index -le 0 ];then
			index=0
		fi
		echo "scan $index match $1 count $step" | $REDIS_CLIENT > $running_file_name.cache
		read index <<< `head -1 $running_file_name.cache`
		read inc <<< `cat $running_file_name.cache | wc -l`
		inc=$((inc - 1))
		if [ $? -ne 0 ];then
			break
		fi
		count=$((count + inc))
	done

	echo "$1 count:"$count
}

#

if [ $# -ne 1 ];then
	echo "$0 "
	exit 0
fi

#
if [ -f "$running_flag" ] ; then
	echo "is running..."
	exit 0
fi

#
touch $running_flag
#

echo "processing...."
echo $*
process $*

#
rm -rf $running_flag
#

echo "ok!"