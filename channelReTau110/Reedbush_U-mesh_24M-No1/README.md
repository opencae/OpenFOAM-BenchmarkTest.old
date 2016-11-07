# Reedbush_U-mesh_24M-No1

## General information

* Measurer:  Masashi Imano
* Data: Oct 30 2016 - Nov 06 2017

## Benchmark condition

* Number of mesh：23961600(24M)
* Number of processos(Number of node)：36(1),72(2),144(4),288(8),576(16),864(24),1152(64),2304(128)

## Hardware

* Name: Reedbush-U (http://www.cc.u-tokyo.ac.jp/system/reedbush/)
* Site: Supercomputing Division, Information Technology Center The University of Tokyo
* System
  * Number of Node: 420
  * Peak performance: 508.03 TFlops
  * Memory: 105 TByte
  * Network topology: Full-bisection Fat Tree
* Node
  * Name: Product name: SGI Rackable C2112-4GP3
  * CPU
    * Processor: Intel Xeon E5-2695v4 (Broadwell-EP)
    * Number of Processor(core): 2(36)
    * Frequency: 2.1GHz-3.3GHz (Turbo boost)
    * Peak performance: 1209.6 GFlops
  * Memory
    * Size: 256GB
    * Bandwidth: 153.6 GB/sec
  * Interconnect: Infiniband EDR 4x(100Gbps)

## Solve batch script

### OpenFOAM version

* OF41
  * Software version: OpenFOAM-4.1

### Compiler

* Icc
  * Version: Icc-16.0.3.210 (module: intel/16.0.3.210)
  * Optimize option for c++: -O3 (default)
  * Optimize option for c: -O3 (default)
* Icc_OptxHost
  * Version: Icc-16.0.3.210 (module: intel/16.0.3.210)
  * Optimize option for c++: -O3 -xHost
  * Optimize option for c: -O3 -no-prec-div
* Icc1604
  * Version: Icc-16.0.4.258 (module: intel/16.0.4.258)
  * Optimize option for c++: -O3 (default)
  * Optimize option for c: -O3 (default)
* Icc1604_OptxHost
  * Version: Icc-16.0.4.258 (module: intel/16.0.4.258)
  * Optimize option for c++: -O3 -xHost
  * Optimize option for c: -O3 -no-prec-div
* Gcc
  * Version: Gcc 4.8.5 20150623 (system compiler)
  * Optimize option for c++: -O3 (default)
  * Optimize option for c: -O3 (default)
* Gcc_Optavx2
  * Version: Gcc 4.8.5 20150623 (system compiler)
  * Optimize option for c++: -O3 -march=core-avx2
  * Optimize option for c: -O3 -march=core-avx2

### MPI Library 

* INTELMPI
  * MPI library: Intel MPI 5.1.3.210 (module: intel-mpi/5.1.3.210)
  * Excution command: mpirun
  * Additional suffix
    * DC0: I_MPI_DYNAMIC_CONNECTION=0 
    * OFA: I_MPI_FABRICS=shm:ofa;I_MPI_FALLBACK=disable
    * UD1: I_MPI_DAPL_UD=enable
    * VTUNE: mpirun -gtool "amplxe-cl -c hotspots -target-tmp-dir=/dev/shm :0 -r Directory"
* INTELMPI513258
  * MPI library: Intel MPI 5.1.3.258 (module: intel-mpi/5.1.3.258)
  * Excution command: mpirun
* SGIMPI
  * MPI library: SGI MPT 2.14 (module: mpt/2.14)
  * Excution command: mpiexec_mpt
* OPENMPI
  * MPI library: OpenMPI 1.10.2 (module: openmpi/1.10.2/gnu)
  * Excution command: mpirun
