#!/bin/bash

if [ "$PJM_ENVIRONMENT" = "INTERACT" ];then
    mpi=1
    MPLIB=OPENMPI
else
    if [ -z "${PJM_JOBID+x}" ] ; then
	PJM_JOBID=$1
	mpi=1
	MPLIB=OPENMPI
    else
	export HOME=/work/$(id -gn)/$(id -un)
	cd $PJM_O_WORKDIR
	mpi=${PJM_MPI_PROC}
	MPLIB=INTELMPI
    fi
fi

# OpenFOAM-v1612+, ThirdParty Gcc, INTELMPI 2017.1.132
module purge
module load gcc/4.8.5
module unload impi
#module load impi/2017.1.132
#export MPI_ROOT=$I_MPI_ROOT
export I_MPI_DEBUG=5
. ${HOME}/OpenFOAM/OpenFOAM-v1612+/etc/bashrc \
    WM_COMPILER_TYPE=ThirdParty \
    WM_COMPILER=Gcc \
    WM_MPLIB=$MPLIB \
    WM_LABEL_SIZE=32

# Application name
application=pre.sh

# Log file
log=log.${application}.${PJM_JOBID}
batchFileDone=${application}.done

env > $log 2>&1
blockMesh >> $log 2>&1
grep "^End" $log >& /dev/null && touch $batchFileDone

#------------------------------------------------------------------------------
