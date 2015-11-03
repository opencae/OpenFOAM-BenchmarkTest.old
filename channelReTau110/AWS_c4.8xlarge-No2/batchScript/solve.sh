#!/bin/bash
#PBS -N openfoam
#PBS -o openfoam.log
#PBS -j oe 

# PATH
VTUNE_PATH=/apps/intel/xe2015/vtune_amplifier_xe/bin64

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions
export NCPUS=`cat $PBS_NODEFILE | wc -l`

cd $PBS_O_WORKDIR
env > log.env
(
if [ -x $VTUNE_PATH/amplxe-cl ];then

    vtunedir="log.vtune"
    mkdir $vtunedir
    mpirun -bind-to core -np ${NCPUS} -machinefile ${PBS_NODEFILE} \
        $VTUNE_PATH/amplxe-cl -q -r $vtunedir -c hotspots -- \
        $(getApplication) -parallel   
else
    mpirun -bind-to core -np ${NCPUS} -machinefile ${PBS_NODEFILE} \
        $(getApplication) -parallel 
fi
) >& log.$(getApplication).$$
