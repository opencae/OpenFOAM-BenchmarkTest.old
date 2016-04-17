#!/bin/bash

# OF230Gcc
export PATH=/usr/apps.sp3/mpi/openmpi/1.6.5/g4.3.4/bin:$PATH
export LD_LIBRARY_PATH=/usr/apps.sp3/mpi/openmpi/1.6.5/g4.3.4/lib:$LD_LIBRARY_PATH
unset FOAM_INST_DIR
source $HOME/OpenFOAM/2.3.0/gnu/openmpi/OpenFOAM-2.3.0/etc/bashrc

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

cd ${PBS_O_WORKDIR}

# Get application name
application=$(getApplication)

(
cat <<EOF
#!/bin/bash

# OF230Gcc
export PATH=/usr/apps.sp3/mpi/openmpi/1.6.5/g4.3.4/bin:$PATH
export LD_LIBRARY_PATH=/usr/apps.sp3/mpi/openmpi/1.6.5/g4.3.4/lib:$LD_LIBRARY_PATH
unset FOAM_INST_DIR
source $HOME/OpenFOAM/2.3.0/gnu/openmpi/OpenFOAM-2.3.0/etc/bashrc

$application -parallel
EOF
) > application.sh

chmod +x application.sh

(
cat <<EOF
#!/bin/bash

# OF230Gcc
export PATH=/usr/apps.sp3/mpi/openmpi/1.6.5/g4.3.4/bin:$PATH
export LD_LIBRARY_PATH=/usr/apps.sp3/mpi/openmpi/1.6.5/g4.3.4/lib:$LD_LIBRARY_PATH
unset FOAM_INST_DIR
source $HOME/OpenFOAM/2.3.0/gnu/openmpi/OpenFOAM-2.3.0/etc/bashrc

pimpleFoam1Step -parallel
EOF
) > application1Step.sh

chmod +x application1Step.sh

(
    pwd

    env

tmp=`cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor`
tmp2=`cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq | tr '\n' ','`
echo $HOSTNAME,$tmp,$tmp2

    mpirun --bind-to-core -mca btl openib,sm,self \
	-n $(getNumberOfProcessors) -hostfile $PBS_NODEFILE ./application1Step.sh

tmp=`cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor`
tmp2=`cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq | tr '\n' ','`
echo $HOSTNAME,$tmp,$tmp2

    mpirun --bind-to-core -mca btl openib,sm,self \
	-n $(getNumberOfProcessors) -hostfile $PBS_NODEFILE ./application.sh
) >& log.$PBS_JOBID
