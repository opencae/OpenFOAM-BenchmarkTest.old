#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pylab
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

data=np.genfromtxt("table.csv", names=True, delimiter=',', dtype=None)

pp = PdfPages('plot.pdf')

mpl.rcParams.update({'font.size': 12})

nCellsArray=np.unique(data['nCells'])
LESModelArray=np.unique(data['LESModel'])
solverArray=np.unique(data['solver'])
nProcsArray=np.unique(data['nProcs'])

pylab.subplots_adjust(bottom=0.5)
            
for nCells in nCellsArray:
    for LESModel in LESModelArray:
        for nProcs in nProcsArray:
            idx=np.where(
                (data['nCells']==nCells)
                & (data['LESModel']==LESModel)
                & (data['nProcs']==nProcs)
                )

            solver=data['solver'][idx]
            preconditioner=data['preconditioner'][idx]
            solvers=np.core.defchararray.add(np.core.defchararray.add(solver, "-"),preconditioner)

            y=data['ExectutionTimeStepss'][idx]

            sn,index0 = np.unique(solvers, return_index=True)
            index1=index0[1:]
            index1=np.append(index1,len(y))
            executionTimeAve=np.zeros(len(sn))
            executionTimeSTD=np.zeros(len(sn))
            for i in range(len(sn)):
                executionTime=y[index0[i]:index1[i]]
                executionTimeAve[i]=np.average(executionTime)
                executionTimeSTD[i]=np.std(executionTime)

            base=str(nCells)+"cells-"+LESModel+"-"+str(nProcs)+"MPI-time"
            print base

            x=np.arange(len(sn))

            offset=(x[len(x)-1]-x[0])*0.05
            xmin=x[0]-offset
            xmax=x[len(x)-1]+offset

            plt.title("Execution time per time step\n("+
                      str(nCells/1e+6)+"M cells, "+LESModel+" ,"+str(nProcs)+" MPI)")
            plt.plot(x,executionTimeAve, label="Execution time per time step [s]", linewidth=1)
            plt.errorbar(x, executionTimeAve, yerr=executionTimeSTD, fmt='.', linewidth=2)
            plt.xlabel('Matrix solver for pressure equation')
            plt.ylabel('Execution time per time step [s]')
            plt.xticks(x,sn, rotation=-90)
            ymin, ymax = plt.ylim()
            ymin=0
            plt.xlim(xmin, xmax)
            plt.ylim(ymin,ymax*1.1)
            plt.grid()
            pp.savefig()
            plt.clf()

pylab.subplots_adjust(bottom=0.1)

for nCells in nCellsArray:
    for LESModel in LESModelArray:
        for solver in solverArray:
            idxSolver=np.where(data['solver']==solver)
            preArray=np.unique(data['preconditioner'][idxSolver])
            for pre in preArray:
                idx=np.where(
                    (data['nCells']==nCells)
                    & (data['LESModel']==LESModel)
                    & (data['solver']==solver)
                    & (data['preconditioner']==pre)
                    )
                x=data['nProcs'][idx]
                y=data['ExectutionTimeStepss'][idx]

                mpi,index0 = np.unique(x, return_index=True)
                index1=index0[1:]
                index1=np.append(index1,len(y))
                executionTimeAve=np.zeros(len(mpi))
                executionTimeSTD=np.zeros(len(mpi))
                srSTD=np.zeros(len(mpi))
                peSTD=np.zeros(len(mpi))
                for i in range(len(mpi)):
                    executionTime=y[index0[i]:index1[i]]
                    executionTimeAve[i]=np.average(executionTime)
                    executionTimeSTD[i]=np.std(executionTime)

                    sr=executionTimeAve[0]/executionTime
                    srSTD[i]=np.std(sr)

                    pe=sr/(mpi[i]/mpi[0])*100.0
                    peSTD[i]=np.std(pe)

                srAve=executionTimeAve[0]/executionTimeAve
                peAve=srAve/(mpi/mpi[0])*100

                base=str(nCells)+"cells-"+LESModel+"-"+solver+"-"+pre
                print base

                offset=(mpi[len(mpi)-1]-mpi[0])*0.05
                xmin=mpi[0]-offset
                xmax=mpi[len(mpi)-1]+offset

                plt.title("Execution time per time step\n("+
                          str(nCells/1e+6)+"M cells, "+LESModel+" ,"+solver+"-"+pre+")")
                plt.xlabel('Number of MPI processes')
                plt.xticks(mpi)
                plt.grid()
                plt.plot(mpi,executionTimeAve, label="Execution time per time step [s]", linewidth=1)
                plt.errorbar(mpi, executionTimeAve, yerr=executionTimeSTD, fmt='.', linewidth=2)
                plt.ylabel('Execution time per time step [s]')
                ymin, ymax = plt.ylim()
                ymin=0
                plt.xlim(xmin, xmax)
                plt.ylim(ymin,ymax*1.1)
                pp.savefig()
                plt.clf()

                plt.title("Speedup ratio\n("+
                          str(nCells/1e+6)+"M cells, "+LESModel+" ,"+solver+"-"+pre+")")
                plt.xlabel('Number of MPI processes')
                plt.xticks(mpi)
                plt.grid()
                plt.plot(mpi,srAve, label="Speedup ratio")    
                plt.errorbar(mpi, srAve, srSTD, fmt='.')
                plt.plot([xmin, xmax], [xmin/mpi[0], xmax/mpi[0]], 'k-', label="Ideal")
                plt.ylabel('Speedup ratio [-]')
                ymin, ymax = plt.ylim()
                ymin=0
                plt.xlim(xmin, xmax)
                plt.ylim(ymin,ymax*1.1)
                plt.legend(loc='upper left')
                pp.savefig()
                plt.clf()

                plt.title("Parallel efficiency\n("+
                          str(nCells/1e+6)+"M cells, "+LESModel+" ,"+solver+"-"+pre+")")
                plt.xlabel('Number of MPI processes')
                plt.xticks(mpi)
                plt.grid()
                plt.plot(mpi,peAve, label="Parallel efficiency")    
                plt.errorbar(mpi, peAve, peSTD, fmt='.')
                plt.plot([xmin, xmax], [100, 100], 'k-', label="Ideal")
                plt.ylabel('Parallel efficiency [%]')
                xmin, xmax = plt.xlim()
                ymin, ymax = plt.ylim()
                ymin=0
                plt.ylim(ymin,ymax*1.1)
                pp.savefig()
                plt.clf()

pp.close()
