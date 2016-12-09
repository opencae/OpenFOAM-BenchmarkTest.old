#!/bin/sh
csv=all.csv
for batchFileNameOption in \
    '' \
    '-b OF230_Gcc_OpenMPI'
do
    for yscaleLinearOption in '' '-y'
    do
	../bin/plot.py \
	    $csv \
	    $yscaleLinearOption \
	    $batchFileNameOption
    done
done
