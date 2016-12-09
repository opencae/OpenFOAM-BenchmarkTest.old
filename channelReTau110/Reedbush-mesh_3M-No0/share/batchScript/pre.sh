#!/bin/sh

WM_COMPILER=Gcc48
WM_MPLIB=SYSTEMOPENMPI

. /etc/profile.d/modules.sh
module purge
module load openmpi/1.8.3/gnu
source ${HOME/\/home/\/lustre}/OpenFOAM/OpenFOAM-2.3.0/etc/bashrc \
    WM_COMPILER=$WM_COMPILER \
    WM_MPLIB=$WM_MPLIB

export MPI_BUFFER_SIZE=20000000

cd $PBS_O_WORKDIR

log=log.$PBS_JOBID
(
    env

    blockMesh
) >& $log
