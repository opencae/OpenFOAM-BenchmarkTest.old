#!/bin/sh

module load gnu/openmpi165
unset FOAM_INST_DIR
source /home1/share/openfoam/2.3.0/gnu/openmpi/OpenFOAM-2.3.0/etc/bashrc

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

(
blockMesh
) >& log.pre.sh.$SLURM_JOB_ID

touch pre.sh.done

#------------------------------------------------------------------------------
