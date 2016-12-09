# Reedbush_U-mesh_3M-No1

## General information

* Measurer:  Masashi Imano
* Date: Jul 9 2016 - Jul 14 2016

## Benchmark condition

* Number of mesh：2995200(3M)
* Number of processors(Number of node)：36(1),72(2),144(4),288(8),576(16),864(24),1152(64),2304(128)

## Hardware

* Name: Reedbush-U (http://www.cc.u-tokyo.ac.jp/system/reedbush/)
* Site: Supercomputing Division, Information Technology Center The University of Tokyo
* System
  * Number of Node: 420
  * Peak performance: 508.03 TFlops
  * Memory: 105 TByte
  * Network topology: Full-bisection Fat Tree
* Node
  * Name: SGI Rackable C2112-4GP3
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

* OF230
  * Software version: OpenFOAM-2.3.0

* OF230_RIST
  * Software version: OpenFOAM-2.3.0
  * With optimisation of communication structures (see below)
     * https://develop.openfoam.com/Development/OpenFOAM-plus/commit/6c8f53012d23be5bb3ad49760db002a6057b4b18
     * https://develop.openfoam.com/Development/OpenFOAM-plus/commit/b50753556b6396628feec69d113fe23146fe4473

### Compiler

* Icc
  * Version: Icc-16.0.3.210 (module: intel/16.0.3.210)
  * Optimize option for c++: -xHost -O2 -no-prec-div (default)
  * Optimize option for c: -O3 -no-prec-div (default)
* Gcc
  * Version: Gcc 4.8.5
  * Optimize option for c++: -O3 (default)
  * Optimize option for c: -O3 (default)

### MPI Library 

* INTELMPI
  * MPI library: Intel MPI 5.1.3.210 (module: intel-mpi/5.1.3.210)
  * Excution command: mpirun
* OpenMPI
  * MPI library: OpenMPI 1.8.3 (module: openmpi/1.8.3/gnu)
  * Excution command: mpirun
* SGIMPI
  * MPI library: SGI MPT 2.14 (module: mpt/2.14)
  * Excution command: mpiexec_mpt
* SYSTEMHPCXMPI3_3_1
  * MPI library: hpcx 3.3-1.0.0.0 (module: hpcx/3.3-1.0.0.0)
  * Excution command: mpirun
* SYSTEMMVAPICH2MPI2_2_rc1
  * MPI library: mvapich2/2.2rc1 (module: mvapich2/2.2rc1/gnu or mvapich2/2.2rc1/intel)
  * Excution command: mpirun
* SYSTEMOPENMPI
  * MPI library: OpenMPI 1.10.2 (module: openmpi/1.10.2/gnu)
  * Excution command: mpirun
