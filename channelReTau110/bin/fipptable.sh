#!/bin/bash

# Source  functions
. ../bin/tools/Functions

tablefile="fipptable.csv"
outputfile=$PWD/$tablefile

line="$(commonHeader)" 
line="$line,Steps,ExectutionTime0(s),ExectutionTime1(s),ExectutionTime/Steps(s)"
line="$line,Elapsed(s),User(s),System(s)"
line="$line,MFLOPS,MFLOPS/PEAK(%),MIPS,MIPS/PEAK(%)"
line="$line,Mem throughput_chip(MB/S),Mem throughput/PEAK(%),SIMD(%)"

echo $line > $outputfile

for Dir in n_*/mpi_*/simulationType_*;do
    echo "Dir= $Dir"
    (cd $Dir
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

	    fippDir=$log.fippdir
	    fippFile=$fippDir.txt

	    if [ -d $fippDir -a ! -f $fippFile ];then
		echo "Convert profile data into text file: $fippFile" >&2
		fipppx -A -Ihwm,call -d $fippDir > $fippFile
		if [ $? -ne 0 ];then
		    rm -f $fippFile
		fi
	    fi

	    if [ -f $fippFile ];then
   	        profile=`awk 'BEGIN {n=0} \
		    /Application$/ { \
		    if (n==0) {printf "%g,%g,%g,",$1,$2,$3} \
		    else if (n==1) {printf "%g,%g,%g,%g,",$2,$3,$4,$5} \
		    else {printf "%g,%g,%g",$2,$3,$4};n++}' $fippFile`
		
		line="$line,$profile"
	    fi

	    echo $line >> $outputfile
	done
    )
done


