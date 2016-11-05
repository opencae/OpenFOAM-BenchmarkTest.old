#!/bin/bash

if [ -z "${PBS_JOBID+x}" ] ; then
    PBS_JOBID=$1
else
    cd $PBS_O_WORKDIR
fi

export MPI_BUFFER_SIZE=20000000

. /etc/profile.d/modules.sh
module purge
module load pbsutils
module load intel/16.0.3.210
module load intel-mpi/5.1.3.210
export MPI_ROOT=$I_MPI_ROOT
source ${HOME/\/home/\/lustre}/OpenFOAM/OpenFOAM-4.1/etc/bashrc \
WM_COMPILER=Icc \
WM_COMPILE_OPTION=Opt \
WM_MPLIB=INTELMPI \
WM_LABEL_SIZE=32

application=decomposePar.sh

log=log.${application}.${PBS_JOBID}
(
    env
    decomposePar -cellDist
    rbstat -s ${PBS_JOBID}    
) >& $log 

grep "^End" $log >& /dev/null
[ $? -eq 0 ] && touch ${application}.done
