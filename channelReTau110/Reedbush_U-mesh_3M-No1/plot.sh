#!/bin/sh
csv=all.csv
for batchFileNameOption in \
    '-b OF41_Icc_INTELMPI' \
    ''
do
    for yscaleLinearOption in '' '-y'
    do
	../bin/plot.py \
	    $csv \
	    $yscaleLinearOption \
	    $batchFileNameOption
    done
done
