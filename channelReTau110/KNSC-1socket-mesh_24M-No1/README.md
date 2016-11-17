# # KNSC-1socket-mesh_24M-No1

## General information

* Measurer:  Masashi Imano
* Date: Nov 17 2016

## Benchmark condition

* Number of mesh：23961600(24M)
* Number of processors(Number of node)：10(1)
* Note: Use one socket only

## Hardware

* Name: KNSC
* Site: Supercomputing Division, Information Technology Center The University of Tokyo
* System
  * Number of Node: 64
  * Peak performance: 28.7 TFlops
  * Memory: 4096 GByte
  * Network topology: Fat-Tree with Full-Bisection Bandwidth
* Node
  * CPU
    * Processor: Intel(R) Xeon(R) CPU E5-2680 v2
    * Number of Processor(core): 2(20)
    * Frequency: 2.80GHz
    * Peak performance: 224 GFlops
  * Memory
    * Size: 32GB 
    * Type: DDR3
  * Interconnect: Infiniband-FDR(Mellanox Connect-IB dual port) (56Gbps/port)

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

* INTELMPI_1socket
  * MPI library: Intel MPI 5.1.3.210 (module: intel-mpi/5.1.3.210)
  * Excution command: mpirun numactl --cpunodebind=0 --membind=0

