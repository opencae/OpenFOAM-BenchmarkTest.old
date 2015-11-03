#!/bin/sh
#PJM -L "rscgrp=lecture"
#PJM -L "node=1"
#PJM -j
#PJM -S
#PJM -g "gt00"

module load OpenFOAM/2.3.0
unset FOAM_INST_DIR
export USER=$PJM_O_LOGNAME
source $WM_PROJECT_DIR/etc/bashrc

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

env

blockMesh >& log.blockMesh

