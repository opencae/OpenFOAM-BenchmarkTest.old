#!/bin/sh
csv=all.csv
for batchFileNameOption in \
    '-b OF230_Gcc_OpenMPI' \
    '-b OF230_Gcc_OpenMPI OF230_Icc_IntelMPI OF230_Icc14_IntelMPI513'
do
    for yscaleLinearOption in '' '-y'
    do
	../bin/plot.py \
	    $batchFileNameOption \
	    $yscaleLinearOption \
	    --ExecutionTimePerStep ExecutionTimePerStep \
	    --ClockTimePerStep ClockTimePerStep \
	    $csv
    done
done
