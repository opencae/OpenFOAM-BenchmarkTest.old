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

application=`sed -ne 's/^ *application[ \t]*\([a-zA-Z]*\)[ \t]*;.*$/\1/p' cases/system/controlDict`

for decomposeParDict in `echo ${decomposeParDictArray[@]} | tr ' ' '\n' | sort | tr '\n' ' '`
do
    for fvSolution in `echo ${fvSolutionArray[@]} | tr ' ' '\n' | sort | tr '\n' ' '`
    do
	for solveBatch in `echo ${solveBatchArray[@]} | tr ' ' '\n' | sort | tr '\n' ' '`
	do
	    Dir=$caseDir/$decomposeParDict/$fvSolution/$solveBatch
	    echo "Dir= $Dir"
	    for log in $Dir/log.${application}.*[0-9]
	    do
		echo "log= $log"
		grep "^End" $log >& /dev/null 
		[ "$?" -ne 0 ] && continue

		Host=`grep '^Host   *:' $log | sed "s/.*: \"\(.*\)\"$/\1/"`

		vtunedir=$log.vtune.$Host
		vtunelog=$vtunedir.txt
		if [ -d $vtunedir -a ! -f $vtunelog ];then
		    amplxe-cl -R hotspots -r $vtunedir -q > $vtunelog
		    if [ $? -ne 0 ];then
			rm -f $vtunelog
		    fi
		fi
	    done
	done
    done
done
