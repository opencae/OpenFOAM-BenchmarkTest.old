#!/bin/sh
# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

for file in plot/*.gp
do
    gnuplot $file
done

epsfiles="executionTime.eps flowRate.eps umean.eps urms.eps vrms.eps wrms.eps uv.eps"
convert -density 300 -resize 1200x1200 $epsfiles plot.pdf


