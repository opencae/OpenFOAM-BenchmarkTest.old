#!/bin/bash

batchFileName="\
v1612+_ThirdParty_GccKNL_INTELMPI_1 \
v1612+_ThirdParty_Gcc_INTELMPI_1 \
v1612+_system_IccKNL_INTELMPI_1 \
v1612+_system_Icc_INTELMPI_1 \
"

../bin/plot.py all.csv -b $batchFileName
../bin/plot.py all.csv -y -b $batchFileName

