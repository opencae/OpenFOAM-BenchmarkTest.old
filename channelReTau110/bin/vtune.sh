#!/bin/bash

for Dir in n_*/mpi_*/simulationType_*
do
    echo "Dir= $Dir"
    (cd $Dir
	for log in log.*[0-9]
	do
	    echo "  log= $log"

	    vtunedir=$log.vtune
	    vtunelog=$vtunedir.txt
	    if [ -d $vtunedir -a ! -f $vtunelog ];then
		amplxe-cl -R hotspots -r $vtunedir -q > $vtunelog
		if [ $? -ne 0 ];then
		    rm -f $vtunelog
		fi
	    fi
	    exit
	done
    )
done
