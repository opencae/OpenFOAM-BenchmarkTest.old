#!/bin/bash

if [ -z "${PBS_JOBID+x}" ] ; then
    PBS_JOBID=$1
else
    cd $PBS_O_WORKDIR
fi

unset WM_PROJECT_DIR
module unload intel intel-mpi mpt openfoam
module load intel/17.0.2.174
module load mpt/2.14
module load openfoam/1612-mpt
. $WM_PROJECT_DIR/etc/bashrc

application=decomposePar.sh

log=log.$application.$PBS_JOBID
(
    env
    decomposePar -cellDist 
    rbstat -s ${PBS_JOBID}
) >&  $log

grep "^End" $log >& /dev/null && touch $application.done

