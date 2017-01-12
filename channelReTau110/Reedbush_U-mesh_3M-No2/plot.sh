#!/bin/sh
csv=all.csv
for batchFileNameOption in \
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
