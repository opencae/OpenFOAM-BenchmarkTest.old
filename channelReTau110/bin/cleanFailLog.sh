#!/bin/bash

usage() {
    cat<<USAGE

Usage: ${0##*/} [OPTION]
options:
  -m | -move        move fail log to log.fail directory
  -r | -remove      remove fail log
  -h | -help        print the usage
USAGE
    exit 1
}

# MAIN SCRIPT
#~~~~~~~~~~~~
unset removeOpt
unset moveOpt

# parse options
while [ "$#" -gt 0 ]
do
   case "$1" in
   -h | -help)
      usage
      ;;
   -r | -remove)
      removeOpt=true
      shift
      ;;
   -m | -move)
      moveOpt=true
      shift
      ;;
   -*)
      usage "invalid option '$1'"
      ;;
   *)
      break
      ;;
   esac
done

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
logFailDir=log.fail

application=`sed -ne 's/^ *application\s*\([a-zA-Z]*\)\s*;.*$/\1/p' cases/system/controlDict`

for decomposeParDict in ${decomposeParDictArray[@]}
do
    for fvSolution in ${fvSolutionArray[@]}
    do
	for solveBatch in ${solveBatchArray[@]}
	do
	    Dir=$caseDir/$decomposeParDict/$fvSolution/$solveBatch
	    n=1
	    for log in $Dir/log.${application}.*[0-9]
	    do
		[ "${log##*/}" == "log.pimpleFoam.*[0-9]" ] && continue
		[ -f $log ] || continue

		grep "^End" $log >& /dev/null
		if [ $? -eq 1 ];then
		    echo "$log:"
		    tail -n 50 $log
		    
		    if [  "$moveOpt" = true ];then
			base=`basename $log`
			dir=`dirname $log`
			(cd $dir
			    [ ! -d $logFailDir ] && mkdir $logFailDir
			    mv $base $logFailDir/
			    [ -f $base.done ] && mv $base.done $logFailDir/ 
			)
		    elif [  "$removeOpt" = true ];then
			rm -f $log $log.done
		    fi
		fi
	    done
	done
    done
done
