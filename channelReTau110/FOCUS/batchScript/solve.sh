#!/bin/bash
#SBATCH -p debug6m
#SBATCH -J OFGcc
#SBATCH -e OFGcc.e%J
#SBATCH -o OFGcc.o%J

# Path
OpenFOAM_PATH=/home1/share/openfoam/2.3.0/gnu/openmpi/OpenFOAM-2.3.0
VTUNE_PATH=/home1/share/opt/intel/vtune_amplifier_xe/bin64
MPI_PATH=/home1/share/openmpi/1.6.5/gnu/bin

# Intel Licence server
export INTEL_LICENSE_FILE=/home1/share/opt/intel/flexlm

module load gnu/openmpi165
unset FOAM_INST_DIR
source $OpenFOAM_PATH/etc/bashrc

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

env > log.env

log=log.$SLURM_JOB_ID
(
if [ -x $VTUNE_PATH/amplxe-cl ];then

    vtunedir=$log.vtune
    mkdir $vtunedir
    $VTUNE_PATH/amplxe-cl -q -r $vtunedir -c hotspots -- \
	$MPI_PATH/mpirun -np $(getNumberOfProcessors)  $(getApplication) -parallel
else
    	$MPI_PATH/mpirun -np $(getNumberOfProcessors)  $(getApplication) -parallel
fi
) >& $log
