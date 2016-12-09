#!/bin/bash

# RavidCFD-dev
source $HOME/RavidCFD/RavidCFD-dev/etc/bashrc

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

cd ${PBS_O_WORKDIR}

# Get application name
application=$(getApplication)

# devices list
MPI=$(wc -l < $PBS_NODEFILE)
devices="'("
i=0
startdevice=0
device=$startdevice
while [ "$i" -lt "$MPI" ]
do
    devices="$devices $device"
    i=$(expr $i + 1)
    device=$(expr $device + 1)
    if [ "$device" -gt 2 ];then
	device=$startdevice
    fi
done
devices="$devices )'"

echo "devices=$devices"

(
cat <<EOF
#!/bin/bash

source $HOME/RavidCFD/RavidCFD-dev/etc/bashrc

export OMPI_MCA_orte_tmpdir_base=/scr/$PBS_JOBID/$OMPI_COMM_WORLD_RANK

$application -parallel -devices $devices

rm -rf $OMPI_MCA_orte_tmpdir_base
EOF
) > application.sh

chmod +x application.sh

(
    command="which mpirun"
    echo $command
    echo "---"
    $command
    echo "---"
    echo

    command="df"
    echo $command
    echo "---"
    $command
    echo "---"
    echo

    command="env"
    echo $command
    echo "---"
    $command
    echo "---"
    echo

    nProcs=`wc -l < $PBS_NODEFILE`

    if [ $nProcs -eq 1 ];then
	$application
    else
	mpirun \
	    --bind-to core -mca btl openib,sm,self \
	    -n $nProcs -hostfile $PBS_NODEFILE ./application.sh
    fi
) >& log.$PBS_JOBID
