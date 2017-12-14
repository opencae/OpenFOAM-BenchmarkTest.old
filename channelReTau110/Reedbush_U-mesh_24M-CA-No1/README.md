# Reedbush_U-mesh_24M-CA-No1

## General information

* Measurer:  Masashi Imano
* Date: Nov 2017

## Benchmark condition

* Number of mesh：23961600(24M)
* Number of processors(Number of node)：32(1),64(2),128(4),256(8),512(16),1024(32),2048(64),4096(128)

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

## fvSolution

* PCG: Standard preconditioned CG in OpenFOAM v1612+
* PCGPG: Preconditioned Chronopoulos/Gear CG
* PPCG: Preconditioned pipelined CG
* GACG: Preconditioned Gropp’s asynchronous CG

## Reference

* P. Ghysels, W. Vanroose: Hiding global synchronization latency in the preconditioned Conjugate Gradient algorithm, Parallel Computing, 40-7, pp.224-238, 2014.
