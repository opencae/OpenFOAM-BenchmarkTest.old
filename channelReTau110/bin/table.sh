#!/bin/bash

# Source  functions
. ../bin/tools/Functions

tablefile="table.csv"
outputfile=$PWD/$tablefile

line=$(commonHeader)
line="$line,CoMean,CoMax"
line="$line,UxInitRes,UxFinalRes,UxNoIter"
line="$line,UyInitRes,UyFinalRes,UyNoIter"
line="$line,UzInitRes,UzFinalRes,UzNoIter"
line="$line,p0InitRes,p0FinalRes,p0NoIter"
line="$line,p1InitRes,p1FinalRes,p1NoIter"
line="$line,contErrSumLocal0,contErrGlobal0,contErrCum0"
line="$line,contErrSumLocal1,contErrGlobal1,contErrCum1"
line="$line,Steps,ExectutionTime0(s),ExectutionTime1(s),ExectutionTime/Steps(s)"
echo $line > $outputfile

for Dir in n_*/mpi_*/simulationType_*
do
    echo "Dir= $Dir"
    (cd $Dir
	n=1
	for log in log.*[0-9]
	do
	    echo "  log= $log"
	    grep "^End" $log >& /dev/null 
	    [ "$?" -ne 0 ] && continue
	    line="$Dir,$log,$(parseCaseSettings),$(parseLog $log)"

	    Co=`grep "^Courant Number" $log | tail -n 1 | cut -d ' ' -f 4,6 | tr ' ' ','`
	    Ux=`grep "Solving for Ux," $log | tail -n 1 | cut -d ' ' -f 9,13,16 | tr -d ' '`
	    Uy=`grep "Solving for Uy," $log | tail -n 1 | cut -d ' ' -f 9,13,16 | tr -d ' '`
	    Uz=`grep "Solving for Uz," $log | tail -n 1 | cut -d ' ' -f 9,13,16 | tr -d ' '`
	    p0=`grep "Solving for p," $log | tail -n 2 | head -n 1 | cut -d ' ' -f 9,13,16 | tr -d ' '`
	    p1=`grep "Solving for p," $log | tail -n 1 | cut -d ' ' -f 9,13,16 | tr -d ' '`
	    err0=`grep "^time step continuity errors" $log | tail -n 2 | head -n 1 | cut -d ' ' -f 9,12,15  | tr -d ' '`
	    err1=`grep "^time step continuity errors" $log | tail -n 1 | cut -d ' ' -f 9,12,15  | tr -d ' '`
	    line="$line,$Co,$Ux,$Uy,$Uz,$p0,$p1,$err0,$err1"

	    ExecutionTime=`awk 'BEGIN {n=0} \
		/^ExecutionTime/ {t=$3;if (n==0) t0=t;n++} \
		END {printf "%d,%g,%g,%g",n,t0,t,(t-t0)/(n-1)}' \
		$log`
	    line="$line,$ExecutionTime"

	    echo $line >> $outputfile

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
            }' $log > log.pimpleFoam.$$.${n}th

	    n=`expr $n + 1`
	done
    )
done

tar jcf caseSettings-log-$$.tar.bz2 n_*/mpi_*/simulationType_*/{0,constant/*Properties,system,caseSettings,log.pimpleFoam.$$.*th}
rm -f n_*/mpi_*/simulationType_*/log.pimpleFoam.$$.*th

