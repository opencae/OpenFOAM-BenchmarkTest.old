# FOCUS_F-mesh_3M-No1

## General information

* Measurer:  Masashi Imano
* Date: Sep 25 2016 - Sep 28 2016, Oct 2 2016

## Benchmark condition

* Number of mesh：23961600(24M)
* Number of processors(Number of node)：40(1),80(2),160(4),320(8),400(10)

## Hardware

* Name: FOCUS F system
* Site: Foundation for Computational Science ( https://www.j-focus.or.jp/ )
* System
  * Number of Node: 12
* Node
  * CPU
    * Processor: Intel Xeon E5-2698 v4
    * Number of Processor(core): 2(40)
    * Frequency: 2.2GHz
    * Peak performance: 1152 GFlops
  * Memory
    * Size: 128GB
  * Interconnect: FDR-InfiniBand(56Gbps)

## Solve batch script

### OpenFOAM version

* OF230
  * Software version: OpenFOAM-2.3.0

### Compiler

* Gcc
  * Version: Gcc 4.8.3
  * Optimize option for c++: -O3 (default)
  * Optimize option for c: -O3 (default)
* Icc
  * Version: Icc-14.0.0.080 (module load PrgEnv-intel-14.0.0.080)
  * Optimize option for c++: -axAVX,SSE4.2 -O2 -no-prec-div
  * Optimize option for c: -O3 -no-prec-div (default)
* Icc14
  * Version: Icc-14.0.2.144 (module load PrgEnv-intel-14.0.2.144)
  * Optimize option for c++: -axAVX2,AVX,SSE4.2 -O2 -no-prec-div
  * Optimize option for c: -O3 -no-prec-div (default)

### MPI Library 

* OPENMPI
  * MPI library: OpenMPI 1.6.5 (module load gnu/openmpi165)
  * Excution command: mpirun -bind-to-core
* INTELMPI
  * MPI library: Intel MPI 4.1.1 (module load impi411)
  * Excution command: mpirun

* INTELMPI513
  * MPI library: Intel MPI 5.1.3 (module load impi513)
  * Excution command: mpirun
