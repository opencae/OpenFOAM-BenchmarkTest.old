#!/bin/bash

if [ "$#" -ne 1 ];then
        cat<<USAGE
Usage: ${0##*/} configuration
USAGE
    exit 1
fi

# Source configuration file
configuration=$1
if [ ! -f $configuration ]
then
    echo "Error: $configuration does not exist."
    exit 1
fi
. $configuration

caseDir=cases
csvFile=$configuration.csv

application=`sed -ne 's/^ *application[ \t]*\([a-zA-Z]*\)[ \t]*;.*$/\1/p' cases/system/controlDict`

logs=""

line="#decomposeParDict,method,fvSolution,solveBatch"
line="$line,Build,Date,Time,nNodes,nProcs"
line="$line,Steps"
line="$line,ClockTimeFirstStep,ClockTimeNextToLastStep,ClockTimeLastStep"
line="$line,ExecutionTimeFirstStep,ExecutionTimeNextToLastStep,ExecutionTimeLastStep"
line="$line,ClockTimePerStepWOLastStep,ClockTimePerStep"
line="$line,ExecutionTimePerStepWOLastStep,ExecutionTimePerStep"

echo $line > $csvFile

for decomposeParDict in `echo ${decomposeParDictArray[@]} | tr ' ' '\n' | sort | tr '\n' ' '`
do
    for fvSolution in `echo ${fvSolutionArray[@]} | tr ' ' '\n' | sort | tr '\n' ' '`
    do
	for solveBatch in `echo ${solveBatchArray[@]} | tr ' ' '\n' | sort | tr '\n' ' '`
	do
	    Dir=$caseDir/$decomposeParDict/$fvSolution/$solveBatch
	    echo "Dir= $Dir"
	    n=1
	    for log in $Dir/log.${application}.*[0-9]
	    do
		echo "log= $log"
		grep "^End" $log >& /dev/null 
		[ "$?" -ne 0 ] && continue
		
		method=`grep '^ *method ' $Dir/system/decomposeParDict | sed "s/.*[ \t]\([^ \t]*\)[ \t]*;.*/\1/"`
		Build=`grep '^Build  *:' $log | sed "s/.*: \(.*\)$/\1/"`
		Date=`grep '^Date  *:' $log | sed "s/.*: \(.*\)$/\1/"`
		Time=`grep '^Time  *:'  $log | sed "s/.*: \(.*\)$/\1/"`
		nProcs=`grep '^nProcs  *:' $log | sed "s/.*: \(.*\)$/\1/"`
		nNodes=`grep "^\"" $log | sed -e "s/^\"//" -e "s/\.[^\.]*$//" | uniq | wc -l`
		
		ExecutionTime=`awk 'BEGIN {n=0;t=0;c=0} \
		/^ExecutionTime/ {told=t;t=$3;cold=c;c=$7;n++;if (n==1) {t1=t;c1=c}} \
		END {printf "%d,%g,%g,%g,%g,%g,%g,%g,%g,%g,%g"\
                ,n\
                ,c1,cold,c\
                ,t1,told,t\
                ,(cold-c1)/(n-2),(c-c1)/(n-1)\
                ,(told-t1)/(n-2),(t-t1)/(n-1)\
                }' \
		$log`
		    
		line="$decomposeParDict,$method,$fvSolution,$solveBatch"
		line="$line,$Build,$Date,$Time,$nNodes,$nProcs"
		line="$line,$ExecutionTime"
		echo $line >> $csvFile
		
		newlog=$Dir/log.${application}.${n}th
		awk -F ' ' 'BEGIN {n=0} \
            {\
               if ($1=="Build") n=1;\
               if (n==1) {\
                 if ($1=="Host")\
                   { print "Host   :"}\
                 else if ($1=="Case")\
                   { print "Case   :"}\
                 else if ($1 ~ /["]/)\
                   { print "\"\"" }\
                 else { print $0} };\
               if ($1=="End") {n=0}\
            }' $log > $newlog

		logs="$logs $newlog"

		n=`expr $n + 1`
	    done
	done
    done
done

tar jcf $configuration.tar.bz2 $logs
rm -f $logs
