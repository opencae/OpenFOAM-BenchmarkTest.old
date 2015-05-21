#!/bin/bash

# Source  functions
. ../bin/tools/Functions

tablefile="table.csv"
outputfile=$PWD/$tablefile

line=$(commonHeader)
line="$line,Steps,ExectutionTime0(s),ExectutionTime1(s),ExectutionTime/Steps(s)"
echo $line > $outputfile

for Dir in n_*/mpi_*/simulationType_*
do
    echo "Dir= $Dir"
    (cd $Dir
	n=0
	for log in log.*[0-9]
	do
	    echo "  log= $log"
	    grep "^End" $log >& /dev/null 
	    [ "$?" -ne 0 ] && continue
	    line="$Dir,$log,$(parseCaseSettings),$(parseLog $log)"

	    ExecutionTime=`awk 'BEGIN {n=0} \
		/^ExecutionTime/ {t=$3;if (n==0) t0=t;n++} \
		END {printf "%d,%g,%g,%g",n,t0,t,(t-t0)/(n-1)}' \
		$log`
	    line="$line,$ExecutionTime"

	    echo $line >> $outputfile
	done
    )
done
