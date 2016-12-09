#!/bin/bash

module load gnu/openmpi165
unset FOAM_INST_DIR
source /home1/share/openfoam/2.3.0/gnu/openmpi/OpenFOAM-2.3.0/etc/bashrc

(
    env
    decomposePar 
) >& log.decomposePar.$SLURM_JOB_ID

touch decomposePar.sh.done
