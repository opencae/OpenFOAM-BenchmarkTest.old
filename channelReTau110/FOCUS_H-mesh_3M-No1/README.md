# FOCUS_H-mesh_3M-No1

## General information

* Measurer:  Masashi Imano
* Date: Sep 24 2016 - Sep 29 2016

## Benchmark condition

* Number of mesh：2995200(3M)
* Number of processors(Number of node)：8(1),16(2),32(4),64(8),128(16),256(32),512(64),544(68)

## Hardware

* Name: FOCUS H system
* Site: Foundation for Computational Science ( https://www.j-focus.or.jp/ )
* System
  * Number of Node: 68
* Node
  * CPU
    * Processor: Intel Xeon D-1541
    * Number of Processor(core): 1(8)
    * Frequency: 2.1GHz
    * Peak performance: 204.8 GFlops
  * Memory
    * Size: 64GB
  * Interconnect: 10GbE x 2

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
  * Additional suffix
    * DEBUG2: I_MPI_DEBUG=2
* INTELMPI513
  * MPI library: Intel MPI 5.1.3 (module load impi513)
  * Excution command: mpirun
  * Additional suffix
    * DEBUG2: I_MPI_DEBUG=2
