#!/bin/bash

batchFileName="\
v1612+_ThirdParty_GccKNL_INTELMPI_64_cache_0 \
v1612+_ThirdParty_Gcc_INTELMPI_64_cache_0 \
v1612+_ThirdParty_IccKNL_INTELMPI_64_cache_0 \
v1612+_ThirdParty_Icc_INTELMPI_64_cache_0 \
"

../bin/plot.py all.csv -b $batchFileName
../bin/plot.py all.csv -y -b $batchFileName
