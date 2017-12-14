#!/bin/sh

../bin/plot.py all.csv --sph --loop --first
../bin/plot.py all.csv -y --pe --solution

base=`basename ${PWD}`
CONVERT=$(which convert 2> /dev/null)
if [ ! "x$CONVERT" = "x" ]
then
    $CONVERT -density 300 *.eps ${base}.pdf
else
    echo "convert not installed" >&2
fi
