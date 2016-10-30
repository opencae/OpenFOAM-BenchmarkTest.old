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
module load openfoam/3.0.1

application=pre.sh

(
    env
    blockMesh
    rbstat -s ${PBS_JOBID}    
) >& log.${application}.${PBS_JOBID}

touch ${application}.done
