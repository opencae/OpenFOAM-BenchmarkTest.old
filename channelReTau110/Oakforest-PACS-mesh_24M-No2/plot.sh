#!/bin/bash

for ppn in 64 128 256
do
    batchFileName="\
v1612+_system_Icc_INTELMPI_${ppn}_flat_3 \
v1612+_system_IccKNL_INTELMPI_${ppn}_flat_3 \
v1612+_system_Icc_INTELMPI_${ppn}_cache_0 \
v1612+_system_IccKNL_INTELMPI_${ppn}_cache_0 \
"
    ../bin/plot.py all.csv -b $batchFileName
    ../bin/plot.py all.csv -y -b $batchFileName
    mkdir ppn-${ppn}
    mv *.pdf ppn-${ppn}
done
