#!/bin/sh
csv=all.csv
for yscaleLinearOption in '' '-y'
do
    ../bin/plot.py \
	$batchFileNameOption \
	$yscaleLinearOption \
	$csv
done
