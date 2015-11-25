#!/bin/sh

usage() {
    cat<<USAGE

Usage: ${0##*/} [OPTION]
options:
  -r | -remove      remove fail log
  -h | -help        print the usage
USAGE
    exit 1
}

# MAIN SCRIPT
#~~~~~~~~~~~~
unset removeOpt

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
   -*)
      usage "invalid option '$1'"
      ;;
   *)
      break
      ;;
   esac
done

for d in n_*/mpi_*/simulation*
do
    (cd $d
	for l in log.[0-9]*[0-9]
	do
	    grep "^End" $l >& /dev/null
	    if [ $? -eq 1 ];then
		echo "$d/$l"
		if [  "$removeOpt" = true ];then
		    echo rm -f $l
		    rm -f $l
		fi
	    fi
	done
    )
done

