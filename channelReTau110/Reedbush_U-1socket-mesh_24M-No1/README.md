# Reedbush_U-1socket-mesh_24M-No1

## General information

* Measurer:  Masashi Imano
* Date: Nov 17 2016

## Benchmark condition

* Number of mesh：23961600(24M)
* Number of processors(Number of node)：18(1)
* Note: Use one socket only


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

* OF41
  * Software version: OpenFOAM-4.1

### Compiler

* Icc
  * Version: Icc-16.0.3.210 (module: intel/16.0.3.210)
  * Optimize option for c++: -O3 (default)
  * Optimize option for c: -O3 (default)

### MPI Library 

* INTELMPI
  * MPI library: Intel MPI 5.1.3.210 (module: intel-mpi/5.1.3.210)
  * Excution command: mpirun numactl --cpunodebind=0 --membind=0


