# Oakforest-PACS-mesh_24M-No2

## General information

* Measurer:  Masashi Imano
* Date: Jan 20 2017-Jan 21 2017

## Benchmark condition

* Number of mesh：23961600(24M)
* Number of processors(Number of node): 64(1) - 32768(512), 128(1) - 32768(256), 256(1) - 32768(128)

## Hardware

* Name: Oakforest-PACS (http://www.cc.u-tokyo.ac.jp/system/ofp/)
* Site: Joint Center for Advanced High Performance Computing (http://jcahpc.jp/eng/index.html)
* System
  * Number of Node: 8208
  * Peak performance: 25.004 PFlops
  * Memory: 897 TByte
  * Network topology: Full-bisection Fat Tree
* Node
  * Name: Fujitsu PRIMERGY CX1640 M1
  * CPU
    * Processor: Intel® Xeon Phi 7250 (Knights Landing)
    * Number of Processor(core): 1(68)
    * Frequency: 1.4GHz
    * Peak performance: 3.0464 TFlops
  * Memory
    * Size: 96 GB(DDR4)＋ 16 GB(MCDRAM)
  * Interconnect: Intel Omni-Path (100Gbps)

## Solve batch script 

Solve batch script name:

"OpenFOAM version"_"Compiler"_" "MPI Library"_"Processor per node"_"Configuration mode"_"Execution command" 

### OpenFOAM version

* v1612+
  * Software version: OpenFOAM-v1612+

### Compiler

* ThirdParty_Gcc
  * Version: Gcc 6.2.0
  * Optimize option for c++: -O3 (default)
  * Optimize option for c: -O3 (default)

* ThirdParty_GccKNL
  * Version: Gcc 6.2.0
  * Optimize option for c++: -O3 (default)
  * Optimize option for c: -O3 (default)

* system_Icc
  * Version: Icc 2017.1.132 (module: intel/2017.1.132)
  * Optimize option for c++: -O3 (default)
  * Optimize option for c: -O3 (default)

* system_IccKNL
  * Version: Icc 2017.1.132 (module: intel/2017.1.132)
  * Optimize option for c++: -O3 (default)
  * Optimize option for c: -O3 (default)

### MPI Library

* INTELMPI
  * MPI library: Intel MPI 2017.1.132 (module: impi/2017.1.132)

### Processor per node

* 64
* 128
* 256

### Memory configuration mode

* cache
* flat

### Solver execution command 

* 0
  * mpirun pimpleFoam -parallel

* 1
  * export I_MPI_PIN_PROCESSOR_EXCLUDE_LIST=0,68,136,204
  * mpirun numactl --membind=1 pimpleFoam -parallel

* 2
  * export I_MPI_PIN_PROCESSOR_EXCLUDE_LIST=0,68,136,204
  * mpirun numactl --membind=0 pimpleFoam -parallel

* 3
  * export I_MPI_PIN_PROCESSOR_EXCLUDE_LIST=0,68,136,204
  * mpirun numactl --preferred=1 pimpleFoam -parallel

* 4
  * export I_MPI_PIN_PROCESSOR_EXCLUDE_LIST=0,68,136,204
  * mpirun numactl --preferred=0 pimpleFoam -parallel

* 5
  * mpirun numactl --membind=1 pimpleFoam -parallel

* 6
  * mpirun numactl --membind=0 pimpleFoam -parallel

* 7
  * mpirun numactl --preferred=1 pimpleFoam -parallel

* 8
  * mpirun numactl --preferred=0 pimpleFoam -parallel
