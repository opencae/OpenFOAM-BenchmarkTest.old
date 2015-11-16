#!/bin/bash
#PBS -N openfoam
#PBS -o openfoam.log
#PBS -j oe 

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

cd $PBS_O_WORKDIR
env
blockMesh >& log.blockMesh
