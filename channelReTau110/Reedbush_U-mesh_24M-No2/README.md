# Reedbush_U-mesh_24M-No2

## General information

* Measurer:  Masashi Imano
* Date: Jan 11 2017

## Benchmark condition

* Number of mesh：23961600(24M)
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

* OFv1612+
  * Software version: OpenFOAM-v1612+ (system)

### Compiler

* Icc
  * Version: Icc-16.0.3.210 (module: intel/16.0.3.210)
  * Optimize option for c++: -O3 (default)
  * Optimize option for c: -O3 (default)
* Gcc
  * Version: Gcc 4.8.5 20150623 (system compiler)
  * Optimize option for c++: -O3 (default)
  * Optimize option for c: -O3 (default)

### MPI Library 

* SGIMPI
  * MPI library: SGI MPT 2.14 (module: mpt/2.14)
  * Excution command: mpiexec_mpt
* OPENMPI
  * MPI library: OpenMPI 1.10.2 (module: openmpi/1.10.2/gnu)
  * Excution command: mpirun
